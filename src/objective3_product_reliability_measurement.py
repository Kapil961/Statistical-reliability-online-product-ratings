
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path


# ============================================================
# OBJECTIVE 3: PRODUCT RATING RELIABILITY MEASUREMENT
# ============================================================

print("\n" + "=" * 70)
print("OBJECTIVE 3: PRODUCT RATING RELIABILITY MEASUREMENT")
print("=" * 70)


# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

DATA_PATH = Path("data/processed/amazon_reviews_cleaned.csv")

REPORT_DIR = Path("outputs/reports")
PLOT_DIR = Path("outputs/plots")

REPORT_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------

print("\nLoading cleaned dataset...")

df = pd.read_csv(DATA_PATH)

print("Total reviews:", len(df))
print("Unique products:", df["parent_asin"].nunique())


# ------------------------------------------------------------
# 3. CALCULATE PRODUCT-LEVEL STATISTICS
# ------------------------------------------------------------

print("\nCalculating product-level statistics...")

product_data = (
    df.groupby(["parent_asin", "category"])
    .agg(
        n_reviews=("rating", "count"),
        mean_rating=("rating", "mean"),
        rating_variance=("rating", "var"),
        rating_std=("rating", "std")
    )
    .reset_index()
)

# Standard error is defined for products with at least
# two observed reviews because sample SD is needed.

product_data["standard_error"] = (
    product_data["rating_std"] /
    np.sqrt(product_data["n_reviews"])
)


# ------------------------------------------------------------
# 4. EVIDENCE VOLUME CLASSIFICATION
# ------------------------------------------------------------

def classify_evidence(n):

    if n == 1:
        return "Insufficient"

    elif n <= 9:
        return "Low"

    elif n <= 99:
        return "Moderate"

    elif n <= 999:
        return "High"

    else:
        return "Very High"


product_data["evidence_level"] = (
    product_data["n_reviews"].apply(classify_evidence)
)


# ------------------------------------------------------------
# 5. PRECISION CLASSIFICATION
# ------------------------------------------------------------

def classify_precision(se):

    if pd.isna(se):
        return "Not Available"

    elif se <= 0.05:
        return "Very High"

    elif se <= 0.10:
        return "High"

    elif se <= 0.20:
        return "Moderate"

    else:
        return "Low"


product_data["precision_level"] = (
    product_data["standard_error"].apply(classify_precision)
)


# ------------------------------------------------------------
# 6. CONSISTENCY CLASSIFICATION
# ------------------------------------------------------------

def classify_consistency(sd):

    if pd.isna(sd):
        return "Not Available"

    elif sd <= 0.50:
        return "Very High"

    elif sd <= 0.75:
        return "High"

    elif sd <= 1.00:
        return "Moderate"

    else:
        return "Low"


product_data["consistency_level"] = (
    product_data["rating_std"].apply(classify_consistency)
)


# ------------------------------------------------------------
# 7. SAVE PRODUCT-LEVEL RESULTS
# ------------------------------------------------------------

output_columns = [
    "parent_asin",
    "category",
    "n_reviews",
    "mean_rating",
    "rating_variance",
    "rating_std",
    "standard_error",
    "evidence_level",
    "precision_level",
    "consistency_level"
]

product_data[output_columns].to_csv(
    REPORT_DIR / "objective3_product_reliability.csv",
    index=False
)

print("\nProduct-level results saved.")


# ------------------------------------------------------------
# 8. OVERALL CLASSIFICATION SUMMARY
# ------------------------------------------------------------

print("\nGenerating classification summaries...")

summary_tables = []

classification_columns = [
    "evidence_level",
    "precision_level",
    "consistency_level"
]

for column in classification_columns:

    summary = (
        product_data[column]
        .value_counts(dropna=False)
        .rename_axis("classification")
        .reset_index(name="number_of_products")
    )

    summary["measure"] = column

    summary_tables.append(summary)


overall_summary = pd.concat(
    summary_tables,
    ignore_index=True
)

overall_summary = overall_summary[
    ["measure", "classification", "number_of_products"]
]

overall_summary.to_csv(
    REPORT_DIR / "objective3_reliability_summary.csv",
    index=False
)


# ------------------------------------------------------------
# 9. CATEGORY-WISE RELIABILITY SUMMARY
# ------------------------------------------------------------

category_summary = (
    product_data.groupby("category")
    .agg(
        number_of_products=("parent_asin", "count"),
        average_reviews=("n_reviews", "mean"),
        average_rating=("mean_rating", "mean"),
        average_standard_deviation=("rating_std", "mean"),
        average_standard_error=("standard_error", "mean"),
        median_standard_error=("standard_error", "median")
    )
    .reset_index()
)

category_summary.to_csv(
    REPORT_DIR / "objective3_category_reliability.csv",
    index=False
)


# ------------------------------------------------------------
# 10. PLOT 1: PRECISION DISTRIBUTION
# ------------------------------------------------------------

valid_se = product_data[
    product_data["standard_error"].notna()
]

plt.figure(figsize=(10, 6))

sns.histplot(
    valid_se["standard_error"],
    bins=50,
    kde=True
)

plt.title("Distribution of Product Rating Standard Errors")
plt.xlabel("Standard Error")
plt.ylabel("Number of Products")

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "objective3_precision_distribution.png",
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 11. PLOT 2: RELIABILITY CLASSIFICATIONS
# ------------------------------------------------------------

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

plot_columns = [
    "evidence_level",
    "precision_level",
    "consistency_level"
]

plot_titles = [
    "Evidence Volume",
    "Rating Precision",
    "Rating Consistency"
]

for ax, column, title in zip(
    axes, plot_columns, plot_titles
):

    order = product_data[column].value_counts().index

    sns.countplot(
        data=product_data,
        x=column,
        order=order,
        ax=ax
    )

    ax.set_title(title)
    ax.set_xlabel("Classification")
    ax.set_ylabel("Number of Products")
    ax.tick_params(axis="x", rotation=35)

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "objective3_reliability_categories.png",
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 12. PLOT 3: PRECISION VS CONSISTENCY
# ------------------------------------------------------------

plt.figure(figsize=(10, 7))

sns.scatterplot(
    data=valid_se,
    x="rating_std",
    y="standard_error",
    hue="evidence_level",
    alpha=0.6
)

plt.title("Product Rating Precision vs Consistency")
plt.xlabel("Rating Standard Deviation")
plt.ylabel("Rating Standard Error")

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "objective3_precision_vs_consistency.png",
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# 13. GENERATE TEXT REPORT
# ------------------------------------------------------------

report_path = (
    REPORT_DIR / "objective3_reliability_report.txt"
)

with open(report_path, "w") as file:

    file.write("=" * 70 + "\n")
    file.write("OBJECTIVE 3: PRODUCT RATING RELIABILITY MEASUREMENT\n")
    file.write("=" * 70 + "\n\n")

    file.write(
        f"Total products analyzed: {len(product_data)}\n"
    )

    file.write(
        f"Products with calculable SE: {valid_se.shape[0]}\n"
    )

    file.write(
        f"Products with one review: "
        f"{(product_data['n_reviews'] == 1).sum()}\n\n"
    )

    file.write("OVERALL CLASSIFICATION SUMMARY\n")
    file.write("-" * 70 + "\n")

    file.write(
        overall_summary.to_string(index=False)
    )

    file.write("\n\nCATEGORY-WISE SUMMARY\n")
    file.write("-" * 70 + "\n")

    file.write(
        category_summary.to_string(index=False)
    )

    file.write("\n\nSTATISTICAL INTERPRETATION\n")
    file.write("-" * 70 + "\n")

    file.write(
        "1. Standard error measures the precision of the estimated "
        "product mean rating.\n"
    )

    file.write(
        "2. Standard deviation measures variation among observed "
        "individual ratings.\n"
    )

    file.write(
        "3. Review count represents the amount of available evidence.\n"
    )

    file.write(
        "4. A larger review count generally reduces standard error, "
        "assuming comparable sampling conditions.\n"
    )

    file.write(
        "5. A low standard error does not guarantee unbiased or "
        "representative reviews.\n"
    )

    file.write(
        "6. Classification thresholds are project-defined analytical "
        "choices, not universal statistical standards.\n"
    )

print("\nText report generated.")


# ------------------------------------------------------------
# 14. FINAL OUTPUT
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("OBJECTIVE 3 COMPLETED")
print("=" * 70)

print("\nEvidence Volume:")
print(product_data["evidence_level"].value_counts())

print("\nPrecision:")
print(product_data["precision_level"].value_counts())

print("\nConsistency:")
print(product_data["consistency_level"].value_counts())

print("\nCategory-wise Summary:")
print(category_summary.to_string(index=False))

print("\nGenerated reports:")
print("- objective3_product_reliability.csv")
print("- objective3_reliability_summary.csv")
print("- objective3_category_reliability.csv")
print("- objective3_reliability_report.txt")

print("\nGenerated plots:")
print("- objective3_precision_distribution.png")
print("- objective3_reliability_categories.png")
print("- objective3_precision_vs_consistency.png")

print("\nObjective 3 analysis finished successfully.")
