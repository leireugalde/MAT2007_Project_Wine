
#MAT2007 project: which countries offer the best balance between price and quality?

# The code follows the order of the Methods section in the README:
# Data: winemag-data-130k-v2.csv should be saved in
# a folder called "data" next to this script. The three figures are saved in "figures".

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "winemag-data-130k-v2.csv")
FIGURE_FOLDER = os.path.join(BASE_DIR, "figures")

# read only specific columns for the coding
COLUMNS = ["country", "points", "price", "title", "description"]
# if below are not included that wine is discarded
REQUIRED = ["country", "points", "price"]

K = 10              # number of subsamples for SD
SEED = 42           # allows every run to give same results 
MIN_WINES = 200     # amount of wines needed to be included in country comparison
N_SAMPLE = 3000     # number of wines randomly chosen for 1b
PRICE_STEP = 0.2    # width of a price range in log10(price)
SHOW_FIGURES = True

# colours
POSITIVE = "#58c79d"   # green: good value
NEGATIVE = "#ef9cc5"   # pink: poor value
INK = "#2d2d2d"        # line
GREY = "#d9d3cf"
TEXT = "#4b4646"

#information for plot 
plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": GREY,
    "axes.labelcolor": TEXT,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": "#f3efe9",
    "legend.frameon": False,
    "legend.fontsize": 8,
})

# statistics functions
def line_fit(x, y):
    #Least-squares straight line y = a + b * x for all wines
    dx = x - np.mean(x)
    dy = y - np.mean(y)
    b = np.sum(dx * dy) / np.sum(dx ** 2)
    a = np.mean(y) - b * np.mean(x)
    return a, b

def pearson(x, y):
    #Pearson correlation between x and y.
    dx = x - np.mean(x)
    dy = y - np.mean(y)
    return np.sum(dx * dy) / np.sqrt(np.sum(dx ** 2) * np.sum(dy ** 2))

# Data: read and clean
if not os.path.exists(DATA_FILE):
    sys.exit("Data file not found: " + DATA_FILE) #protection 

# usecols --> make sure columns previously named are only used 
wine = pd.read_csv(DATA_FILE, usecols=COLUMNS)
n_read = len(wine)

# Remove wines without a country, points or price
wine = wine.dropna(subset=REQUIRED)
n_complete = len(wine)

# removes duplicates indicated by the title and description
wine = wine.drop_duplicates(subset=["title", "description"])
n_kept = len(wine)
wine = wine.reset_index(drop=True)

print()
print("Rows read:               ", n_read)
print("Removed (missing values):", n_read - n_complete)
print("Removed (duplicates):    ", n_complete - n_kept)
print("Wines kept:              ", n_kept, f"({100 * n_kept / n_read:.1f} %)")
# print information to know how much data is kept 

#calculate log of price --> convert into linear due to skewness
wine["log_price"] = np.log10(wine["price"])

#line for all wines 
a, b = line_fit(wine["log_price"].to_numpy(), wine["points"].to_numpy())

print()
print(f"Line through all wines: expected points = {a:.2f} + {b:.2f} * log10(price)")
# b is the number of extra points for 10x the price; log10(2) = 0.30, so
# doubling the price gives b * 0.30 extra points
print(f"  10x the price buys {b:.2f} points, doubling the price {b * np.log10(2):.2f} points")
for price in [10, 20, 50, 100]:
    print(f"  a ${price} wine is expected to score {a + b * np.log10(price):.1f} points")


# value score = actual points - expected points
#   > 0: the wine is rated higher than other wines of the same price (good value)
#   < 0: the wine is rated lower than expected for its price (overpriced)
wine["expected_points"] = a + b * wine["log_price"]
wine["value"] = wine["points"] - wine["expected_points"]

n_above = int((wine["value"] > 0).sum())
print(f"  {100 * n_above / n_kept:.0f} % of the wines lie above the line")


# pearson correlation
# r = how strongly log(price) and points go together (-1 to 1)
# r^2 = share of the differences in points that is explained by price
r = pearson(wine["log_price"].to_numpy(), wine["points"].to_numpy())
print()
print(f"Pearson r = {r:.3f}, r^2 = {r ** 2:.2f}: "
      f"price explains {100 * r ** 2:.0f} % of the differences in points")


# grouping per countries 
QUANTITIES = ["mean points", "median price", "pearson", "points per 10x price", "value score"]

# use median instead of mean, because mean is pulled by very expensive bottles, median is not 
def calculate(group):

    a_group, b_group = line_fit(group["log_price"].to_numpy(), group["points"].to_numpy())
    return {
        "mean points": np.mean(group["points"]),
        "median price": np.median(group["price"]),
        "pearson": pearson(group["log_price"].to_numpy(), group["points"].to_numpy()),
        "points per 10x price": b_group,
        "value score": np.mean(group["value"]),     # average value score of the group
    }


# Only countries with at least MIN_WINES wines
countries = [] #begin with empty 
for country in wine["country"].unique():
    if (wine["country"] == country).sum() >= MIN_WINES:
        countries.append(country)
print()
print(len(countries), "of", wine["country"].nunique(), "countries have at least",
      MIN_WINES, "wines")


# uncertainties from subsamples 
rng = np.random.default_rng(SEED) #shuffling values 
wine["subsample"] = rng.permutation(n_kept) % K

def calculate_with_uncertainty(group):

    result = calculate(group)

    # loop 1: calculate all results in each subsample
    sub_results = []
    for k in range(K):
        part = group[group["subsample"] == k]
        sub_results.append(calculate(part))

    # loop 2: for each quantity, collect the K values and take their SD
    # (ddof=1: sample standard deviation, divides by K - 1)
    uncertainty = {}
    for quantity in QUANTITIES:
        sub_values = []
        for k in range(K):
            sub_values.append(sub_results[k][quantity])
        uncertainty[quantity] = np.std(sub_values, ddof=1)

    return result, uncertainty


# all wines together
result, uncertainty = calculate_with_uncertainty(wine)
print()
print("Results for all wines (value ± SD of the 10 subsamples):")
for quantity in QUANTITIES:
    if quantity != "value score":       # the value score is 0 for all wines together
        print(f"  {quantity:<22} {result[quantity]:8.3f} ± {uncertainty[quantity]:.3f}")

# every country (the same function, all countries treated the same way)
rows = []
for country in countries:
    group = wine[wine["country"] == country]
    result, uncertainty = calculate_with_uncertainty(group)
    row = {"country": country, "n": len(group)}
    for quantity in QUANTITIES:
        row[quantity] = result[quantity]
        row[quantity + " unc"] = uncertainty[quantity]
    rows.append(row)

table = pd.DataFrame(rows).sort_values("value score", ascending=False)
table = table.reset_index(drop=True)

print()
print(f"Results per country (at least {MIN_WINES} wines, best value first):")
print(f"{'country':<15}{'n':>7}{'value score':>16}{'mean points':>16}{'median $':>14}")
for i in range(len(table)):
    row = table.iloc[i]
    print(f"{row['country']:<15}{row['n']:>7}"
          f"{row['value score']:>9.2f} ± {row['value score unc']:.2f}"
          f"{row['mean points']:>9.2f} ± {row['mean points unc']:.2f}"
          f"{row['median price']:>8.1f} ± {row['median price unc']:.1f}")


# instructions for figures 
os.makedirs(FIGURE_FOLDER, exist_ok=True)

def save_figure(fig, filename):
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURE_FOLDER, filename), bbox_inches="tight")
    if SHOW_FIGURES:
        plt.show()
    else:
        plt.close(fig)

def price_range_averages(data): #split prices into ranges of equal width, showing averages 
    
    edges = np.arange(np.floor(data["log_price"].min() * 5) / 5,
                      data["log_price"].max() + PRICE_STEP, PRICE_STEP)
    middle_prices = []
    means = []
    sds = []
    for i in range(len(edges) - 1):
        in_range = data[(data["log_price"] >= edges[i]) & (data["log_price"] < edges[i + 1])]
        if len(in_range) < 50:          # too few wines for a reliable average
            continue
        middle_prices.append(10 ** ((edges[i] + edges[i + 1]) / 2))
        means.append(np.mean(in_range["points"]))
        sds.append(np.std(in_range["points"], ddof=1))
    return middle_prices, means, sds


def value_line_plot(dots, title, filename, dot_size, dot_alpha, averages=None):
    jitter = np.random.default_rng(0).uniform(-0.3, 0.3, len(dots))
    above = (dots["value"] > 0).to_numpy()
    below = np.logical_not(above)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.scatter(dots["price"][above], dots["points"][above] + jitter[above],
               s=dot_size, alpha=dot_alpha, color=POSITIVE, linewidths=0, rasterized=True)
    ax.scatter(dots["price"][below], dots["points"][below] + jitter[below],
               s=dot_size, alpha=dot_alpha, color=NEGATIVE, linewidths=0, rasterized=True)

    # the fitted line drawn over the whole price range
    prices = np.logspace(np.log10(wine["price"].min()), np.log10(wine["price"].max()), 100)
    ax.plot(prices, a + b * np.log10(prices), color=INK, linewidth=2.2)

    if averages is not None:
        middle_prices, means, sds = averages
        ax.errorbar(middle_prices, means, yerr=sds, fmt="o", color=INK,
                    markerfacecolor="white", markersize=6, capsize=3, zorder=5,
                    label="average points per price range (± SD)")

    # empty plots for the legend
    ax.scatter([], [], s=15, color=POSITIVE,
               label=f"above the line: good value ({100 * n_above / n_kept:.0f} % of wines)")
    ax.scatter([], [], s=15, color=NEGATIVE,
               label=f"below the line: overpriced ({100 - 100 * n_above / n_kept:.0f} % of wines)")
    ax.plot([], [], color=INK, linewidth=2,
            label=f"expected points = {a:.1f} + {b:.2f} · log10(price)")

    ax.set_xscale("log")      # log scale the same as in the fit
    ax.set_xlabel("price ($, log scale)")
    ax.set_ylabel("points")
    ax.set_title(title, loc="left")
    ax.legend(loc="upper left")
    save_figure(fig, filename)


# Figure 1a: all wines
value_line_plot(wine, "Price vs points, all wines",
                "fig1a_value_line_all_wines.png", dot_size=2, dot_alpha=0.06)

# Figure 1b: random 3000 random wines drawn for better visualization
# The line and the averages are still calculated from all wines 
sample = wine.sample(N_SAMPLE, random_state=SEED)
value_line_plot(sample, f"Price vs points: {N_SAMPLE} random wines + averages",
                "fig1b_value_line_averages.png", dot_size=8, dot_alpha=0.35,
                averages=price_range_averages(wine))

# Figure 2: value score per country with its uncertainty (SD of the subsamples)
# table is reversed for the figure 
# If  error bars of two countries do not overlap, difference is real
fig, ax = plt.subplots(figsize=(7, 0.32 * len(table) + 1.2))
reversed_table = table.iloc[::-1]
for i in range(len(reversed_table)):
    row = reversed_table.iloc[i]
    if row["value score"] >= 0:
        colour = POSITIVE
    else:
        colour = NEGATIVE
    ax.errorbar(row["value score"], i, xerr=row["value score unc"], fmt="o",
                color=colour, markersize=6, capsize=3, linewidth=1.5)
ax.axvline(0, color=GREY, linewidth=1.5)      # 0 = the average wine
ax.set_yticks(range(len(reversed_table)))
ax.set_yticklabels(reversed_table["country"])
ax.grid(axis="y", visible=False)
ax.set_xlabel("value score (points above / below expected for the price)")
ax.set_title("Value score per country (± SD)", loc="left")
save_figure(fig, "fig2_value_by_country.png")

print()
print("Figures saved in", FIGURE_FOLDER)