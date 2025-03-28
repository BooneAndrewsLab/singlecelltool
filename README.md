# singlecelltool
Custom-made graphical user interface (GUI) application that allows users to view and 
label single cell images on a grid layout. Users can save a phenotype for each cell 
and then export the data.

This tool is used in the paper: "Systematic genetics and single-cell imaging reveal 
widespread morphological pleiotropy and cell-to-cell variability"

_Mojca Mattiazzi Usaj, Nil Sahin, Helena Friesen, Carles Pons, Matej Usaj,
 Myra Paz Masinas, Ermira Shuteriqi, Aleksei Shkurin, Patrick Aloy, Quaid Morris, 
 Charles Boone, and Brenda J. Andrews_
 
Note: If input is a multi-frame image, the tool will display the first frame by default.

### OS compatibility
Tested on: Linux, macOS, Windows


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
* **Single cell data file** - a spreadsheet containing the single cell information such as cell ID (if available),
image path location, cell coordinates,  and initial label (if available). The CSV or 
excel file should strictly follow the order of column information: cell ID (optional), image path, 
x-coordinate, y-coordinate, and initial label (optional). 

* **Phenotype list** -  a file containing a list of all possible phenotype or label

* **Index minimum** - index of the first cell to be included in the analysis. This is optional. By default, 
the minimum is set to 1 which means it will display cells starting from the first item on the input file. 

* **Index maximum** - index of the last cell to be included in the analysis. This is optional. By default, 
the maximum is set to the total number of cells from the input file.

* **Display limit** - number of cells to be displayed on a single page. The default is 20.

* **Crop size** - Pixel size to be used in cropping single cells from the image.
The default is 64.

* **Brightness** - Brightness setting. The minimum and default value is 1. If the cell crops look dark, try 
increasing the brightness to 2 or 3 and so on.

* **Channel** - Specify which channel(s) to view. Must be comma-separated if multi-channel. The default is 1.

* **Channel tint** - Apply tint(s): Green, Red or Blue. Must be comma-separated if multi-channel. The default is 
grayscale (single-channel) and GRB (multi-channel).

* **Pixel minimum** - Set the minimum displayed pixel intensity value. This is optional. Along with the "Pixel maximum" 
value, this allows you to choose how to scale and display the range of gray levels in an image. This is a similar 
to ImageJ's "Set Display Range" function.

* **Pixel maximum** - Set the maximum displayed pixel intensity value. This is optional. Along with the "Pixel minimum" 
value, this allows you to choose how to scale and display the range of gray levels in an image. This is a similar 
to ImageJ's "Set Display Range" function.

* **Cell ID** - Check this box if 'Cell ID' information is included in the input file.

* **Dark Mode** - Check this box to enable Dark Mode.

_Note: For big input files (i.e. more than 1000 cells), it is strongly recommended to break up your analysis
into batches by setting the index minimum and maximum values. It will also be great to assign unique cell IDs
for easy tracking of the single cells_

### Output
The output is a CSV file containing all the labeled single cells.