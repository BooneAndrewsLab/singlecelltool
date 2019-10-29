# singlecelltool
Custom-made graphical user interface (GUI) application that allows users to view and 
label single cell images on a grid layout. Users can save a phenotype for each cell 
and then export the data.

This tool is used in the paper: "Exploring endocytic compartment morphology with 
systematic genetics and single cell image analysis"

_Mojca Mattiazzi Usaj, Nil Sahin, Helena Friesen, Carles Pons, Matej Usaj,
 Myra Paz Masinas, Ermira Shuteriqi, Aleksei Shkurin, Patrick Aloy, Quaid Morris, 
 Charles Boone, and Brenda J. Andrews_
 
Note: If input is a multi-frame image, the tool will display the first frame by default.

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

or if using the Anaconda Python distribution, create a new environment with the dependencies (recommended):
```
conda create --name singlecelltool_env --file requirements.txt
source activate singlecelltool_env
```

Run the application
```
python singlecelltool.py
```

### User input requirements 
* Single cell data file - a spreadsheet containing the single cell information such as cell ID (if available),
image path location, cell coordinates,  and initial label (if available). The CSV or 
excel file should strictly follow the order of column information: cell ID (optional), image path, 
x-coordinate, y-coordinate, and initial label (optional). 

* Phenotype list -  a file containing a list of all possible phenotype or label

* Index minimum - index of the first cell to be included in the analysis. This is optional. By default, 
the minimum is set to 1 which means it will display cells starting from the first item on the input file. 

* Index maximum - index of the last cell to be included in the analysis. This is optional. By default, 
the maximum is set to the total number of cells from the input file.


* Display limit - number of cells to be displayed on a single page. The default is 20.

* Crop size - Pixel size to be used in cropping single cells from the image.
The default is 64.

_Note: For big input files (i.e. more than 1000 cells), it is strongly recommended to break up your analysis
into batches by setting the index minimum and maximum values. It will also be great to assign unique cell IDs
for easy tracking of the single cells_

### Output
The output is a CSV file containing all the labeled single cells.