
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# OBJECTIVE 2: STATISTICAL RELIABILITY OF PRODUCT RATINGS
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
    print("OBJECTIVE 2: STATISTICAL RELIABILITY ANALYSIS")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. LOAD CLEANED DATASET
    # --------------------------------------------------------

    print("\nLoading cleaned dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Total reviews:", len(df))
    print("Unique products:", df["parent_asin"].nunique())

    # --------------------------------------------------------
    # 2. CALCULATE PRODUCT-LEVEL STATISTICS
    # --------------------------------------------------------

    print("\nCalculating product-level statistics...")

    product_data = (
        df.groupby(["parent_asin", "category"])["rating"]
        .agg(
            n_reviews="count",
            mean_rating="mean",
            rating_variance="var",
            rating_std="std"
        )
        .reset_index()
    )

    # Standard error of the sample mean.
    # Sample standard deviation is used.
    product_data["standard_error"] = (
        product_data["rating_std"]
        / np.sqrt(product_data["n_reviews"])
    )

    # Products with one review have undefined sample variance
    # and standard deviation.
    product_data.loc[
        product_data["n_reviews"] == 1,
        ["rating_variance", "rating_std", "standard_error"]
    ] = np.nan

    print("\nProduct-level calculations completed.")

    print("\nFirst five product records:")
    print(product_data.head().to_string(index=False))

    # --------------------------------------------------------
    # 3. REVIEW COUNT GROUPS
    # --------------------------------------------------------

    print("\nCreating review-count groups...")

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
        labels=labels
    )

    # --------------------------------------------------------
    # 4. GROUP-WISE RELIABILITY SUMMARY
    # --------------------------------------------------------

    print("\nCalculating group-wise reliability statistics...")

    group_summary = (
        product_data.groupby(
            "review_count_group",
            observed=False
        )
        .agg(
            number_of_products=("parent_asin", "count"),
            average_rating=("mean_rating", "mean"),
            average_rating_variance=("rating_variance", "mean"),
            average_rating_std=("rating_std", "mean"),
            average_standard_error=("standard_error", "mean"),
            median_standard_error=("standard_error", "median")
        )
        .reset_index()
    )

    print("\n" + "=" * 70)
    print("REVIEW COUNT GROUP RELIABILITY SUMMARY")
    print("=" * 70)

    print(group_summary.to_string(index=False))

    # --------------------------------------------------------
    # 5. SAVE PRODUCT-LEVEL DATA
    # --------------------------------------------------------

    product_data.to_csv(
        REPORT_DIR / "objective2_product_reliability.csv",
        index=False
    )

    group_summary.to_csv(
        REPORT_DIR / "objective2_reliability_group_summary.csv",
        index=False
    )

    # --------------------------------------------------------
    # 6. PLOT: REVIEW COUNT VS STANDARD ERROR
    # --------------------------------------------------------

    valid_data = product_data.dropna(
        subset=["standard_error"]
    )

    plt.figure(figsize=(10, 6))

    plt.scatter(
        valid_data["n_reviews"],
        valid_data["standard_error"],
        alpha=0.25
    )

    plt.xscale("log")
    plt.xlabel("Number of Reviews (log scale)")
    plt.ylabel("Standard Error of Mean Rating")
    plt.title("Review Count vs Standard Error")
    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "objective2_review_count_vs_standard_error.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------------------------
    # 7. PLOT: GROUP-WISE STANDARD ERROR
    # --------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.bar(
        group_summary["review_count_group"].astype(str),
        group_summary["average_standard_error"]
    )

    plt.xlabel("Review Count Group")
    plt.ylabel("Average Standard Error")
    plt.title("Average Standard Error Across Review Groups")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "objective2_group_standard_error.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------------------------
    # 8. GENERATE STATISTICAL REPORT
    # --------------------------------------------------------

    report_path = REPORT_DIR / "objective2_reliability_report.txt"

    with open(report_path, "w") as file:

        file.write(
            "OBJECTIVE 2: STATISTICAL RELIABILITY OF PRODUCT RATINGS\n"
        )

        file.write("=" * 65 + "\n\n")

        file.write(
            f"Total reviews: {len(df)}\n"
        )

        file.write(
            f"Unique products: {product_data.shape[0]}\n\n"
        )

        file.write(
            "GROUP-WISE RELIABILITY SUMMARY\n"
        )

        file.write("=" * 65 + "\n")

        file.write(
            group_summary.to_string(index=False)
        )

        file.write("\n\n")

        file.write(
            "THEORETICAL RELATIONSHIP\n"
        )

        file.write(
            "SE(mean rating) = s / sqrt(n)\n"
        )

        file.write(
            "The standard error generally decreases as sample size increases, "
            "assuming independent observations with finite variance.\n"
        )

        file.write(
            "\nLIMITATIONS\n"
        )

        file.write(
            "Products with one review have undefined sample variance and "
            "sample standard deviation.\n"
        )

        file.write(
            "The standard error formula assumes independent observations. "
            "Repeated reviews may not be independent or representative.\n"
        )

    # --------------------------------------------------------
    # 9. FINAL OUTPUT
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("OBJECTIVE 2 INITIAL ANALYSIS COMPLETED")
    print("=" * 70)

    print("\nGenerated files:")

    print("- objective2_product_reliability.csv")
    print("- objective2_reliability_group_summary.csv")
    print("- objective2_reliability_report.txt")

    print("- objective2_review_count_vs_standard_error.png")
    print("- objective2_group_standard_error.png")

    print("\nAll outputs saved successfully.")


if __name__ == "__main__":
    main()
