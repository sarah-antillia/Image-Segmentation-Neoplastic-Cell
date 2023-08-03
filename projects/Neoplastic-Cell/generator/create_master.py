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

import os
import shutil
import cv2
import numpy as np
import traceback
"""
`masks.npy` an array of 6 channel instance-wise masks 
 (0: Neoplastic cells, 
  1: Inflammatory, 
  2: Connective/Soft tissue cells, 
  3: Dead Cells, 
  4: Epithelial, 
  6: Background)
"""

  
def create_images(input_file, mask_output_dir, images_output_dir):

  if os.path.exists(images_output_dir):
    shutil.rmtree(images_output_dir)

  if not os.path.exists(images_output_dir):
    os.makedirs(images_output_dir)

  images = np.load(input_file,  mmap_mode='r')
  
  index = 10000

  for image in images:
    try:
      print(image.shape) 
      w, h, c = image.shape
      if w <=1 or h<=1:
       continue
 
      image = np.array(image)

      index += 1

      image_file = str(index) + ".jpg"
      image_filepath = os.path.join(images_output_dir, image_file)
      mask_filepath  = os.path.join(mask_output_dir, image_file)
      if os.path.exists(mask_filepath):
        
        cv2.imwrite(image_filepath, image)
        print("Saved image {}".format(image_filepath))
      else:
        print("No found correspondimg mask to image {}".format(image_filepath))
    except:
      traceback.print_exc()


def create_masks(input_file, output_dir, channels=[0]):

  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  images = np.load(input_file,  mmap_mode='r')
  
  index = 10000

  for image in images:
    try:
      print(image.shape) 
      w, h, c = image.shape
      if w <=1 or h<=1:
       continue
 
      image = np.array(image)

      index += 1

      image_file = str(index) + ".jpg"
      image_filepath = os.path.join(output_dir, image_file)
 
     
      if len(channels)== 1:
        channel = channels[0]
        img = image[:, :, channel]
        print("  mask shape {}".format(img.shape))
        image_file = str(index)  + ".jpg"
        if np.any(img) >0:
          image_filepath = os.path.join(output_dir, image_file)
          cv2.imwrite(image_filepath, img)
          print("Saved mask {}".format(image_filepath))
        else:
         print("Empty mask {}".format(image_file))
      else :     
        """
          `masks.npy` an array of 6 channel instance-wise masks 
            0: Neoplastic cells, 
            1: Inflammatory, 
            2: Connective/Soft tissue cells, 
            3: Dead Cells, 
            4: Epithelial, 
            6: Background)
        """     
        channels = [0, 1, 2, 3, 4, 6]
        for i in channels:
          img = image[:, :, i]
          print("  mask shape {}".format(img.shape))
          image_file = str(index) + "_mask_" +str(i) + ".jpg"
          
          image_filepath = os.path.join(output_dir, image_file)
          cv2.imwrite(image_filepath, img)
          print("Saved mask {}".format(image_filepath))

    except:
      traceback.print_exc()


if __name__ == "__main__":
  try:
   
 
   input_masks_file  = "./Masks/masks.npy"
   masks_output_dir  = "./PanNuke-Base/masks"

   #channel = 0: Neoplastic cells, 
   # all channels
   #  channels = [0, 1, 2, 3, 4, 6]
   # If you would like to create massks for 
   #  0: Neoplastic cells, 
   # specify 
   #   channels = [0]
   create_masks(input_masks_file, masks_output_dir, channels = [0])

   input_images_file = "./Images/images.npy"
   images_output_dir = "./PanNuke-Base/images"

   create_images(input_images_file, masks_output_dir , images_output_dir)
  
  except:
    traceback.print_exc()
