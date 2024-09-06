import sys
from colorama import Fore, init
from core.ocr import execute_ocr

# This script runs experiments

# parameters:
# 1) dataset_path - Path to dataset. This can be a directory or a specific image. [REQUIRED]
# for example:
# ../datasets/PE014F03
# ../datasets/PE014F03/image_637872639234119245.bmp

# 2) text_to_find - Text searched in the picture. e.g. PE014F03 [REQUIRED]
# this can be:
# PE014F03
# PE014012
# PE514024

# 3) experiment - Experiment type. Enter values A, B or C. [REQUIRED]
# We have 3 experiments that differ in the specified cropping region.
# A - Left image: [50:150, 265:540] Right image: [1050:1150, 265:540]
# B - Left image: [50:140, 245:560] Right image: [1060:1135, 320:560]
# C - Left image: [45:140, 255:555] Right image: [1045:1140, 255:555]

# 4) accuracy - Accuracy per relay or Accuracy per image. [REQUIRED]
# enter "0" for Accuracy per relay
# enter "1" Accuracy per image

# 5) preprocessing - Preprocessing.
# If you do not enter, no preprocessing is used. [REQUIRED]
# none - No preprocessing
# binary - Simple binary thresholding
# mean - Adaptive mean thresholding
# gaus - Adaptive gaussian thresholding
# otsu - Otu’s thresholding
# dilate - Eroding
# erode - Dilating

# 6) - Debug mode. [OPTIONAL]
# You can add "debug" parameter to command.
# If debug is enabled, a preview of the output images is displayed. This is done for each image in the dataset.
# It is recommended to use this only if one input image is tested.

# command example:
# python run.py [dataset_path] [text_to_find] [experiment] [accuracy] [preprocessing] [debug]
# python run.py ../datasets/PE514024/ PE514024 A 0 mean debug


dataset_path = sys.argv[1]
text_to_find = sys.argv[2]
experiment = sys.argv[3]
accuracy = sys.argv[4]
preprocessing = sys.argv[5]


# colorama init
init()

print(Fore.MAGENTA + "***** Script started ***** ")    
print("Dataset: " + dataset_path)        
print("Text to find: " + text_to_find)   
print("Experiment: " + experiment)   
print("Accuracy per relay" if accuracy == 0 else "Accuracy per image")   
print("Debug: " + str('debug' in sys.argv))   
print("\n")  

execute_ocr(dataset_path, text_to_find, experiment, int(accuracy), preprocessing, 'debug' in sys.argv)

