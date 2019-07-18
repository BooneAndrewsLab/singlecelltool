# singlecelltool
Custom-made graphical user interface (GUI) application that allows users to view and 
label single cell images on a grid layout. Users can save a phenotype for each cell 
and then export the data.

This tool is used in the paper: "Exploring endocytic compartment morphology with 
systematic genetics and single cell image analysis"

_Mojca Mattiazzi Usaj, Nil Sahin, Helena Friesen, Carles Pons, Matej Usaj,
 Myra Paz Masinas, Ermira Shuteriqi, Aleksei Shkurin, Patrick Aloy, Quaid Morris, 
 Charles Boone, and Brenda J. Andrews_
 

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