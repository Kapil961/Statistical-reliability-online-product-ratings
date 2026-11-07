
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from scipy.stats import pearsonr
import statsmodels.api as sm


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "amazon_reviews_cleaned.csv"
)

REPORT_DIR = PROJECT_DIR / "outputs" / "reports"
PLOT_DIR = PROJECT_DIR / "outputs" / "plots"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 70)
print("OBJECTIVE 1: REVIEW COUNT VS PRODUCT RATING")
print("=" * 70)

df = pd.read_csv(DATA_FILE)

print("\nDataset loaded successfully.")
print("Total reviews:", len(df))


# ============================================================
# CREATE PRODUCT-LEVEL DATASET
# ============================================================

print("\nCreating product-level dataset...")

products = (
    df.groupby(["parent_asin", "category"])
    .agg(
        n_reviews=("rating", "size"),
        mean_rating=("rating", "mean"),
        rating_variance=("rating", "var"),
        rating_std=("rating", "std")
    )
    .reset_index()
)

print("Total products:", len(products))


# ============================================================
# DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("1. DESCRIPTIVE STATISTICS")
print("=" * 70)

print("\nReview count statistics:")
print(products["n_reviews"].describe())

print("\nAverage product rating statistics:")
print(products["mean_rating"].describe())

print("\nOverall average product rating:")
print(round(products["mean_rating"].mean(), 4))


# ============================================================
# PEARSON CORRELATION
# ============================================================

print("\n" + "=" * 70)
print("2. PEARSON CORRELATION")
print("=" * 70)

x = products["n_reviews"]
y = products["mean_rating"]

correlation, p_value = pearsonr(x, y)

print("\nPearson correlation coefficient:", round(correlation, 5))
print("P-value:", p_value)

if correlation < 0:
    print("Direction: Negative relationship")
elif correlation > 0:
    print("Direction: Positive relationship")
else:
    print("Direction: No linear relationship")


# ============================================================
# SIMPLE LINEAR REGRESSION
# ============================================================

print("\n" + "=" * 70)
print("3. SIMPLE LINEAR REGRESSION")
print("=" * 70)

X = sm.add_constant(x)

model = sm.OLS(y, X).fit()

print(model.summary())


# ============================================================
# LOG-TRANSFORMED REVIEW COUNT REGRESSION
# ============================================================

print("\n" + "=" * 70)
print("4. REGRESSION USING LOG(1 + REVIEW COUNT)")
print("=" * 70)

products["log_review_count"] = np.log1p(
    products["n_reviews"]
)

X_log = sm.add_constant(
    products["log_review_count"]
)

log_model = sm.OLS(y, X_log).fit()

print(log_model.summary())


# ============================================================
# REVIEW COUNT GROUP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("5. REVIEW COUNT GROUP COMPARISON")
print("=" * 70)

bins = [0, 1, 4, 9, 29, 99, 999, np.inf]

labels = [
    "1",
    "2-4",
    "5-9",
    "10-29",
    "30-99",
    "100-999",
    "1000+"
]

products["review_count_group"] = pd.cut(
    products["n_reviews"],
    bins=bins,
    labels=labels
)

group_summary = (
    products.groupby(
        "review_count_group",
        observed=False
    )
    .agg(
        number_of_products=("mean_rating", "count"),
        average_rating=("mean_rating", "mean"),
        median_rating=("mean_rating", "median"),
        rating_std=("mean_rating", "std")
    )
    .reset_index()
)

print(group_summary.to_string(index=False))


# ============================================================
# SAVE RESULTS
# ============================================================

products.to_csv(
    REPORT_DIR / "objective1_product_data.csv",
    index=False
)

group_summary.to_csv(
    REPORT_DIR / "objective1_group_summary.csv",
    index=False
)


# ============================================================
# VISUALIZATION 1: REVIEW COUNT VS RATING
# ============================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    products["n_reviews"],
    products["mean_rating"],
    alpha=0.25
)

plt.xscale("log")

plt.xlabel("Number of Reviews (log scale)")
plt.ylabel("Average Product Rating")

plt.title(
    "Relationship Between Product Review Count and Average Rating"
)

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "objective1_review_count_vs_rating.png",
    dpi=300
)

plt.close()


# ============================================================
# VISUALIZATION 2: LOG-TRANSFORMED REGRESSION
# ============================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    products["log_review_count"],
    products["mean_rating"],
    alpha=0.25
)

sorted_products = products.sort_values(
    "log_review_count"
)

predicted = log_model.predict(
    sm.add_constant(
        sorted_products["log_review_count"]
    )
)

plt.plot(
    sorted_products["log_review_count"],
    predicted,
    linewidth=2
)

plt.xlabel("Log(1 + Number of Reviews)")
plt.ylabel("Average Product Rating")

plt.title(
    "Linear Regression: Log Review Count vs Product Rating"
)

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "objective1_log_regression.png",
    dpi=300
)

plt.close()


# ============================================================
# SAVE STATISTICAL REPORT
# ============================================================

report = []

report.append("OBJECTIVE 1: REVIEW COUNT VS PRODUCT RATING")
report.append("=" * 65)

report.append(f"\nTotal products: {len(products)}")

report.append(
    f"\nPearson correlation: {correlation:.6f}"
)

report.append(
    f"Correlation p-value: {p_value:.8g}"
)

report.append("\nORIGINAL-SCALE REGRESSION")
report.append("-" * 65)
report.append(model.summary().as_text())

report.append("\nLOG-TRANSFORMED REGRESSION")
report.append("-" * 65)
report.append(log_model.summary().as_text())

report.append("\nREVIEW COUNT GROUP SUMMARY")
report.append("-" * 65)
report.append(group_summary.to_string(index=False))

report.append("\nINTERPRETATION")
report.append("-" * 65)

if correlation < 0:
    report.append(
        "The observed Pearson correlation is negative."
    )
elif correlation > 0:
    report.append(
        "The observed Pearson correlation is positive."
    )
else:
    report.append(
        "The observed Pearson correlation is zero."
    )

report.append(
    "Correlation and regression describe association, "
    "not causation."
)

(REPORT_DIR / "objective1_statistical_report.txt").write_text(
    "\n".join(report),
    encoding="utf-8"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("OBJECTIVE 1 ANALYSIS COMPLETED")
print("=" * 70)

print("\nGenerated reports:")
print("- objective1_product_data.csv")
print("- objective1_group_summary.csv")
print("- objective1_statistical_report.txt")

print("\nGenerated plots:")
print("- objective1_review_count_vs_rating.png")
print("- objective1_log_regression.png")

print("\n" + "=" * 70)
