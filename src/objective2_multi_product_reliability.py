
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# OBJECTIVE 2: MULTI-PRODUCT RELIABILITY ANALYSIS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "amazon_reviews_cleaned.csv"
)

REPORT_DIR = PROJECT_ROOT / "outputs" / "reports"
PLOT_DIR = PROJECT_ROOT / "outputs" / "plots"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    print("=" * 70)
    print("OBJECTIVE 2: MULTI-PRODUCT RELIABILITY ANALYSIS")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. LOAD DATA
    # --------------------------------------------------------

    print("\nLoading cleaned dataset...")

    df = pd.read_csv(DATA_PATH)

    # --------------------------------------------------------
    # 2. CALCULATE PRODUCT-LEVEL STATISTICS
    # --------------------------------------------------------

    print("\nCalculating product-level statistics...")

    products = (
        df.groupby(["parent_asin", "category"])["rating"]
        .agg(
            n_reviews="count",
            mean_rating="mean",
            rating_variance="var",
            rating_std="std"
        )
        .reset_index()
    )

    products["standard_error"] = (
        products["rating_std"]
        / np.sqrt(products["n_reviews"])
    )

    # --------------------------------------------------------
    # 3. CALCULATE POOLED REVIEW-LEVEL VARIANCE
    # --------------------------------------------------------

    pooled_variance = df["rating"].var(ddof=1)
    pooled_std = np.sqrt(pooled_variance)

    print("\nPooled review-level variance:", pooled_variance)
    print("Pooled review-level standard deviation:", pooled_std)

    # --------------------------------------------------------
    # 4. CALCULATE THEORETICAL STANDARD ERROR
    # --------------------------------------------------------

    products["theoretical_standard_error"] = (
        pooled_std / np.sqrt(products["n_reviews"])
    )

    # --------------------------------------------------------
    # 5. CREATE REVIEW COUNT GROUPS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 6. GROUP-WISE COMPARISON
    # --------------------------------------------------------

    print("\nCalculating group-wise comparisons...")

    summary = (
        products.groupby(
            "review_count_group",
            observed=False
        )
        .agg(
            number_of_products=("parent_asin", "count"),
            average_review_count=("n_reviews", "mean"),
            average_rating=("mean_rating", "mean"),
            average_observed_variance=("rating_variance", "mean"),
            average_observed_std=("rating_std", "mean"),
            average_observed_se=("standard_error", "mean"),
            average_theoretical_se=(
                "theoretical_standard_error", "mean"
            )
        )
        .reset_index()
    )

    print("\n" + "=" * 70)
    print("MULTI-PRODUCT RELIABILITY COMPARISON")
    print("=" * 70)

    print(summary.round(5).to_string(index=False))

    # --------------------------------------------------------
    # 7. SAVE PRODUCT-LEVEL AND GROUP-LEVEL RESULTS
    # --------------------------------------------------------

    products.to_csv(
        REPORT_DIR / "objective2_multi_product_data.csv",
        index=False
    )

    summary.to_csv(
        REPORT_DIR / "objective2_multi_product_summary.csv",
        index=False
    )

    # --------------------------------------------------------
    # 8. PLOT OBSERVED VS THEORETICAL STANDARD ERROR
    # --------------------------------------------------------

    valid_summary = summary.dropna(
        subset=[
            "average_observed_se",
            "average_theoretical_se"
        ]
    )

    x = np.arange(len(valid_summary))
    width = 0.35

    plt.figure(figsize=(11, 6))

    plt.bar(
        x - width / 2,
        valid_summary["average_observed_se"],
        width,
        label="Observed average SE"
    )

    plt.bar(
        x + width / 2,
        valid_summary["average_theoretical_se"],
        width,
        label="Theoretical SE using pooled SD"
    )

    plt.xticks(
        x,
        valid_summary["review_count_group"].astype(str)
    )

    plt.xlabel("Review Count Group")
    plt.ylabel("Standard Error")
    plt.title("Observed vs Theoretical Standard Error")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "objective2_multi_product_se_comparison.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------------------------
    # 9. PLOT REVIEW COUNT VS OBSERVED STANDARD ERROR
    # --------------------------------------------------------

    valid_products = products.dropna(
        subset=["standard_error"]
    )

    plt.figure(figsize=(10, 6))

    plt.scatter(
        valid_products["n_reviews"],
        valid_products["standard_error"],
        alpha=0.25
    )

    plt.xscale("log")
    plt.xlabel("Number of Reviews (log scale)")
    plt.ylabel("Observed Standard Error")
    plt.title("Product Review Count vs Standard Error")
    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "objective2_multi_product_scatter.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------------------------
    # 10. GENERATE REPORT
    # --------------------------------------------------------

    report_path = (
        REPORT_DIR / "objective2_multi_product_report.txt"
    )

    with open(report_path, "w") as file:

        file.write(
            "OBJECTIVE 2: MULTI-PRODUCT RELIABILITY ANALYSIS\n"
        )

        file.write("=" * 65 + "\n\n")

        file.write(
            f"Total reviews: {len(df)}\n"
        )

        file.write(
            f"Unique products: {len(products)}\n"
        )

        file.write(
            f"Pooled rating variance: {pooled_variance:.6f}\n"
        )

        file.write(
            f"Pooled rating standard deviation: {pooled_std:.6f}\n\n"
        )

        file.write(
            "GROUP-WISE RELIABILITY COMPARISON\n"
        )

        file.write("=" * 65 + "\n")

        file.write(
            summary.to_string(index=False)
        )

        file.write("\n\nMETHODOLOGICAL LIMITATIONS\n")
        file.write("=" * 65 + "\n")

        file.write(
            "The pooled standard deviation is used as a common "
            "reference for theoretical standard errors. Actual "
            "products may have different rating variances.\n"
        )

        file.write(
            "Products with one review have undefined sample "
            "variance and sample standard deviation.\n"
        )

        file.write(
            "The standard error formula assumes independent "
            "observations. Actual customer reviews may not "
            "satisfy this assumption.\n"
        )

    # --------------------------------------------------------
    # 11. FINAL OUTPUT
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("MULTI-PRODUCT RELIABILITY ANALYSIS COMPLETED")
    print("=" * 70)

    print("\nGenerated reports:")
    print("- objective2_multi_product_data.csv")
    print("- objective2_multi_product_summary.csv")
    print("- objective2_multi_product_report.txt")

    print("\nGenerated plots:")
    print("- objective2_multi_product_se_comparison.png")
    print("- objective2_multi_product_scatter.png")


if __name__ == "__main__":
    main()
