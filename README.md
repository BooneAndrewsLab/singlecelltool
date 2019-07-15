# singlecelltool
_Custom-made graphical user interface (GUI) application written in Python which allows 
users to view and label single cell images on a grid layout. Users can save a phenotype 
for each cell and then export the data._

### OS compatibility
Tested on: Linux, macOS


### Prerequisites
Python 2.7 or 3: https://www.python.org/downloads

### Installation and Usage
Clone the repository
```
git clone https://github.com/BooneAndrewsLab/singlecelltool.git
cd singlecelltool
```

Install required packages
```
pip install -r requirements.txt
```

Run the application
```
python singlecelltool.py
```

### User input requirements 
* Single cell data file - a spreadsheet containing the single cell information such as 
image path location, cell coordinates and initial label (if available). The CSV or 
excel file should strictly follow the order of column information: (1) image path, 
(2) x-coordinate, (3) y-coordinate, (4 *optional) initial label. 

* Phenotype list -  a file containing a list of all possible phenotype or label

* Cell count - total number of cells to be processed from the uploaded single cell 
data file. This is optional. By default, no limit is set.

* Display limit - number of cells to be displayed on a single page. The default is 20.

* Crop size - Pixel size to be used in cropping single cells from the image.
The default is 50.

### Output
The output is a CSV file containing all the labeled single cells.

