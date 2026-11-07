
import pandas as pd
import numpy as np
import statsmodels.api as sm
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
# LOAD AND AGGREGATE DATA
# ============================================================

print("=" * 70)
print("OBJECTIVE 1: CATEGORY-ADJUSTED REGRESSION")
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

print("\nProducts:", len(products))

print("\nCategory distribution:")
print(products["category"].value_counts())


# ============================================================
# MODEL 1: LOG REVIEW COUNT ONLY
# ============================================================

print("\n" + "=" * 70)
print("MODEL 1: REVIEW COUNT ONLY")
print("=" * 70)

X1 = sm.add_constant(
    products[["log_review_count"]]
)

model1 = sm.OLS(
    products["mean_rating"],
    X1
).fit()

print(model1.summary())


# ============================================================
# MODEL 2: REVIEW COUNT + CATEGORY
# ============================================================

print("\n" + "=" * 70)
print("MODEL 2: REVIEW COUNT + CATEGORY")
print("=" * 70)

category_dummies = pd.get_dummies(
    products["category"],
    drop_first=True,
    dtype=float
)

X2 = pd.concat(
    [
        products[["log_review_count"]],
        category_dummies
    ],
    axis=1
)

X2 = sm.add_constant(X2)

model2 = sm.OLS(
    products["mean_rating"],
    X2
).fit()

print(model2.summary())


# ============================================================
# COMPARE BOTH MODELS
# ============================================================

comparison = pd.DataFrame({
    "Model": [
        "Review count only",
        "Review count + category"
    ],
    "R_squared": [
        model1.rsquared,
        model2.rsquared
    ],
    "Adjusted_R_squared": [
        model1.rsquared_adj,
        model2.rsquared_adj
    ],
    "Review_count_coefficient": [
        model1.params["log_review_count"],
        model2.params["log_review_count"]
    ],
    "Review_count_p_value": [
        model1.pvalues["log_review_count"],
        model2.pvalues["log_review_count"]
    ]
})

print("\n" + "=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

print(comparison.to_string(index=False))


# ============================================================
# CATEGORY-WISE REVIEW COUNT RELATIONSHIP
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY-WISE CORRELATION")
print("=" * 70)

category_results = []

for category, group in products.groupby("category"):

    correlation = group[
        ["n_reviews", "mean_rating"]
    ].corr().iloc[0, 1]

    log_correlation = group[
        ["log_review_count", "mean_rating"]
    ].corr().iloc[0, 1]

    category_results.append({
        "category": category,
        "number_of_products": len(group),
        "correlation_raw_count": correlation,
        "correlation_log_count": log_correlation
    })

category_results = pd.DataFrame(category_results)

print(category_results.to_string(index=False))


# ============================================================
# RESIDUAL DIAGNOSTICS FOR MODEL 2
# ============================================================

print("\n" + "=" * 70)
print("RESIDUAL DIAGNOSTICS")
print("=" * 70)

residuals = model2.resid
fitted = model2.fittedvalues

print("\nResidual mean:", residuals.mean())
print("Residual standard deviation:", residuals.std())

print(
    "\nResidual skewness:",
    residuals.skew()
)

print(
    "Residual kurtosis:",
    residuals.kurtosis()
)


# Residual vs fitted plot

plt.figure(figsize=(10, 6))

plt.scatter(
    fitted,
    residuals,
    alpha=0.2
)

plt.axhline(
    y=0,
    linestyle="--"
)

plt.xlabel("Predicted Product Rating")
plt.ylabel("Regression Residual")

plt.title(
    "Residuals vs Predicted Ratings: Category-Adjusted Model"
)

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    PLOT_DIR / "objective1_category_adjusted_residuals.png",
    dpi=300
)

plt.close()


# ============================================================
# SAVE RESULTS
# ============================================================

comparison.to_csv(
    REPORT_DIR / "objective1_model_comparison.csv",
    index=False
)

category_results.to_csv(
    REPORT_DIR / "objective1_category_correlations.csv",
    index=False
)

report = []

report.append("OBJECTIVE 1: CATEGORY-ADJUSTED REGRESSION")
report.append("=" * 65)

report.append("\nMODEL 1: REVIEW COUNT ONLY")
report.append(model1.summary().as_text())

report.append("\nMODEL 2: REVIEW COUNT + CATEGORY")
report.append(model2.summary().as_text())

report.append("\nMODEL COMPARISON")
report.append(comparison.to_string(index=False))

report.append("\nCATEGORY-WISE CORRELATIONS")
report.append(category_results.to_string(index=False))

report.append("\nRESIDUAL DIAGNOSTICS")
report.append(f"Residual mean: {residuals.mean():.8f}")
report.append(f"Residual SD: {residuals.std():.6f}")
report.append(f"Residual skewness: {residuals.skew():.6f}")
report.append(f"Residual kurtosis: {residuals.kurtosis():.6f}")

report.append(
    "\nNote: Regression association does not establish causation. "
    "Conventional regression inference requires appropriate "
    "error assumptions."
)

(
    REPORT_DIR / "objective1_category_adjusted_report.txt"
).write_text(
    "\n".join(report),
    encoding="utf-8"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY-ADJUSTED ANALYSIS COMPLETED")
print("=" * 70)

print("\nGenerated reports:")
print("- objective1_model_comparison.csv")
print("- objective1_category_correlations.csv")
print("- objective1_category_adjusted_report.txt")

print("\nGenerated plot:")
print("- objective1_category_adjusted_residuals.png")

print("\n" + "=" * 70)
