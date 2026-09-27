# MAT2007 Project - Wine Geogrpahy and Price/Quality Analysis 

---

## Project description 
This project analyzes a large dataset of wine reviews to investigate the relationship between wine quality, price, geographical origin and grape variety.

The main research question is: 
**Which geographical regions and grape varieties offer highly rated wines at relatively low prices?**

The analysis focuses on wine reviews from "Wine Enthusiast" and uses variables such as wine rating(`points`), price (`price`), country (`country`), region (`province` and `region_1`), and grape variety (`variety`). The project intends to investigate geographical patterns in wine quality and price and identify combinations of regions and grape varieties, particularly when showing high ratings compared to their prices. 

---

## Dataset

The dataset was originally from *Wine Enthusiast*. It was downloaded as a **Wine Reviews** dataset available on Kaggle: https://www.kaggle.com/datasets/zynicide/wine-reviews

The dataset contains approximately 130,000 wine reviews and includes information about:

* Country
* Province
* Wine region
* Grape variety
* Winery
* Wine rating (`points`)
* Price (`price`)
* Wine description

The dataset should be downloaded from Kaggle and placed in the project folder before running the analysis.

The main file used by the script is:
`winemag-data-130k-v2.csv` (Consider about the other ones?)


### Data cleaning

The original dataset requires some cleaning before analysis. In particular, the analysis handles missing values in variables required for each specific analysis.

Countries, regions, and grape varieties with very few observations may also be excluded from some comparisons. This prevents conclusions from being based on a very small number of wines.

The original data are not otherwise manually modified. The cleaning and filtering steps are performed within the R script so that the analysis can be reproduced.

---

## Requirements and dependencies

The analysis is written in **R** and can be run using R through Visual Studio Code.

The following R package is required:

* `tidyverse`

If `tidyverse` is not already installed, run:

```r
install.packages("tidyverse")
```

The package can then be loaded with:

```r
library(tidyverse)
```

---

## How to run the code

### 1. Download the dataset

Download the Wine Reviews dataset from Kaggle:

https://www.kaggle.com/datasets/zynicide/wine-reviews

Place `winemag-data-130k-v2.csv` in the same directory as the R script.

The project directory should look approximately like:

```text
wine_project/
├── wine_analysis.R
├── winemag-data-130k-v2.csv
└── figures/
```

### 2. Install the required package (Only has to be done once)

Open R or the VS Code R terminal and run:

```r
install.packages("tidyverse")
```

### 3. Open the project

Open the project folder in Visual Studio Code and open:

`wine_analysis.R`

Make sure the working directory is the project directory containing the CSV file.

### 4. Run the analysis

Run the R script from beginning to end.

The script will:

1. Load the required packages.
2. Import the wine dataset.
3. Inspect and clean the data.
4. Analyse wine prices and ratings.
5. Investigate geographical patterns.
6. Compare grape varieties.
7. Analyse the relationship between wine price and quality.
8. Produce figures used to interpret the results.

---

## Reproducibility

To reproduce the results, the user should download the original dataset from Kaggle and place the CSV file in the project directory using the filename:

`winemag-data-130k-v2.csv`

No manual editing of the dataset is required. All relevant cleaning and filtering steps are performed by the R script.

Because the dataset represents wines reviewed by *Wine Enthusiast* rather than a random sample of all wines available worldwide, the results should be interpreted as patterns within this dataset rather than as definitive rankings of countries, regions, or grape varieties.

