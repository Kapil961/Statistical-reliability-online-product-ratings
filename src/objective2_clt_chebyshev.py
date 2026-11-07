
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import skew, kurtosis


# ============================================================
# OBJECTIVE 2: CENTRAL LIMIT THEOREM AND CHEBYSHEV INEQUALITY
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

PRODUCT_ID = "B00IX1I3G6"

SAMPLE_SIZES = [5, 10, 30, 50, 100, 500]
SIMULATIONS = 5000
EPSILON = 0.2

RANDOM_SEED = 42


def main():

    print("=" * 70)
    print("OBJECTIVE 2: CLT AND CHEBYSHEV ANALYSIS")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. LOAD PRODUCT RATINGS
    # --------------------------------------------------------

    print("\nLoading product ratings...")

    df = pd.read_csv(DATA_PATH)

    ratings = df.loc[
        df["parent_asin"] == PRODUCT_ID,
        "rating"
    ].to_numpy(dtype=float)

    if len(ratings) == 0:
        raise ValueError("Selected product was not found.")

    population_mean = np.mean(ratings)

    # Treat the observed ratings as an empirical distribution.
    population_variance = np.var(ratings, ddof=0)
    population_std = np.std(ratings, ddof=0)

    print("Product ID:", PRODUCT_ID)
    print("Number of observed reviews:", len(ratings))
    print("Mean rating:", population_mean)
    print("Empirical variance:", population_variance)
    print("Empirical standard deviation:", population_std)

    # --------------------------------------------------------
    # 2. SIMULATE SAMPLE MEANS
    # --------------------------------------------------------

    print("\nRunning repeated sampling simulations...")

    rng = np.random.default_rng(RANDOM_SEED)

    simulation_results = []
    sample_mean_distributions = {}

    for n in SAMPLE_SIZES:

        sample_means = np.empty(SIMULATIONS)

        for i in range(SIMULATIONS):

            sample = rng.choice(
                ratings,
                size=n,
                replace=True
            )

            sample_means[i] = np.mean(sample)

        sample_mean_distributions[n] = sample_means

        theoretical_se = population_std / np.sqrt(n)

        empirical_se = np.std(
            sample_means,
            ddof=1
        )

        simulation_results.append({
            "sample_size": n,
            "simulations": SIMULATIONS,
            "theoretical_mean": population_mean,
            "empirical_mean": np.mean(sample_means),
            "theoretical_standard_error": theoretical_se,
            "empirical_standard_error": empirical_se,
            "skewness": skew(sample_means),
            "excess_kurtosis": kurtosis(sample_means)
        })

    results_df = pd.DataFrame(simulation_results)

    print("\n" + "=" * 70)
    print("CENTRAL LIMIT THEOREM SIMULATION RESULTS")
    print("=" * 70)

    print(results_df.round(5).to_string(index=False))

    # --------------------------------------------------------
    # 3. CHEBYSHEV INEQUALITY
    # --------------------------------------------------------

    print("\nCalculating Chebyshev inequality results...")

    chebyshev_results = []

    for n in SAMPLE_SIZES:

        sample_means = sample_mean_distributions[n]

        observed_probability = np.mean(
            np.abs(sample_means - population_mean) >= EPSILON
        )

        theoretical_bound = (
            population_variance
            / (n * EPSILON ** 2)
        )

        # A probability cannot exceed 1.
        theoretical_bound = min(1.0, theoretical_bound)

        chebyshev_results.append({
            "sample_size": n,
            "epsilon": EPSILON,
            "observed_deviation_probability": observed_probability,
            "chebyshev_upper_bound": theoretical_bound
        })

    chebyshev_df = pd.DataFrame(chebyshev_results)

    print("\n" + "=" * 70)
    print("CHEBYSHEV INEQUALITY RESULTS")
    print("=" * 70)

    print(chebyshev_df.round(5).to_string(index=False))

    # --------------------------------------------------------
    # 4. SAVE RESULTS
    # --------------------------------------------------------

    results_df.to_csv(
        REPORT_DIR / "objective2_clt_simulation.csv",
        index=False
    )

    chebyshev_df.to_csv(
        REPORT_DIR / "objective2_chebyshev_results.csv",
        index=False
    )

    # --------------------------------------------------------
    # 5. PLOT SAMPLE MEAN DISTRIBUTIONS
    # --------------------------------------------------------

    fig, axes = plt.subplots(
        2,
        3,
        figsize=(15, 9)
    )

    for ax, n in zip(axes.flat, SAMPLE_SIZES):

        sample_means = sample_mean_distributions[n]

        ax.hist(
            sample_means,
            bins=30,
            density=True,
            alpha=0.7
        )

        ax.axvline(
            population_mean,
            linestyle="--",
            linewidth=2,
            label="Population mean"
        )

        ax.set_title(f"Sample size n = {n}")
        ax.set_xlabel("Sample mean rating")
        ax.set_ylabel("Density")
        ax.legend()

    fig.suptitle(
        "Central Limit Theorem: Distribution of Sample Means"
    )

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "objective2_clt_sample_mean_distributions.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------------------------
    # 6. PLOT THEORETICAL VS EMPIRICAL STANDARD ERROR
    # --------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        results_df["sample_size"],
        results_df["theoretical_standard_error"],
        marker="o",
        label="Theoretical SE"
    )

    plt.plot(
        results_df["sample_size"],
        results_df["empirical_standard_error"],
        marker="s",
        label="Empirical SE"
    )

    plt.xlabel("Sample size")
    plt.ylabel("Standard deviation of sample means")
    plt.title("Theoretical vs Empirical Standard Error")

    plt.xscale("log")
    plt.grid(alpha=0.3)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "objective2_clt_standard_error_comparison.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------------------------
    # 7. PLOT CHEBYSHEV RESULTS
    # --------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        chebyshev_df["sample_size"],
        chebyshev_df["observed_deviation_probability"],
        marker="o",
        label="Observed probability"
    )

    plt.plot(
        chebyshev_df["sample_size"],
        chebyshev_df["chebyshev_upper_bound"],
        marker="s",
        linestyle="--",
        label="Chebyshev upper bound"
    )

    plt.xlabel("Sample size")
    plt.ylabel("Probability")
    plt.title(
        f"Chebyshev Inequality: Deviation of {EPSILON} Rating Points"
    )

    plt.xscale("log")
    plt.ylim(0, 1.05)
    plt.grid(alpha=0.3)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "objective2_chebyshev_comparison.png",
        dpi=300
    )

    plt.close()

    # --------------------------------------------------------
    # 8. GENERATE TEXT REPORT
    # --------------------------------------------------------

    report_path = REPORT_DIR / "objective2_clt_chebyshev_report.txt"

    with open(report_path, "w") as file:

        file.write(
            "OBJECTIVE 2: CLT AND CHEBYSHEV ANALYSIS\n"
        )

        file.write("=" * 65 + "\n\n")

        file.write(f"Product ID: {PRODUCT_ID}\n")
        file.write(f"Observed reviews: {len(ratings)}\n")
        file.write(f"Empirical mean: {population_mean:.6f}\n")
        file.write(
            f"Empirical variance: {population_variance:.6f}\n"
        )
        file.write(
            f"Empirical standard deviation: {population_std:.6f}\n\n"
        )

        file.write("CLT SIMULATION RESULTS\n")
        file.write("=" * 65 + "\n")

        file.write(results_df.to_string(index=False))

        file.write("\n\nCHEBYSHEV RESULTS\n")
        file.write("=" * 65 + "\n")

        file.write(chebyshev_df.to_string(index=False))

        file.write("\n\nMETHODOLOGY AND LIMITATIONS\n")
        file.write("=" * 65 + "\n")

        file.write(
            "The observed product ratings are treated as an empirical "
            "distribution. Samples are drawn with replacement.\n"
        )

        file.write(
            "The simulation illustrates independent sampling from this "
            "empirical distribution, not the independence or "
            "representativeness of actual customer reviews.\n"
        )

        file.write(
            "The CLT describes the distribution of sample means under "
            "appropriate conditions, including finite variance.\n"
        )

        file.write(
            "Chebyshev's inequality provides an upper bound on the "
            "probability of deviation from the mean.\n"
        )

    # --------------------------------------------------------
    # 9. FINAL OUTPUT
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("CLT AND CHEBYSHEV ANALYSIS COMPLETED")
    print("=" * 70)

    print("\nGenerated reports:")
    print("- objective2_clt_simulation.csv")
    print("- objective2_chebyshev_results.csv")
    print("- objective2_clt_chebyshev_report.txt")

    print("\nGenerated plots:")
    print("- objective2_clt_sample_mean_distributions.png")
    print("- objective2_clt_standard_error_comparison.png")
    print("- objective2_chebyshev_comparison.png")


if __name__ == "__main__":
    main()
