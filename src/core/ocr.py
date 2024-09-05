
import sys
import cv2
import glob
import time
from colorama import Fore, init
from scipy import ndimage
import pytesseract
from .utils import rotate_image, remove_unnecessary_symbols, get_string_from_results, threshold_binary, threshold_adaptive_mean, threshold_adaptive_gaussian, threshold_adaptive_otsu, erode, dilate


IMAGE_EXTENSION = ".bmp"


def execute_ocr(dataset_path, text_to_find, experiment, accuracy, preprocessing, debug):        
    # List of image blobs
    image_list = []
    # List of image names
    image_names = []

    # Load dataset
    print("Loading dataset...")
    # If there is an extension in the path, it is the path to the image not the directory
    if(IMAGE_EXTENSION in dataset_path):
        image_list.append(cv2.imread(dataset_path))
        image_names.append(dataset_path)
    else:
        for filename in glob.glob(dataset_path + '/*' + IMAGE_EXTENSION):
            im = cv2.imread(filename)
            image_names.append(filename.rsplit('\\', 1)[-1])
            image_list.append(im)
    print("Dataset loaded!")
    print("\n")

    print("Looking for text...")
    timer_start = time.time()
    count_positive = 0
    for ind, img in enumerate(image_list, start = 0): 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  

        # There are 2 relays in the picture. We know the approximate position of each relay and the text on it. A crop is made.    
        # The cropping area is set according to the selected experiment. More in the article.
        if experiment == "A":
            cropped_image_1 = img[265:540, 50:150]    
            cropped_image_2 = img[265:540, 1050:1150]   
        if experiment == "B":
            cropped_image_1 = img[245:560, 50:140]
            cropped_image_2 = img[320:560, 1060:1135] 
        if experiment == "C":
            cropped_image_1 = img[255:555, 45:140]    
            cropped_image_2 = img[255:555, 1045:1140]       

        # Rotate the images 90 degrees
        rotated_image_1 = ndimage.rotate(cropped_image_1, -90)
        rotated_image_2 = ndimage.rotate(cropped_image_2, -90)

        # Appy preprocessing
        if preprocessing == "binary":
            rotated_image_1 = threshold_binary(rotated_image_1)
            rotated_image_2 = threshold_binary(rotated_image_2)
        if preprocessing == "mean":
            rotated_image_1 = threshold_adaptive_mean(rotated_image_1)
            rotated_image_2 = threshold_adaptive_mean(rotated_image_2)
        if preprocessing == "gaus":
            rotated_image_1 = threshold_adaptive_gaussian(rotated_image_1)
            rotated_image_2 = threshold_adaptive_gaussian(rotated_image_2)            
        if preprocessing == "otsu":
            rotated_image_1 = threshold_adaptive_otsu(rotated_image_1)
            rotated_image_2 = threshold_adaptive_otsu(rotated_image_2)
        if preprocessing == "erode":
            rotated_image_1 = erode(rotated_image_1)
            rotated_image_2 = erode(rotated_image_2)
        if preprocessing == "dilate":
            rotated_image_1 = dilate(rotated_image_1)
            rotated_image_2 = dilate(rotated_image_2)                        

        # Show images for debug
        if debug:            
            cv2.imshow("cropped image 1 " + image_names[ind], rotated_image_1)
            cv2.imshow("cropped image 2 " + image_names[ind], rotated_image_2)

        # Tesseract config
        # https://muthu.co/all-tesseract-ocr-options/
        custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=' + text_to_find            

        # Execute Tesseract for both images
        result_1 = pytesseract.image_to_string(rotated_image_1, config=custom_config).upper()
        result_2 = pytesseract.image_to_string(rotated_image_2, config=custom_config).upper()

        # Remove unnecessary symbols
        result_1 = remove_unnecessary_symbols(result_1, len(text_to_find))
        result_2 = remove_unnecessary_symbols(result_2, len(text_to_find))

        text_found = False
        # Count and print result
        if accuracy == 0 and (result_1 == text_to_find and result_2 == text_to_find):            
            text_found = True
            count_positive += 1
        if accuracy == 1 and (result_1 == text_to_find or result_2 == text_to_find):                      
            text_found = True
            count_positive += 1

        if text_found:
            print(Fore.GREEN + get_string_from_results(result_1, result_2, image_names[ind]))        
        else:
            print(Fore.RED + get_string_from_results(result_1, result_2, image_names[ind]))

    # Print final results    
    print("\n")
    print(Fore.MAGENTA + "Number of images: " + str(len(image_names)))
    print("Positive found: " + str(count_positive))
    print("Not found: " + str(len(image_names) - count_positive))
    print("Reliability: " + str(count_positive / (len(image_names)) * 100) + "%")
    print("Duration: " + str(time.time() - timer_start) + "s")

    if debug:
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        

    

