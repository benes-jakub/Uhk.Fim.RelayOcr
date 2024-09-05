import glob
import cv2
import numpy as np
import pytesseract
import sys
import time
from utils import rotateImage
from colorama import Fore, init

init()

def execute_ocr(dataset_path, text_to_find):
    print(dataset_path)
    print(text_to_find)


# Vytvoří string výsledků    
def processResults(result1, result2, imageName):
    if not imageName:        
        return result1 + ";" + result2
    else:
        return imageName + ": " + result1 + ";" + result2

# Ze stringu odstraňuje zbytečné symboly
def removeUnnecessarySymbols(result, searchTextLength):
    result = result.replace(" ", "").replace("|", "").replace("/", "").replace("\\", "").replace("\n", "").replace("!", "").replace(":", "")
    if(len(result) > searchTextLength):
        result = result[1:searchTextLength + 1]
    return result

# Načte cestu k souboru/souborům. Může se jednat o konkrétní image nebo o adresář.    
image_path = sys.argv[1]

# Debug proměnné
debug = False
if 'debug' in sys.argv:
    debug = True
timer = False
if 'timer' in sys.argv:
    timer = True
    start = time.time()

# Hledaný text
searchText = sys.argv[2]
# Seznam obrázků - skutečně blob
image_list = []
# Seznam názvů (cest k obrázkům)
image_names = []

# Kontrola, jestli byl zadán samostatný obrázek nebo adresář
# TODO: Možnost v parametru zvolit formát obrázku. Proč zadávat? Stačí vyčíst z přípony.
if(".bmp" in image_path):
    image_list.append(cv2.imread(image_path))
    image_names.append(image_path)
else:
    for filename in glob.glob(image_path + '/*.bmp'):
        im = cv2.imread(filename)
        image_names.append(filename)
        image_list.append(im)

# Pomocná proměnná pro výpočet úspěšnosti
okCount = 0
for ind, img in enumerate(image_list, start = 0):    
    # Otočíme celý obrázek o 90 stupňů
    # TODO: Není rychlejší nejdříve ořezat a pak otočit?
    img_rotated = rotateImage(img, -90, None, 0.8)    

    # Na obrázku se nacházejí 2 relé. Známe přibližnou polohu každého relé a textu na něm. Ořízneme.       
    cropped_image1 = img_rotated[790:880, 645:882]    
    cropped_image2 = img_rotated[0:80, 675:910]    
        
    # Preprocessing    
    cropped_image1 = cv2.bitwise_not(cropped_image1)
    cropped_image2 = cv2.bitwise_not(cropped_image2)

    # Nastavení OCR
    custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=' + searchText    
    result1 = removeUnnecessarySymbols(pytesseract.image_to_string(cropped_image1, config=custom_config).upper(), len(searchText))
    result2 = removeUnnecessarySymbols(pytesseract.image_to_string(cropped_image2, config=custom_config).upper(), len(searchText))        

    # V debug módu počítáme úspěšnost a barevně zobrazíme výsledek
    if debug:
        isOk = False    
        # Spojíme nalezený text a číslo. Musejí se rovnat hledanému výrazu. Pro oba obrázky.    
        if(result1 == searchText or result2 == searchText):
            isOk = True
            okCount += 1
        
        # Výpis do konzole, jestli se OCR podařilo.        
        if(result1 == searchText or result2 == searchText):    
            print(Fore.GREEN + processResults(result1, result2, image_names[ind]))        
        else:
            print(Fore.RED + processResults(result1, result2, image_names[ind]))
    else:
        print(processResults(result1, result2, ""))

# Zobrazení úspěšnosti
if debug:
    print("Reliability: " + str(okCount / (len(image_names)) * 100) + "%")

if timer:    
    print("Duration: " + str(time.time() - start) + "s")

# V debug režimu postzupně zobrazíme obrázky, jak se mění
if debug:
    cv2.imshow("original", img)
    cv2.imshow("rotated", img_rotated)    
    cv2.imshow("cropped_image1", cropped_image1)
    cv2.imshow("cropped_image2", cropped_image2)    
    cv2.waitKey(0)
    cv2.destroyAllWindows()