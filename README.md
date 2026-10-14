# MAT2007 Project - Wine Geogrpahy and Price/Quality Analysis 

---

## Project description 
This project analyzes a large dataset of wine reviews to find out where you can get the best quality wine for your money. 

The main research question is: 
**What wine producing countries (and regions) offer the best balance between price and quality?**

Each wine is comapred to other wines at that same price. A wine that is rated higher than the expected for its specific price, is considered a wine with a good value. Finding the average of the value score for each country, shows which are the best places to look for good value wine.  

---

## Dataset

The dataset was originally from *Wine Enthusiast Magazine*. It was downloaded as a **Wine Reviews** dataset available on Kaggle: https://www.kaggle.com/datasets/zynicide/wine-reviews

The Kaggle offers three files, but this project only uses the following, as it had the most updated data with less duplicates. 

`winemag-data-130k-v2.csv`

*One of the other files was simply the one above in a different format, and the was an older version of this document* 

The dataset contains approximately 130,000 wine reviews had 14 columns. Only the followig columns were used:
* Wine rating (`points`)
* Price of one bottle in US$ (`price`)
* Country (`country`)
* Winery (`winery`)
* Title and description (`title`and `description`) 

The dataset should be downloaded from Kaggle and placed in the project folder before running the analysis.

### Data cleaning

None of the data has to be cleaned manually. Download the CSV file and run it as it is. All of the cleaning is done by the script. 

* Only columns above are read from the file 
* Wines without a `price`, `points` and `country` are removed
* Duplicate reviews are removed (with help of `title`and `description`)
* Countries with less than 200 wines are not included in the comparison, so conlcusions are based on larger and more representative datasets.

---

## Methods 
### Overview 
Read data --> clean --> log10(price) --> fit one line --> value score --> group by country + uncertainty from 10 subsamples (SD)

### Steps 
| Step | Script | Why |
|---|---|--|
| 1. Log of price | uses `log10(price)`instead of normal price | Prices are very skewed by very expensive bottles. Making this a log scale makes the relationship linear. |
| 2. Expected rating | fit one line through all wines `expected points = a + b*log10(price)  | Give a rating of what a wine at a specific price should have. |
| 3. Value score | `value score = actual points - expected points` for every wine  | Positive value = good value, negative value = overpriced |
| 4. Pearson  r | used to find correlation between `log10(price)` and `points | Show how strongly r and price rating go together |
| 5. Grouping | mean value score and median value per country (min 200 wines) | Helps answer the research question |
| 6. Uncertainty | repeats each calulation in 10 random subsamples , SD is error bars | Show how much a result would change. |


##Continue ratio, uncertainty, line fit 
look for what is output in output section 


## Requirements and extensions 

* Python 3
* VS code with python extension
* Python packages: numpy, pandas, matplotlib
    * Install the packages once in the VS code terminal      

## How to run the code

1. Download the Wine Reviews dataset from Kaggle:
   https://www.kaggle.com/datasets/zynicide/wine-reviews
2. Set up the project folder
   - Place `winemag-data-130k-v2.csv` in the same folder as the python script.
3. Install packages: numpy, matplotlib, pandas
4. Run script `wine_maincode.py` as run python file
   - It is very important that the script is run from the project folder so it can find `winemag-data-130k-v2.csv`
5. The script will take some time to run and code 

## What does the script do 
- Cleans data
- Creates expected rating line with all cleaned data
- Fits expected rating line and calculates value score for each wine
- Does this again but with 3000 random wines to find the averages and better visualisation
- Splits wine into 10 random subsamples to calculate uncertainties
- Calculate results for all wines per country
- Plots and saves figures 

---

## Output 


## Reproducibility

To reproduce the results, the user should download the original dataset from Kaggle and place the CSV file in the project directory using the filename:

`winemag-data-130k-v2.csv`

No manual editing of the dataset is required. All relevant cleaning and filtering steps are performed by the R script.

Because the dataset represents wines reviewed by *Wine Enthusiast* rather than a random sample of all wines available worldwide, the results should be interpreted as patterns within this dataset rather than as definitive rankings of countries, regions, or grape varieties.

