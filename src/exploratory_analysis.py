
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path


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
# LOAD CLEANED DATASET
# ============================================================

print("=" * 70)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 70)

df = pd.read_csv(DATA_FILE)

print("\nDataset loaded successfully.")

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# BASIC DATASET INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("1. BASIC DATASET INFORMATION")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)

print("\nData types:")
print(df.dtypes)

print("\nNumber of unique products:")
print(df["parent_asin"].nunique())

print("\nNumber of unique users:")
print(df["user_id"].nunique())

print("\nCategories:")
print(df["category"].value_counts())


# ============================================================
# REVIEW-LEVEL RATING STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("2. REVIEW-LEVEL RATING STATISTICS")
print("=" * 70)

rating_mean = df["rating"].mean()
rating_variance = df["rating"].var()
rating_std = df["rating"].std()

print(f"\nMean rating: {rating_mean:.4f}")
print(f"Rating variance: {rating_variance:.4f}")
print(f"Rating standard deviation: {rating_std:.4f}")

rating_distribution = (
    df["rating"]
    .value_counts()
    .sort_index()
    .rename_axis("rating")
    .reset_index(name="review_count")
)

rating_distribution["percentage"] = (
    rating_distribution["review_count"]
    / len(df)
    * 100
)

print("\nRating distribution:")
print(rating_distribution.to_string(index=False))

rating_distribution.to_csv(
    REPORT_DIR / "rating_distribution.csv",
    index=False
)


# ============================================================
# PRODUCT-LEVEL STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("3. PRODUCT-LEVEL STATISTICS")
print("=" * 70)

product_data = (
    df.groupby("parent_asin")
    .agg(
        category=("category", "first"),
        n_reviews=("rating", "size"),
        mean_rating=("rating", "mean"),
        rating_variance=("rating", "var"),
        rating_std=("rating", "std")
    )
    .reset_index()
)

print("\nProduct-level dataset created.")

print("Number of products:", len(product_data))

print("\nProduct average rating statistics:")
print(product_data["mean_rating"].describe())

print("\nProduct review count statistics:")
print(product_data["n_reviews"].describe())

product_data.to_csv(
    REPORT_DIR / "product_level_summary.csv",
    index=False
)


# ============================================================
# PRODUCT REVIEW COUNT GROUPS
# ============================================================

print("\n" + "=" * 70)
print("4. PRODUCT REVIEW COUNT GROUP ANALYSIS")
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

product_data["review_count_group"] = pd.cut(
    product_data["n_reviews"],
    bins=bins,
    labels=labels,
    right=True
)

group_summary = (
    product_data.groupby(
        "review_count_group",
        observed=False
    )
    .agg(
        number_of_products=("parent_asin", "count"),
        average_product_rating=("mean_rating", "mean"),
        median_product_rating=("mean_rating", "median"),
        standard_deviation=("mean_rating", "std")
    )
    .reset_index()
)

perfect_rating_percentage = (
    product_data.assign(
        perfect_rating=product_data["mean_rating"] == 5
    )
    .groupby("review_count_group", observed=False)
    ["perfect_rating"]
    .mean()
    * 100
)

group_summary["perfect_rating_percentage"] = (
    perfect_rating_percentage.to_numpy()
)

print("\nReview count group summary:")
print(group_summary.to_string(index=False))

group_summary.to_csv(
    REPORT_DIR / "review_count_group_summary.csv",
    index=False
)


# ============================================================
# CATEGORY-WISE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("5. CATEGORY-WISE ANALYSIS")
print("=" * 70)

category_review_summary = (
    df.groupby("category")
    .agg(
        total_reviews=("rating", "size"),
        review_level_mean=("rating", "mean"),
        review_level_std=("rating", "std")
    )
)

category_product_summary = (
    product_data.groupby("category")
    .agg(
        total_products=("parent_asin", "count"),
        product_level_mean=("mean_rating", "mean"),
        product_level_std=("mean_rating", "std")
    )
)

category_summary = category_review_summary.join(
    category_product_summary
).reset_index()

print("\nCategory summary:")
print(category_summary.to_string(index=False))

category_summary.to_csv(
    REPORT_DIR / "category_summary.csv",
    index=False
)


# ============================================================
# GRAPH 1: RATING DISTRIBUTION
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    rating_distribution["rating"],
    rating_distribution["review_count"]
)

plt.title("Distribution of Individual Product Ratings")
plt.xlabel("Star Rating")
plt.ylabel("Number of Reviews")

plt.xticks([1, 2, 3, 4, 5])
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "rating_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 2: PRODUCT REVIEW COUNT DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    product_data["n_reviews"],
    bins=np.logspace(
        0,
        np.log10(product_data["n_reviews"].max()),
        40
    )
)

plt.xscale("log")

plt.title("Distribution of Product Review Counts")
plt.xlabel("Number of Reviews per Product (Log Scale)")
plt.ylabel("Number of Products")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "product_review_count_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 3: PRODUCT AVERAGE RATING BY REVIEW COUNT GROUP
# ============================================================

plt.figure(figsize=(10, 6))

plt.errorbar(
    group_summary["review_count_group"].astype(str),
    group_summary["average_product_rating"],
    yerr=group_summary["standard_deviation"],
    marker="o",
    capsize=5
)

plt.title("Average Product Rating by Review Count Group")
plt.xlabel("Number of Reviews per Product")
plt.ylabel("Average Product Rating")

plt.ylim(1, 5.5)
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "product_rating_by_review_count.png",
    dpi=300
)

plt.close()


# ============================================================
# GRAPH 4: CATEGORY-WISE RATING COMPARISON
# ============================================================

x = np.arange(len(category_summary))
width = 0.35

plt.figure(figsize=(11, 6))

plt.bar(
    x - width / 2,
    category_summary["review_level_mean"],
    width,
    label="Review-Level Mean"
)

plt.bar(
    x + width / 2,
    category_summary["product_level_mean"],
    width,
    label="Product-Level Mean"
)

plt.title("Category-Wise Rating Comparison")
plt.xlabel("Category")
plt.ylabel("Average Rating")

plt.xticks(
    x,
    category_summary["category"],
    rotation=15
)

plt.ylim(0, 5)
plt.legend()
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "category_rating_comparison.png",
    dpi=300
)

plt.close()


# ============================================================
# SAVE EDA SUMMARY REPORT
# ============================================================

summary_lines = [
    "EXPLORATORY DATA ANALYSIS SUMMARY",
    "=" * 65,
    "",
    f"Total reviews: {len(df)}",
    f"Total products: {len(product_data)}",
    f"Total users: {df['user_id'].nunique()}",
    f"Number of categories: {df['category'].nunique()}",
    "",
    f"Overall mean rating: {rating_mean:.4f}",
    f"Overall rating variance: {rating_variance:.4f}",
    f"Overall rating standard deviation: {rating_std:.4f}",
    "",
    "PRODUCT REVIEW COUNT GROUPS",
    "-" * 65,
    group_summary.to_string(index=False),
    "",
    "CATEGORY SUMMARY",
    "-" * 65,
    category_summary.to_string(index=False)
]

(REPORT_DIR / "eda_summary.txt").write_text(
    "\n".join(summary_lines),
    encoding="utf-8"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("EXPLORATORY DATA ANALYSIS COMPLETED")
print("=" * 70)

print("\nGenerated reports:")

for file in sorted(REPORT_DIR.glob("*.csv")):
    print(file.name)

print("\nGenerated graphs:")

for file in sorted(PLOT_DIR.glob("*.png")):
    print(file.name)

print("\nEDA summary saved.")

print("=" * 70)
