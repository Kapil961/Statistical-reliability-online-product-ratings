
import pandas as pd
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_DIR / "data" / "raw" / "amazon_reviews.csv"

CLEAN_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "amazon_reviews_cleaned.csv"
)

REPORT_FILE = (
    PROJECT_DIR
    / "outputs"
    / "reports"
    / "data_validation_summary.txt"
)


# ============================================================
# LOAD ORIGINAL DATASET
# ============================================================

print("=" * 65)
print("AMAZON REVIEWS DATASET CLEANING")
print("=" * 65)

print("\nLoading original dataset...")

df = pd.read_csv(RAW_FILE)

print("Original rows:", len(df))
print("Original columns:", len(df.columns))


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "category",
    "rating",
    "parent_asin",
    "user_id",
    "product_review_count",
    "user_review_count"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns missing: {missing_columns}"
    )

print("\nRequired columns verified.")


# ============================================================
# INITIAL DATASET VALIDATION
# ============================================================

print("\nChecking missing values...")

missing_values = df.isnull().sum()

print(missing_values.to_string())

print("\nChecking exact duplicate rows...")

duplicate_count = df.duplicated().sum()

print("Duplicate rows:", duplicate_count)


# ============================================================
# REMOVE EXACT DUPLICATES
# ============================================================

print("\nRemoving exact duplicate rows...")

clean = df.drop_duplicates().copy()

print("Rows after duplicate removal:", len(clean))

remaining_duplicates = clean.duplicated().sum()

print("Remaining duplicate rows:", remaining_duplicates)


# ============================================================
# RECALCULATE PRODUCT REVIEW COUNTS
# ============================================================

print("\nRecalculating product review counts...")

clean["product_review_count"] = (
    clean.groupby("parent_asin")["parent_asin"]
    .transform("size")
)


# ============================================================
# RECALCULATE USER REVIEW COUNTS
# ============================================================

print("Recalculating user review counts...")

clean["user_review_count"] = (
    clean.groupby("user_id")["user_id"]
    .transform("size")
)


# ============================================================
# VALIDATE RECALCULATED COUNTS
# ============================================================

actual_product_counts = (
    clean.groupby("parent_asin").size()
)

actual_user_counts = (
    clean.groupby("user_id").size()
)

product_count_valid = all(
    clean.groupby("parent_asin")["product_review_count"]
    .nunique() == 1
)

user_count_valid = all(
    clean.groupby("user_id")["user_review_count"]
    .nunique() == 1
)

product_count_matches = (
    clean["product_review_count"].to_numpy()
    ==
    clean["parent_asin"].map(actual_product_counts).to_numpy()
).all()

user_count_matches = (
    clean["user_review_count"].to_numpy()
    ==
    clean["user_id"].map(actual_user_counts).to_numpy()
).all()


# ============================================================
# ADDITIONAL VALIDATION
# ============================================================

print("\nChecking rating values...")

valid_ratings = clean["rating"].isin([1, 2, 3, 4, 5]).all()

print("All ratings between 1 and 5:", valid_ratings)

print("\nChecking category consistency...")

category_counts_per_product = (
    clean.groupby("parent_asin")["category"].nunique()
)

inconsistent_products = (
    category_counts_per_product > 1
).sum()

print(
    "Products associated with multiple categories:",
    inconsistent_products
)


# ============================================================
# SAVE CLEANED DATASET
# ============================================================

print("\nSaving cleaned dataset...")

clean.to_csv(CLEAN_FILE, index=False)

print("Cleaned dataset saved:", CLEAN_FILE)


# ============================================================
# GENERATE VALIDATION REPORT
# ============================================================

REPORT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

summary = [
    "AMAZON REVIEWS DATASET VALIDATION REPORT",
    "=" * 55,
    "",
    f"Original rows: {len(df)}",
    f"Cleaned rows: {len(clean)}",
    f"Removed duplicate rows: {duplicate_count}",
    f"Remaining duplicate rows: {remaining_duplicates}",
    "",
    f"Number of columns: {len(clean.columns)}",
    f"Unique products: {clean['parent_asin'].nunique()}",
    f"Unique users: {clean['user_id'].nunique()}",
    "",
    f"Missing values: {clean.isnull().sum().sum()}",
    f"Valid ratings: {valid_ratings}",
    f"Product count consistency: {product_count_matches}",
    f"User count consistency: {user_count_matches}",
    f"Product count constant within product: {product_count_valid}",
    f"User count constant within user: {user_count_valid}",
    f"Products with multiple categories: {inconsistent_products}",
    "",
    "CATEGORY REVIEW COUNTS",
    "-" * 55,
    clean["category"].value_counts().to_string(),
    "",
    "RATING DISTRIBUTION",
    "-" * 55,
    clean["rating"].value_counts().sort_index().to_string(),
    "",
    "REVIEW DATE RANGE",
    "-" * 55,
    f"Start: {clean['review_date'].min()}",
    f"End: {clean['review_date'].max()}",
]

REPORT_FILE.write_text(
    "\n".join(summary),
    encoding="utf-8"
)


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n" + "=" * 65)
print("DATASET CLEANING COMPLETED")
print("=" * 65)

print("Original rows:", len(df))
print("Cleaned rows:", len(clean))
print("Duplicates removed:", duplicate_count)
print("Unique products:", clean["parent_asin"].nunique())
print("Unique users:", clean["user_id"].nunique())

print("\nProduct counts valid:", product_count_matches)
print("User counts valid:", user_count_matches)
print("Ratings valid:", valid_ratings)

print("\nCleaned file:", CLEAN_FILE)
print("Validation report:", REPORT_FILE)

print("\n" + "=" * 65)
