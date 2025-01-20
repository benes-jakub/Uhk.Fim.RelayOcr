import sys
from colorama import Fore, init
from core.ocr import execute_ocr

datasets = ["PE014012"]
experiments = ["C"]
preprocessings = ["none"]

for ind, dataset in enumerate(datasets, start = 0): 
    for ind, preprocessing in enumerate(preprocessings, start = 0): 
        for ind, experiment in enumerate(experiments, start = 0):             
            result = execute_ocr("../datasets/" + dataset + "/", dataset, experiment, 0, preprocessing, True, True)
            print(dataset + " " + preprocessing + " " + experiment + ": " + result)            
        print("\n")