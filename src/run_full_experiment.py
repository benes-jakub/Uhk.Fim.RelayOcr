import sys
from colorama import Fore, init
from core.ocr import execute_ocr

datasets = ["PE514024", "PE514F03", "PE014012"]
experiments = ["A", "B", "C"]
preprocessings = ["none", "binary", "mean", "gaus", "otsu", "dilate", "erode"]

for ind, dataset in enumerate(datasets, start = 0): 
    for ind, preprocessing in enumerate(preprocessings, start = 0): 
        for ind, experiment in enumerate(experiments, start = 0):             
            result = execute_ocr("../datasets/" + dataset + "/", dataset, experiment, 0, preprocessing, False, True)
            print(dataset + " " + preprocessing + " " + experiment + ": " + result)            
        print("\n")