
import pandas as pd
import numpy as np
import statsmodels.api as sm

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
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA AND CREATE PRODUCT-LEVEL DATASET
# ============================================================

print("=" * 70)
print("OBJECTIVE 1: CATEGORY INTERACTION ANALYSIS")
print("=" * 70)

df = pd.read_csv(DATA_FILE)

products = (
    df.groupby(["parent_asin", "category"])
    .agg(
        n_reviews=("rating", "size"),
        mean_rating=("rating", "mean")
    )
    .reset_index()
)

products["log_review_count"] = np.log1p(
    products["n_reviews"]
)


# ============================================================
# CREATE CATEGORY INDICATORS
# ============================================================

dummies = pd.get_dummies(
    products["category"],
    drop_first=True,
    dtype=float
)

X = pd.concat(
    [
        products[["log_review_count"]],
        dummies
    ],
    axis=1
)

# Create interaction terms
for category in dummies.columns:
    X[f"log_count_x_{category}"] = (
        products["log_review_count"] * dummies[category]
    )

X = sm.add_constant(X)


# ============================================================
# FIT INTERACTION MODEL
# ============================================================

print("\nFitting category interaction regression...")

model = sm.OLS(
    products["mean_rating"],
    X
).fit()

print(model.summary())


# ============================================================
# CALCULATE CATEGORY-SPECIFIC SLOPES
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY-SPECIFIC REGRESSION SLOPES")
print("=" * 70)

base_slope = model.params["log_review_count"]

results = []

results.append({
    "category": "Digital_Music",
    "slope": base_slope
})

for category in dummies.columns:

    interaction_name = f"log_count_x_{category}"

    category_slope = (
        base_slope + model.params[interaction_name]
    )

    results.append({
        "category": category,
        "slope": category_slope
    })

slope_summary = pd.DataFrame(results)

print(slope_summary.to_string(index=False))


# ============================================================
# CATEGORY-WISE REVIEW COUNT GROUP SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY-WISE REVIEW COUNT GROUP SUMMARY")
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
        ["category", "review_count_group"],
        observed=False
    )
    .agg(
        number_of_products=("mean_rating", "count"),
        average_rating=("mean_rating", "mean")
    )
    .reset_index()
)

print(group_summary.to_string(index=False))


# ============================================================
# COMPARE MODELS WITH AND WITHOUT INTERACTIONS
# ============================================================

print("\n" + "=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

# Common-slope model
X_common = pd.concat(
    [
        products[["log_review_count"]],
        dummies
    ],
    axis=1
)

X_common = sm.add_constant(X_common)

common_model = sm.OLS(
    products["mean_rating"],
    X_common
).fit()

comparison = pd.DataFrame({
    "model": [
        "Common category slope",
        "Category-specific slopes"
    ],
    "R_squared": [
        common_model.rsquared,
        model.rsquared
    ],
    "Adjusted_R_squared": [
        common_model.rsquared_adj,
        model.rsquared_adj
    ],
    "Residual_Sum_of_Squares": [
        sum(common_model.resid ** 2),
        sum(model.resid ** 2)
    ]
})

print(comparison.to_string(index=False))


# ============================================================
# JOINT TEST OF INTERACTION COEFFICIENTS
# ============================================================

print("\n" + "=" * 70)
print("JOINT INTERACTION TEST")
print("=" * 70)

interaction_names = [
    f"log_count_x_{category}"
    for category in dummies.columns
]

restriction = ", ".join(
    f"{name} = 0"
    for name in interaction_names
)

interaction_test = model.f_test(restriction)

print(interaction_test)


# ============================================================
# SAVE OUTPUTS
# ============================================================

slope_summary.to_csv(
    REPORT_DIR / "objective1_category_specific_slopes.csv",
    index=False
)

group_summary.to_csv(
    REPORT_DIR / "objective1_category_group_summary.csv",
    index=False
)

comparison.to_csv(
    REPORT_DIR / "objective1_interaction_model_comparison.csv",
    index=False
)

report = []

report.append("OBJECTIVE 1: CATEGORY INTERACTION ANALYSIS")
report.append("=" * 65)

report.append("\nINTERACTION MODEL")
report.append(model.summary().as_text())

report.append("\nCATEGORY-SPECIFIC SLOPES")
report.append(slope_summary.to_string(index=False))

report.append("\nCATEGORY-WISE GROUP SUMMARY")
report.append(group_summary.to_string(index=False))

report.append("\nMODEL COMPARISON")
report.append(comparison.to_string(index=False))

report.append("\nJOINT INTERACTION TEST")
report.append(str(interaction_test))

(
    REPORT_DIR / "objective1_interaction_report.txt"
).write_text(
    "\n".join(report),
    encoding="utf-8"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY INTERACTION ANALYSIS COMPLETED")
print("=" * 70)

print("\nGenerated files:")
print("- objective1_category_specific_slopes.csv")
print("- objective1_category_group_summary.csv")
print("- objective1_interaction_model_comparison.csv")
print("- objective1_interaction_report.txt")

print("\n" + "=" * 70)
