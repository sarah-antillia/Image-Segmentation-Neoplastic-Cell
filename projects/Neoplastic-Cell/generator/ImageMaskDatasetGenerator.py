# Copyright 2023 antillia.com Toshiyuki Arai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# 2023/08/02 to-arai solarsystem-laboratory.com

import os
import shutil
import glob
import cv2
import numpy as np
import traceback
from PIL import Image, ImageOps, ImageFilter

"""
# License

[Attribution-NonCommercial-ShareAlike 4.0 International](http://creativecommons.org/licenses/by-nc-sa/4.0/)

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

# Please cite:


1:

```latex
@article{gamper2020pannuke,
  title={PanNuke Dataset Extension, Insights and Baselines},
  author={Gamper, Jevgenij and Koohbanani, Navid Alemi and Graham, Simon and Jahanifar, Mostafa and Benet, Ksenija and Khurram, Syed Ali and Azam, Ayesha and Hewitt, Katherine and Rajpoot, Nasir},
  journal={arXiv preprint arXiv:2003.10778},
  year={2020}
}
```

2: 

```
@inproceedings{gamper2019pannuke,
  title={Pannuke: An open pan-cancer histology dataset for nuclei instance segmentation and classification},
  author={Gamper, Jevgenij and Koohbanani, Navid Alemi and Benet, Ksenija and Khuram, Ali and Rajpoot, Nasir},
  booktitle={European Congress on Digital Pathology},
  pages={11--19},
  year={2019},
  organization={Springer}
}
```

"""

"""
`masks.npy` an array of 6 channel instance-wise masks 
 (0: Neoplastic cells, 
  1: Inflammatory, 
  2: Connective/Soft tissue cells, 
  3: Dead Cells, 
  4: Epithelial, 
  6: Background)
"""

class ImageMaskDatasetGenerator:
  def __init__(self):
    pass
    
  def augment(self, image, output_dir, filename):
    # 2023/08/02
    #ANGLES = [30, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    ANGLES = [0, 90, 180, 270]
    for angle in ANGLES:
      rotated_image = image.rotate(angle)
      output_filename = "rotated_" + str(angle) + "_" + filename
      rotated_image_file = os.path.join(output_dir, output_filename)
      #cropped  =  self.crop_image(rotated_image)
      rotated_image.save(rotated_image_file)
      print("=== Saved {}".format(rotated_image_file))
      
    # Create mirrored image
    mirrored = ImageOps.mirror(image)
    output_filename = "mirrored_" + filename
    image_filepath = os.path.join(output_dir, output_filename)
    #cropped = self.crop_image(mirrored)
    
    mirrored.save(image_filepath)
    print("=== Saved {}".format(image_filepath))
        
    # Create flipped image
    flipped = ImageOps.flip(image)
    output_filename = "flipped_" + filename

    image_filepath = os.path.join(output_dir, output_filename)
    #cropped = self.crop_image(flipped)

    flipped.save(image_filepath)
    print("=== Saved {}".format(image_filepath))


  def generate(self, input_images_dir, input_masks_dir, images_output_dir, masks_output_dir,
               mono_color_mask=False):

    if os.path.exists(images_output_dir):
      shutil.rmtree(images_output_dir)

    if not os.path.exists(images_output_dir):
      os.makedirs(images_output_dir)

    if os.path.exists(masks_output_dir):
      shutil.rmtree(masks_output_dir)

    if not os.path.exists(masks_output_dir):
      os.makedirs(masks_output_dir)

    image_files = glob.glob(input_images_dir + "/*.jpg")
    
    mask_files  = glob.glob(input_masks_dir + "/*.jpg")
    num_images  = len(image_files)
    num_masks   = len(mask_files)
    
    print("=== generate num_image_files {} num_masks_files {}".format(num_images, num_masks))

    if num_images != num_masks:
      raise Exception("Not matched image_files and mask_files")
    
    
    for image_file in image_files:
      try:
        basename = os.path.basename(image_file)
        mask_filepath  = os.path.join(input_masks_dir, basename)

        image = Image.open(image_file).convert("RGB")
        self.augment(image, images_output_dir, basename)

        mask = Image.open(mask_filepath).convert("RGB")
        
        if  mono_color_mask:
          mask = self.create_mono_color_mask(mask)

        self.augment(mask, masks_output_dir,  basename)
          
      except:
        traceback.print_exc()


  def create_mono_color_mask(self, mask, mask_color=(255, 255, 255)):
    rw, rh = mask.size    
    xmask = Image.new("RGB", (rw, rh))
    #print("---w {} h {}".format(rw, rh))

    for i in range(rw):
      for j in range(rh):
        color = mask.getpixel((i, j))
        (r, g, b) = color
        # If color is blue
        if r>4 or g >4 or b > 4:
          xmask.putpixel((i, j), mask_color)

    return xmask
  
  
if __name__ == "__main__":
  try:
   generator = ImageMaskDatasetGenerator()
   

   input_images_dir  = "./PanNuke-Base/images/"
   input_masks_dir   = "./PanNuke-Base/masks/"

   images_output_dir = "./PanNuke-master/images/"
   masks_output_dir  = "./PanNuke-master/masks/"

   generator.generate(input_images_dir, input_masks_dir, 
   					  images_output_dir, masks_output_dir)
  
  except:
    traceback.print_exc()
