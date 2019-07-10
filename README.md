# singlecelltool
_Custom-made graphical user interface (GUI) application written in Python which allows 
users to view single cell images on a grid layout. Users can label and save a phenotype 
for each cell and then export the data._

### OS compatibility
Linux, MacOS, Windows


### Prerequisites
Python 3: https://www.python.org/downloads

### Python Requirements
```
pillow
pandas
numpy
xlrd
```

### User input requirements 
* Single cell data file - a spreadsheet containing the single cell information such as 
image path location, cell coordinates and initial label (if available). The CSV or 
excel file should strictly follow the order of column information: (1) image path, 
(2) x-coordinate, (3) y-coordinate, (4 *optional) initial label. 

* Phenotype or label list -  a file containing a list of all possible phenotype or label

* Number of cells - users may specify a limit on how many cells should be processed 
from the uploaded single cell data file. By default, no limit is set.

* Display limit - users may specify how many cells they want to be shown on a single
page. The default is 20.

### Output
The output is a CSV file containing all the saved labeled single cells. 