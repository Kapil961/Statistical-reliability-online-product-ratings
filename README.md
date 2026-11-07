# Statistical Reliability of Online Product Ratings

## Project Overview

This project investigates the statistical reliability of online product ratings using the **Amazon Reviews 2023** dataset.

It applies statistical methods to examine how review volume, rating variation, and sample size affect the interpretation and precision of product ratings.

The project explores whether a product's average rating provides meaningful information when the number of customer reviews and the variation among those reviews differ.

## Project Objectives

This project has exactly three objectives.

### Objective 1: Relationship Between Review Count and Product Rating

Investigate the relationship between the number of customer reviews and the average product rating.

**Statistical methods:**
- Pearson correlation coefficient
- Simple linear regression
- Log-transformed regression
- Multiple linear regression with category indicators
- Regression interaction analysis
- Residual diagnostics

### Objective 2: Statistical Reliability of Product Ratings

Study how sample size affects the precision of estimated product ratings.

**Statistical methods:**
- Mean, variance, and standard deviation
- Standard error of the sample mean
- Central Limit Theorem (CLT)
- Chebyshev's inequality
- Simulation of sample means
- Comparison of theoretical and empirical standard errors

### Objective 3: Product Rating Reliability Measurement

Evaluate product ratings through three separate dimensions:

1. **Precision:** How accurately the observed sample mean estimates the underlying mean, as represented by standard error.
2. **Consistency:** How much individual customer ratings vary, as represented by sample standard deviation.
3. **Evidence Volume:** How many reviews are available for a product.

Project-defined classification thresholds are used to summarize these dimensions. They are analytical categories, not universal statistical standards or probabilities.

## Dataset

The project uses the **Amazon Reviews 2023** dataset from McAuley Lab, University of California, San Diego.

Both the original and cleaned datasets are included in this GitHub repository.

### Dataset files

| File | Description |
|---|---|
| `data/raw/amazon_reviews.csv` | Original dataset |
| `data/processed/amazon_reviews_cleaned.csv` | Cleaned dataset used for statistical analysis |

### Dataset characteristics

| Attribute | Value |
|---|---:|
| Original reviews | 370,557 |
| Cleaned reviews | 366,692 |
| Exact duplicate rows removed | 3,865 |
| Unique products | 75,680 |
| Unique users | 305,033 |
| Product categories | 4 |
| Original dataset size | Approximately 38 MB |
| Cleaned dataset size | Approximately 38 MB |

### Product categories

- Digital Music
- Gift Cards
- Magazine Subscriptions
- Subscription Boxes

### Data cleaning

The cleaning process includes:

- Required-column validation
- Missing-value inspection
- Exact duplicate removal
- Recalculation of product review counts
- Recalculation of user review counts
- Rating-range validation
- Product-category consistency checks

The cleaning process removed 3,865 exact duplicate rows, leaving 366,692 reviews.

## Statistical Methodology and Results

### Objective 1: Review Count vs Product Rating

The raw Pearson correlation between review count and average product rating was:

\[
r=-0.00257
\]

The raw-scale linear regression did not show a statistically significant linear relationship.

After applying the logarithmic transformation:

\[
\hat{Y}=4.5584-0.0679\ln(1+X)
\]

Where:

- \(Y\) = average product rating
- \(X\) = number of reviews

The log-transformed model showed a statistically significant negative association:

- Slope: -0.0679
- p-value: \(8.27\times10^{-33}\)
- R-squared: 0.002

Category-adjusted multiple regression produced a positive coefficient for log review count:

- Coefficient: 0.0371
- R-squared: 0.0210

The category interaction analysis found statistically significant joint interaction terms:

- F-statistic: 8.9283
- p-value: \(6.55\times10^{-6}\)
- R-squared: 0.02138

**Interpretation:** The relationship depends on the scale and category adjustment. The low R-squared values indicate that review count explains only a small proportion of variation in product ratings. The regression results indicate association, not causation.

### Objective 2: Statistical Reliability

The analysis examined the effect of sample size on standard error.

The standard error of the sample mean is:

\[
SE=\frac{s}{\sqrt{n}}
\]

Where:

- \(s\) = sample standard deviation
- \(n\) = number of reviews

The largest product in the dataset, `B00IX1I3G6`, was selected for the CLT and Chebyshev simulation.

Its statistics were:

| Statistic | Value |
|---|---:|
| Reviews | 36,508 |
| Mean rating | 4.6061 |
| Variance | 1.1281 |
| Standard deviation | 1.0621 |

A simulation using 5,000 repeated samples for each sample size showed that empirical standard errors approached the theoretical values:

\[
SE=\frac{\sigma}{\sqrt{n}}
\]

The sample-mean distributions also became more symmetric as sample size increased, consistent with the Central Limit Theorem.

Chebyshev's inequality was evaluated using:

\[
P(|\bar{X}-\mu|\geq\epsilon)
\leq\frac{\sigma^2}{n\epsilon^2}
\]

with \(\epsilon=0.2\).

The observed simulation probabilities remained within the corresponding theoretical upper bounds.

**Interpretation:** Increasing sample size reduces the variability of sample means. The simulations illustrate the CLT and Chebyshev's inequality under an independent sampling model.

### Objective 3: Product Rating Reliability Measurement

Each product was evaluated using three dimensions.

**Precision**

\[
SE=\frac{s}{\sqrt{n}}
\]

**Consistency**

\[
s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}
\]

**Evidence Volume**

\[
n=\text{Number of observed reviews}
\]

The analysis covered 75,680 products.

#### Evidence volume classification

| Evidence classification | Number of products |
|---|---:|
| Insufficient (1 review) | 54,488 |
| Low (2–9 reviews) | 18,191 |
| Moderate (10–99 reviews) | 2,681 |
| High (100–999 reviews) | 294 |
| Very High (1,000+ reviews) | 26 |

Approximately 71.99% of products had only one review. Their sample standard deviation and standard error could not be calculated.

**Interpretation:** A high average rating alone does not establish rating reliability. Review volume, precision, and disagreement among customers must be considered separately.

## Project Structure

```text
statistical-reliability-online-product-ratings/
│
├── data/
│   ├── raw/
│   │   ├── amazon_reviews.csv
│   │   └── .gitkeep
│   │
│   └── processed/
│       ├── amazon_reviews_cleaned.csv
│       └── .gitkeep
│
├── src/
│   ├── clean_dataset.py
│   ├── exploratory_analysis.py
│   ├── objective1_review_count_vs_rating.py
│   ├── objective1_category_adjusted_regression.py
│   ├── objective1_category_interaction.py
│   ├── objective2_rating_reliability.py
│   ├── objective2_clt_chebyshev.py
│   ├── objective2_multi_product_reliability.py
│   └── objective3_product_reliability_measurement.py
│
├── outputs/
│   ├── plots/
│   └── reports/
│
├── docs/
│   └── project_report.md
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/Kapil961/Statistical-reliability-online-product-ratings.git

cd Statistical-reliability-online-product-ratings
```

### 2. Create a virtual environment

```bash
python3.11 -m venv .venv

source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify dataset files

Both datasets are already included in the repository.

Check that they exist:

```bash
ls -lh data/raw/amazon_reviews.csv

ls -lh data/processed/amazon_reviews_cleaned.csv
```

### 5. Run the analyses in order

Run the following scripts from the project root directory:

```bash
python src/clean_dataset.py

python src/exploratory_analysis.py

python src/objective1_review_count_vs_rating.py

python src/objective1_category_adjusted_regression.py

python src/objective1_category_interaction.py

python src/objective2_rating_reliability.py

python src/objective2_clt_chebyshev.py

python src/objective2_multi_product_reliability.py

python src/objective3_product_reliability_measurement.py
```

Generated plots are saved in `outputs/plots/`.

Generated statistical reports and CSV summaries are saved in `outputs/reports/`.

**Note:** Running the cleaning and analysis scripts regenerates the corresponding processed dataset and output files.

## Technologies Used

- Python 3.11
- NumPy
- Pandas
- Matplotlib
- Seaborn
- SciPy
- Statsmodels
- Jupyter Notebook

## Limitations

- The dataset contains only four product categories.
- A large proportion of products have only one review.
- Products have highly unequal review counts.
- The CLT and Chebyshev simulations use sampling with replacement from an empirical rating distribution.
- The simulations illustrate statistical principles and do not establish that real customer reviews are independent or representative.
- Regression results indicate associations and should not be interpreted as causal relationships.
- Reliability classification thresholds are project-defined analytical choices.

## Conclusion

This project demonstrates how statistical concepts can be applied to understand the reliability of online product ratings.

The analysis highlights that review count, rating variation, and standard error provide different information about a product's rating reliability.

A product with a high average rating may still have limited statistical evidence when based on very few reviews. Therefore, product ratings should be interpreted by considering both the estimated average and the amount and variability of supporting review data.

## Detailed Academic Report

The complete academic project report, including methodology, statistical formulas, results, interpretations, limitations, and references, is available here:

[`docs/project_report.md`](docs/project_report.md)

## Dataset Reference

McAuley Lab. *Amazon Reviews 2023*. University of California, San Diego.

https://amazon-reviews-2023.github.io/

## Author

**Kapil Kumawat**

B.Tech – Computer Science and Artificial Intelligence

JK Lakshmipat University, Jaipur, Rajasthan