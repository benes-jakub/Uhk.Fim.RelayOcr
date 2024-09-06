# Quality control of labels using OCR

Source codes for replicating test scenarios from article Quality control of labels using OCR.

## Required core technologies

Scripts and scenarios were tested on these versions. It is possible to use updated versions, but the same results and functionality of the scripts are not guaranteed.

- Python (https://www.python.org/). Project developed on version 3.10.1
- Tesseract (https://digi.bib.uni-mannheim.de/tesseract/). Project developed on version 5.0.1.20220118
- opencv-python (https://pypi.org/project/opencv-python/). Project developed on version 4.9.0.80
- pytesseract (https://pypi.org/project/pytesseract/). Project developed on version 0.3.10
- Colorama (https://pypi.org/project/colorama/). Project developed on version 0.4.6

## Installation

1. Install Python.
2. Install Tesseract (https://digi.bib.uni-mannheim.de/tesseract/).
3. Install libraries. The file requirements.txt is ready. To install the libraries, go to the project root and call the following command.

```
pip install -r requirements.txt
```

## Docs

Only run the `run.py` script, which can be found in the `src` directory. The run command should look like this.

```
python run.py [dataset_path] [text_to_find] [experiment] [accuracy] [preprocessing] [debug]
```

### Parameters

**dataset_path [REQUIRED]**<br /> Path to dataset. This can be a directory or a specific image.

```
# example
../datasets/PE014F03
../datasets/PE014F03/image_637872639234119245.bmp
```

**text_to_find [REQUIRED]**<br /> Text searched in the picture.

```
# allowed values
PE014F03
PE014012
PE514024
```

**experiment [REQUIRED]**<br /> Experiment type. Enter values `A`, `B` or `C`.

```
# We have 3 experiments that differ in the specified cropping region.
A - Left image: [50:150, 265:540] Right image: [1050:1150, 265:540]
B - Left image: [50:140, 245:560] Right image: [1060:1135, 320:560]
C - Left image: [45:140, 255:555] Right image: [1045:1140, 255:555]
```

**accuracy [REQUIRED]**<br /> Accuracy per relay or Accuracy per image.

```
# allowed values
0 for Accuracy per relay
1 for Accuracy per image
```

**preprocessing [REQUIRED]**<br /> Preprocessing method.

```
# allowed values
none - No preprocessing
binary - Simple binary thresholding
mean - Adaptive mean thresholding
gaus - Adaptive gaussian thresholding
otsu - Otu’s thresholding
dilate - Eroding
erode - Dilating
```

**debug [OPTIONAL]**<br /> You can add `debug` parameter to command. If debug is enabled, a preview of the output images is saved into debug directory in project root. This is done for each image in the dataset.

### Command example

```
# dataset "PE514024", looking for text "PE514024". It is selected experiment A. Accuracy i per relay. Adaptive mean thresholding preprocessing method will be used. Debug mode is enabled.

python run.py ../datasets/PE514024/ PE514024 A 0 mean debug
```
