# Statistical Reliability of Online Product Ratings

## Abstract

Online product ratings are widely used by consumers to evaluate products before making purchasing decisions. However, the reliability of an average product rating depends on several statistical factors, including the number of reviews, variation among individual ratings, and the distribution of observations.

This project investigates the statistical reliability of online product ratings using an Amazon product reviews dataset containing 370,557 observations across 11 variables. After data cleaning and removal of 3,865 duplicate records, 366,692 valid reviews covering 75,680 unique products and 305,033 unique users were retained.

The study consists of three objectives. First, it examines the relationship between the number of reviews and average product ratings using correlation and regression analysis, including category-adjusted and interaction models. Second, it investigates rating reliability through product-level variance, standard deviation, standard error, the Central Limit Theorem (CLT), and Chebyshev's inequality. Third, it measures product rating reliability through three dimensions: precision, consistency, and evidence volume.

The results demonstrate that the number of reviews alone does not fully explain differences in average product ratings. Review count is more clearly associated with the precision of an estimated average rating than with its rating value. The study also shows that products with only one review have insufficient information for estimating within-product rating variability.

The project provides a statistical framework for understanding why product ratings should be interpreted alongside review volume and rating variation rather than as isolated numbers.

---

## 1. Introduction

Online shopping platforms allow customers to share their experiences through numerical ratings and written reviews. These ratings influence purchasing decisions and help consumers compare products.

A product with an average rating of 4.8 stars may appear more attractive than one with 4.2 stars. However, the average rating does not reveal how many customers contributed to it or how much their opinions differ.

For example, a product rated 5.0 stars from two reviews may have a less dependable estimated average than a product rated 4.6 stars from several thousand reviews.

This raises an important statistical question:

**How reliable are online product ratings, and how does the amount of review evidence affect their reliability?**

Statistical methods such as correlation, regression, variance, standard deviation, standard error, the Central Limit Theorem, and Chebyshev's inequality can help investigate this question.

This project applies these concepts to a real-world product review dataset.

## 2. Problem Statement

Online product ratings are commonly presented as a single average value. Consumers may interpret this value as a reliable measure of product quality without considering the number of reviews or the variation among individual ratings.

However, two products with identical average ratings may have substantially different levels of statistical reliability.

A rating calculated from a small number of reviews may be more sensitive to individual opinions, while a rating calculated from a larger number of reviews may provide a more precise estimate of the average customer rating.

Furthermore, product categories may differ in their typical ratings and review volumes. Ignoring these differences may lead to misleading conclusions about the relationship between review count and product ratings.

Therefore, this project uses statistical analysis to study the relationship between review count and average ratings, examine the sampling behaviour of ratings, and develop a practical classification of product rating reliability.

## 3. Project Objectives

The project has exactly three objectives.

### Objective 1: Analyse the relationship between review count and average product rating

- Investigate whether the number of reviews is associated with the average product rating.
- Apply Pearson correlation and simple linear regression.
- Examine the relationship after accounting for product categories.
- Investigate whether the relationship differs across categories using interaction regression.

### Objective 2: Study the statistical reliability of product ratings

- Calculate product-level rating variance, standard deviation, and standard error.
- Examine how standard error changes with the number of reviews.
- Demonstrate the Central Limit Theorem through simulation.
- Apply Chebyshev's inequality to sample means.
- Compare observed standard errors with a pooled-standard-deviation reference.

### Objective 3: Develop a product rating reliability measurement framework

- Measure rating precision using standard error.
- Measure rating consistency using standard deviation.
- Measure evidence volume using the number of reviews.
- Classify products according to these three dimensions.
- Compare reliability measurements across product categories.

---

## 4. Dataset Description

### 4.1 Dataset overview

The project uses an Amazon product reviews dataset containing product ratings, review information, customer identifiers, and product identifiers.

The original dataset contained:

| Attribute | Value |
|---|---:|
| Original observations | 370,557 |
| Original columns | 11 |
| Unique products after cleaning | 75,680 |
| Unique users after cleaning | 305,033 |
| Final observations | 366,692 |
| Duplicate observations removed | 3,865 |

### 4.2 Dataset variables

The dataset contains the following variables:

| Variable | Description |
|---|---|
| category | Product category |
| rating | Numerical product rating |
| helpful_vote | Number of helpful votes |
| verified_purchase | Whether the purchase was verified |
| timestamp | Review timestamp |
| review_date | Review date |
| parent_asin | Parent product identifier |
| asin | Product identifier |
| user_id | Customer identifier |
| user_review_count | Number of reviews associated with the user |
| product_review_count | Number of reviews associated with the product |

The rating variable ranges from 1 to 5.

### 4.3 Product categories

The cleaned dataset contains four categories:

| Category | Number of reviews |
|---|---:|
| Gift Cards | 150,989 |
| Digital Music | 128,764 |
| Magazine Subscriptions | 70,922 |
| Subscription Boxes | 16,017 |
| **Total** | **366,692** |

### 4.4 Data cleaning and validation

Data cleaning was performed using the Python script:

`src/clean_dataset.py`

The following operations were performed:

1. Loaded the original dataset.
2. Verified the required columns.
3. Checked missing values.
4. Identified and removed exact duplicate records.
5. Recalculated product review counts using product identifiers.
6. Recalculated user review counts using user identifiers.
7. Verified that ratings were within the valid range of 1 to 5.
8. Checked product-category consistency.
9. Saved the cleaned dataset and a validation report.

### 4.5 Data validation results

| Validation check | Result |
|---|---|
| Missing values | 0 |
| Remaining exact duplicates | 0 |
| Product review counts valid | True |
| User review counts valid | True |
| Ratings within valid range | True |
| Products assigned to multiple categories | 0 |

The cleaned dataset was saved at:

`data/processed/amazon_reviews_cleaned.csv`

All subsequent analyses were performed using this cleaned dataset.

---

## 5. Statistical Methodology

This section describes the statistical concepts used throughout the project.

### 5.1 Arithmetic mean

The arithmetic mean represents the average of a set of observations.

For ratings \(x_1,x_2,\ldots,x_n\):

\[
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
\]

Here, \(n\) represents the number of reviews and \(x_i\) represents an individual rating.

### 5.2 Variance

Variance measures the dispersion of individual ratings around their mean.

The sample variance is:

\[
s^2=\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}
\]

A larger variance indicates greater disagreement among individual ratings.

### 5.3 Standard deviation

Standard deviation is the square root of variance.

\[
s=\sqrt{s^2}
\]

It measures rating variation in the original rating units.

### 5.4 Standard error

The standard error measures the estimated variability of a sample mean.

\[
SE=\frac{s}{\sqrt{n}}
\]

A smaller standard error generally indicates a more precise estimate of the mean, under the assumptions of the sampling model.

For a product with only one review, sample variance, sample standard deviation, and the corresponding estimated standard error cannot be calculated. These values are therefore treated as unavailable rather than zero.

### 5.5 Pearson correlation coefficient

Pearson's correlation coefficient measures the strength and direction of a linear relationship between two variables.

\[
r=\frac{\operatorname{Cov}(X,Y)}{\sigma_X\sigma_Y}
\]

Its value ranges from -1 to +1.

- Positive values indicate a positive linear association.
- Negative values indicate a negative linear association.
- Values close to zero indicate little linear association.

Correlation does not establish causation.

### 5.6 Simple linear regression

The simple linear regression model is:

\[
Y=\beta_0+\beta_1X+\epsilon
\]

Where:

- \(Y\) is the average product rating.
- \(X\) is the number of reviews or its transformation.
- \(\beta_0\) is the intercept.
- \(\beta_1\) is the regression coefficient.
- \(\epsilon\) is the error term.

The coefficient \(\beta_1\) describes the estimated change in average rating associated with a one-unit change in the predictor.

### 5.7 Multiple linear regression

Multiple regression examines the relationship between an outcome and multiple explanatory variables.

The category-adjusted model uses log-transformed review count and category indicator variables.

### 5.8 Regression interaction

An interaction model allows the relationship between review count and average rating to differ across categories.

It includes interaction terms between log-transformed review count and category indicators.

### 5.9 Central Limit Theorem

The Central Limit Theorem states that, under appropriate conditions, the distribution of sample means approaches a normal distribution as sample size increases.

The theoretical standard error of the sample mean is:

\[
SE_{\bar X}=\frac{\sigma}{\sqrt{n}}
\]

### 5.10 Chebyshev's inequality

Chebyshev's inequality provides an upper bound on the probability that a random variable differs from its mean by at least a specified distance.

For a sample mean:

\[
P(|\bar X-\mu|\geq\epsilon)
\leq
\frac{\sigma^2}{n\epsilon^2}
\]

The probability bound cannot exceed 1, so the practical bound is:

\[
P(|\bar X-\mu|\geq\epsilon)
\leq
\min\left(1,\frac{\sigma^2}{n\epsilon^2}\right)
\]

---

# 6. Objective 1: Relationship Between Review Count and Average Product Rating

## 6.1 Objective

The first objective investigates whether products with more reviews tend to receive higher or lower average ratings.

The analysis uses product-level observations rather than individual review-level observations. Each product contributes one average rating and one review count.

This avoids treating individual reviews as separate products in the regression analysis.

## 6.2 Product-level data preparation

The cleaned review dataset was grouped using the product identifier and category.

For every product, the following statistics were calculated:

- Number of reviews
- Mean rating
- Rating variance
- Rating standard deviation

Total products analysed: **75,680**

The mean product rating was 4.4932, while the mean review count was approximately 4.845.

The median product had only one review.

The maximum number of reviews associated with a product was 36,508.

## 6.3 Review count and rating distribution

The distribution of product review counts was highly right-skewed.

Most products had very few reviews:

| Number of reviews | Number of products |
|---|---:|
| 1 | 54,488 |
| 2–4 | 14,950 |
| 5–9 | 3,241 |
| 10–29 | 1,969 |
| 30–99 | 712 |
| 100–999 | 294 |
| 1,000+ | 26 |

Approximately 72% of products had only one review.

This imbalance is important when interpreting product-level statistical results.

## 6.4 Pearson correlation analysis

The Pearson correlation between raw review count and average product rating was:

\[
r=-0.00257
\]

The corresponding p-value was:

\[
p=0.4793
\]

The correlation is extremely close to zero, indicating almost no linear relationship between raw review count and average product rating in the overall product dataset.

The result does not provide evidence of a statistically significant raw-scale linear association.

## 6.5 Simple linear regression using raw review count

The fitted regression equation was:

\[
\hat{Y}=4.4933-0.00001606X
\]

Where:

- \(Y\) represents average product rating.
- \(X\) represents the number of reviews.

The slope was extremely small and was not statistically significant.

The model had an R-squared value close to zero.

Therefore, raw review count alone does not explain meaningful variation in average product ratings.

## 6.6 Regression using log-transformed review count

Because review counts were highly right-skewed, the logarithmic transformation was also examined.

The predictor was defined as:

\[
X'=\ln(1+X)
\]

The fitted regression equation was:

\[
\hat{Y}=4.5584-0.0679\ln(1+X)
\]

Results:

| Statistic | Result |
|---|---:|
| Regression coefficient | -0.0679 |
| t-statistic | -11.935 |
| p-value | \(8.27\times10^{-33}\) |
| R-squared | 0.002 |

The negative coefficient indicates a negative association between log-transformed review count and average product rating in the pooled dataset.

Although the coefficient was statistically significant, the model explained only approximately 0.2% of the variation in average product ratings.

This demonstrates why statistical significance should not be confused with practical explanatory power.

## 6.7 Category-adjusted multiple regression

Product categories have different rating distributions and review-count patterns.

To account for these differences, a multiple regression model was fitted:

\[
Y=\beta_0+\beta_1\ln(1+n)
+\beta_2D_1+\beta_3D_2+\beta_4D_3+\epsilon
\]

Digital Music was used as the baseline category.

The estimated model was:

\[
\begin{aligned}
\hat{Y}={}&4.4963+0.0371\ln(1+n)\\
&-0.3364D_{\text{Gift Cards}}\\
&-0.5804D_{\text{Magazine}}\\
&-0.9031D_{\text{Subscription Boxes}}
\end{aligned}
\]

Results:

| Variable | Coefficient | p-value |
|---|---:|---:|
| Log review count | +0.0371 | \(9.22\times10^{-9}\) |
| Gift Cards | -0.3364 | < 0.001 |
| Magazine Subscriptions | -0.5804 | < 0.001 |
| Subscription Boxes | -0.9031 | < 0.001 |

Model statistics:

| Statistic | Result |
|---|---:|
| R-squared | 0.021034 |
| Adjusted R-squared | 0.020982 |
| F-statistic | 406.5 |
| Number of products | 75,680 |

The log review count coefficient changed from negative in the pooled regression to positive after adjusting for category.

This indicates that category composition has an important influence on the pooled relationship.

The result resembles a Simpson's-paradox-type pattern: the overall association and the category-adjusted association have different directions.

However, the adjusted model still explains only about 2.1% of the variation in average product ratings.

## 6.8 Category-specific correlation

Pearson correlations were also calculated separately for each category.

| Category | Products | Raw count correlation | Log count correlation |
|---|---:|---:|---:|
| Digital Music | 70,511 | 0.003148 | 0.006849 |
| Gift Cards | 1,137 | 0.030336 | 0.181224 |
| Magazine Subscriptions | 3,391 | 0.012663 | 0.050253 |
| Subscription Boxes | 641 | 0.022073 | 0.029301 |

The log-transformed review-count correlations were positive in all four categories.

The strongest category-level correlation was observed for Gift Cards.

These correlations are descriptive and should not be interpreted as proof of causation.

## 6.9 Category interaction regression

An interaction model was fitted to determine whether the relationship between log review count and average rating differed across categories.

The model included:

- Log review count
- Category indicator variables
- Interaction terms between log review count and category indicators

Results:

| Statistic | Result |
|---|---:|
| R-squared | 0.021380 |
| Adjusted R-squared | 0.021290 |
| F-statistic | 236.2 |
| Observations | 75,680 |

Estimated category-specific slopes:

| Category | Log review-count slope |
|---|---:|
| Digital Music | 0.015529 |
| Gift Cards | 0.112675 |
| Magazine Subscriptions | 0.043486 |
| Subscription Boxes | 0.026225 |

The joint interaction test produced:

\[
F=8.9283
\]

\[
p=6.5457\times10^{-6}
\]

The interaction terms were jointly statistically significant.

The Gift Cards interaction was individually significant, while the Magazine Subscriptions and Subscription Boxes interaction terms were not statistically significant at the 5% level.

However, the improvement in R-squared was small:

\[
0.021380-0.021034=0.000346
\]

Thus, allowing category-specific slopes improved model fit only slightly.

## 6.10 Regression diagnostics and interpretation

Residual diagnostics for the category-adjusted regression indicated:

- Residual skewness: approximately -2.286
- Residual excess kurtosis: approximately 4.861
- Strong evidence of non-normal residuals

The average product rating is bounded between 1 and 5, and its distribution is not normally distributed.

Consequently, conventional OLS p-values and standard errors should be interpreted cautiously.

The dataset also has substantially unequal category sizes, which affects the precision of category-specific estimates.

### Objective 1 conclusion

The analysis shows that raw review count has almost no linear relationship with average product rating.

After logarithmic transformation, a small negative pooled association was observed. However, after adjusting for product category, the estimated relationship became positive.

The interaction analysis also showed that the relationship varies across categories, although the additional explanatory power was small.

Overall, review count alone is not a strong predictor of average product rating. Category differences must be considered when interpreting the relationship.

---

# 7. Objective 2: Statistical Reliability of Product Ratings

## 7.1 Objective

The second objective investigates how reliably a product's average rating represents the underlying pattern of customer ratings.

The analysis focuses on three statistical quantities:

1. Variance
2. Standard deviation
3. Standard error

It also applies the Central Limit Theorem and Chebyshev's inequality through simulation.

## 7.2 Product-level variance and standard error

For each product, the following statistics were calculated:

\[
\bar{x}=\frac{1}{n}\sum x_i
\]

\[
s^2=\frac{\sum(x_i-\bar{x})^2}{n-1}
\]

\[
SE=\frac{s}{\sqrt n}
\]

Products were divided into seven review-count groups.

### Results

| Review group | Products | Average rating variance | Average SD | Average SE |
|---|---:|---:|---:|---:|
| 1 | 54,488 | Not available | Not available | Not available |
| 2–4 | 14,950 | 0.991940 | 0.567753 | 0.363183 |
| 5–9 | 3,241 | 1.161233 | 0.837977 | 0.335220 |
| 10–29 | 1,969 | 1.328253 | 1.025916 | 0.264661 |
| 30–99 | 712 | 1.569175 | 1.186032 | 0.171239 |
| 100–999 | 294 | 1.670270 | 1.241326 | 0.089448 |
| 1,000+ | 26 | 1.557651 | 1.214490 | 0.027358 |

The average standard error generally decreased as review count increased.

This supports the statistical principle that larger sample sizes tend to produce more precise estimates of the mean.

However, the average variance and standard deviation did not decrease with review count. They increased across several groups.

This distinction is important:

- Standard deviation measures disagreement among individual ratings.
- Standard error measures the estimated uncertainty of the sample mean.

A product can have considerable disagreement among customers but still have a relatively precise estimated average when the number of reviews is large.

## 7.3 Central Limit Theorem simulation

A product with a large number of reviews was selected for simulation.

Selected product:

**B00IX1I3G6**

Number of observed reviews:

\[
n=36,508
\]

Rating distribution:

| Rating | Number of reviews |
|---|---:|
| 1 star | 2,328 |
| 2 stars | 451 |
| 3 stars | 913 |
| 4 stars | 1,888 |
| 5 stars | 30,928 |

The mean rating was:

\[
\mu=4.60614
\]

The empirical variance used for simulation was:

\[
\sigma^2=1.128073
\]

The corresponding standard deviation was:

\[
\sigma=1.062108
\]

The original rating distribution was highly asymmetric, with approximately 84.72% of reviews giving five stars.

### Simulation settings

The simulation used:

- Sample sizes: 5, 10, 30, 50, 100, and 500
- Number of simulations per sample size: 5,000
- Sampling with replacement
- Random seed: 42

For every simulation, a random sample of ratings was selected and its sample mean was calculated.

### CLT simulation results

| Sample size | Theoretical SE | Empirical SE | Skewness | Excess kurtosis |
|---:|---:|---:|---:|---:|
| 5 | 0.47499 | 0.47106 | -1.24127 | 1.38040 |
| 10 | 0.33587 | 0.34001 | -0.93435 | 0.88905 |
| 30 | 0.19391 | 0.19299 | -0.51287 | 0.22432 |
| 50 | 0.15020 | 0.14771 | -0.35130 | 0.05574 |
| 100 | 0.10621 | 0.10748 | -0.25200 | 0.01912 |
| 500 | 0.04750 | 0.04800 | -0.13268 | 0.05170 |

### Interpretation

The empirical standard errors were close to the theoretical values:

\[
SE=\frac{\sigma}{\sqrt n}
\]

As the sample size increased:

- The standard error decreased.
- The sample-mean distribution became more symmetric.
- Skewness moved closer to zero.
- The sample means became more normal-like.

These observations are consistent with the Central Limit Theorem.

The simulation demonstrates how sample means can become more normally distributed even when the original rating distribution is highly asymmetric.

The simulation uses independent sampling with replacement from the observed empirical distribution. It illustrates the theoretical sampling behaviour and does not establish that actual customer reviews are independent or representative.

## 7.4 Chebyshev's inequality

Chebyshev's inequality was applied to the sample means generated in the CLT simulation.

The deviation threshold was:

\[
\epsilon=0.2
\]

The probability of a sample mean differing from the population mean by at least 0.2 was measured for each sample size.

The theoretical upper bound was calculated as:

\[
P(|\bar X-\mu|\geq0.2)
\leq
\min\left(1,\frac{\sigma^2}{n(0.2)^2}\right)
\]

### Results

| Sample size | Observed deviation probability | Chebyshev upper bound |
|---:|---:|---:|
| 5 | 0.7814 | 1.00000 |
| 10 | 0.5822 | 1.00000 |
| 30 | 0.2964 | 0.94006 |
| 50 | 0.1682 | 0.56404 |
| 100 | 0.0592 | 0.28202 |
| 500 | 0.0000 | 0.05640 |

### Interpretation

The observed probability of a deviation of at least 0.2 decreased as the sample size increased.

The Chebyshev upper bound also decreased with sample size.

For every sample size, the observed deviation probability was below the theoretical upper bound.

At sample size 500, no deviations were observed among the 5,000 simulations. This does not mean the true probability is zero; it only means that no such event occurred in the simulated samples.

The result demonstrates how Chebyshev's inequality provides a distribution-independent upper bound on deviations from the mean.

## 7.5 Multi-product reliability comparison

To examine whether the results were specific to one product, the reliability analysis was extended across all products.

The pooled review-level variance was:

\[
\sigma^2=1.491801
\]

The pooled standard deviation was:

\[
\sigma=1.221393
\]

A reference standard error was calculated using:

\[
SE_{\text{reference}}=\frac{\sigma}{\sqrt n}
\]

This provided a common-variance reference for comparing observed product-level standard errors.

### Results

| Review group | Average observed SE | Average theoretical reference SE |
|---|---:|---:|
| 1 | Not available | 1.22139* |
| 2–4 | 0.36318 | 0.79391 |
| 5–9 | 0.33522 | 0.49045 |
| 10–29 | 0.26466 | 0.31828 |
| 30–99 | 0.17124 | 0.17734 |
| 100–999 | 0.08945 | 0.08796 |
| 1,000+ | 0.02736 | 0.02702 |

*For products with one review, the reference value is based on the pooled standard deviation. An individual product's sample standard deviation and sample standard error cannot be estimated from one observation.

### Interpretation

The average observed standard error decreased substantially as review count increased.

For products with larger review counts, observed standard errors were close to the pooled-standard-deviation reference.

The observed standard errors in smaller review groups were sometimes lower than the reference because many products had identical ratings in their small observed samples.

This does not establish that those products will continue to receive identical ratings in future reviews.

The pooled reference also assumes a common standard deviation, whereas actual products can have different rating variability.

### Objective 2 conclusion

The results demonstrate that review count has an important relationship with the precision of average product ratings.

Standard error generally decreases as the number of reviews increases, even though individual rating variation does not necessarily decrease.

The CLT simulation showed that the distribution of sample means becomes more symmetric as sample size increases. Chebyshev's inequality provided valid upper bounds on deviations from the mean.

The multi-product comparison confirmed the general pattern across the dataset.

---

# 8. Objective 3: Product Rating Reliability Measurement

## 8.1 Objective

The third objective develops a practical framework to measure product rating reliability.

A single numerical rating cannot fully describe the reliability of a product's average rating. Therefore, three separate dimensions were considered:

1. Precision
2. Consistency
3. Evidence volume

These dimensions are reported separately rather than combined into an arbitrary overall score.

## 8.2 Reliability dimensions

### A. Precision

Precision is measured using standard error:

\[
SE=\frac{s}{\sqrt n}
\]

A smaller standard error indicates a more precise estimate of the average rating under the sampling assumptions.

### B. Consistency

Consistency is measured using sample standard deviation:

\[
s=\sqrt{\frac{\sum(x_i-\bar{x})^2}{n-1}}
\]

A smaller standard deviation indicates that individual ratings are more closely grouped around their mean.

### C. Evidence volume

Evidence volume is measured using the total number of reviews:

\[
n=\text{Number of reviews}
\]

A larger number of reviews indicates a larger quantity of observed evidence.

However, review count alone does not guarantee that reviews are representative or independent.

## 8.3 Reliability classification thresholds

The following project-defined thresholds were used to classify products.

These thresholds are analytical choices for this project and are not universal statistical standards.

### Evidence volume classification

| Number of reviews | Classification |
|---|---|
| 1 | Insufficient |
| 2–9 | Low |
| 10–99 | Moderate |
| 100–999 | High |
| 1,000 or more | Very High |

### Precision classification

| Standard error | Classification |
|---|---|
| SE ≤ 0.05 | Very High |
| 0.05 < SE ≤ 0.10 | High |
| 0.10 < SE ≤ 0.20 | Moderate |
| SE > 0.20 | Low |

### Consistency classification

| Standard deviation | Classification |
|---|---|
| SD ≤ 0.50 | Very High |
| 0.50 < SD ≤ 0.75 | High |
| 0.75 < SD ≤ 1.00 | Moderate |
| SD > 1.00 | Low |

For products with only one review, precision and consistency are classified as unavailable because sample standard deviation and standard error cannot be estimated.

## 8.4 Evidence volume results

The product-level evidence volume classification produced the following results:

| Evidence volume category | Number of products |
|---|---:|
| Insufficient | 54,488 |
| Low | 18,191 |
| Moderate | 2,681 |
| High | 294 |
| Very High | 26 |
| **Total** | **75,680** |

The largest group consisted of products with only one review.

This indicates that a large proportion of product ratings in the dataset are based on very limited review evidence.

## 8.5 Precision results

The precision classification produced:

| Precision category | Number of products |
|---|---:|
| Not Available | 54,488 |
| Low | 9,858 |
| Very High | 9,623 |
| Moderate | 1,318 |
| High | 393 |
| **Total** | **75,680** |

Precision could not be estimated for products with only one review.

Among the remaining products, the distribution shows that many products have relatively large standard errors, while some have very small standard errors.

The number of reviews and rating variation jointly determine standard error.

## 8.6 Consistency results

The consistency classification produced:

| Consistency category | Number of products |
|---|---:|
| Not Available | 54,488 |
| Very High | 10,731 |
| Low | 6,477 |
| High | 2,878 |
| Moderate | 1,106 |
| **Total** | **75,680** |

Products classified as having very high consistency had relatively low variation among their observed ratings.

Products classified as having low consistency had larger rating variation.

Consistency and precision are related but different concepts. A product may have considerable disagreement among customers but still have a relatively precise average rating if its review count is sufficiently large.

## 8.7 Category-wise reliability analysis

The reliability framework was also applied separately to the four product categories.

### Results

| Category | Products | Average reviews | Average rating | Average SD | Average SE | Median SE |
|---|---:|---:|---:|---:|---:|---:|
| Digital Music | 70,511 | 1.8262 | 4.5289 | 0.5801 | 0.3260 | 0 |
| Gift Cards | 1,137 | 132.7960 | 4.2546 | 1.0059 | 0.2900 | 0.1664 |
| Magazine Subscriptions | 3,391 | 20.9148 | 3.9867 | 1.1827 | 0.4267 | 0.3111 |
| Subscription Boxes | 641 | 24.9875 | 3.6654 | 1.3085 | 0.4730 | 0.3815 |

Average standard error is calculated only for products where it can be estimated. The average review count includes all products in each category.

### Interpretation

Digital Music had the highest average product rating and the lowest average product-level standard deviation.

Subscription Boxes had the lowest average product rating and the highest average product-level standard deviation.

Gift Cards had a substantially higher average review count than the other categories.

Digital Music had a median standard error of zero because many products had identical ratings across their small observed samples. This should not be interpreted as proof that their future average ratings are perfectly certain.

The category comparisons also show that the reliability characteristics of products differ across categories.

## 8.8 Objective 3 conclusion

The reliability framework demonstrates that product ratings should be interpreted using multiple dimensions.

- Precision describes the estimated uncertainty of the average rating.
- Consistency describes the variation among individual ratings.
- Evidence volume describes how many reviews support the rating.

The classification results show that a large proportion of products have insufficient evidence for estimating rating variability because they have only one review.

Therefore, presenting an average rating without its review count and information about rating variation can provide an incomplete picture of product reliability.

---

# 9. Overall Findings

The project produced several important findings across its three objectives.

### Finding 1: Review count is not a strong predictor of average product rating

The raw Pearson correlation was approximately -0.00257, indicating almost no linear association between raw review count and average product rating.

### Finding 2: Product category affects the observed relationship

The log review-count coefficient changed from negative in the pooled regression to positive in the category-adjusted regression.

The interaction analysis also showed that the relationship differs across categories.

### Finding 3: Statistical significance does not imply strong explanatory power

Although some regression coefficients were statistically significant, the models explained only a small proportion of the variation in average product ratings.

### Finding 4: Standard error generally decreases with review count

Products with more reviews generally had lower average standard errors, indicating greater precision in their estimated average ratings.

### Finding 5: Rating variation and mean precision are different

Standard deviation measures disagreement among individual ratings, while standard error measures the estimated variability of the mean.

A larger review count can reduce standard error without reducing individual rating variation.

### Finding 6: The Central Limit Theorem is demonstrated through simulation

As sample size increased, the simulated sample-mean distributions became more symmetric and their standard errors decreased.

### Finding 7: Chebyshev's inequality provides an upper bound

The observed deviation probabilities remained below the theoretical Chebyshev bounds in the simulation.

### Finding 8: A large number of products have insufficient review evidence

Out of 75,680 products, 54,488 had only one review. For these products, sample standard deviation and standard error could not be estimated.

### Finding 9: Reliability differs across product categories

The categories differed in average rating, review volume, rating variation, and estimated standard error.

---

# 10. Limitations of the Study

The following limitations should be considered when interpreting the findings.

1. **Dataset representation:** The results describe the supplied Amazon reviews dataset and may not represent every product or customer on the platform.

2. **Review dependence:** Actual customer reviews may not be statistically independent. The CLT simulation uses sampling with replacement and therefore represents an idealized sampling model.

3. **Unequal category sizes:** Digital Music contains substantially more products than the other categories. This affects the precision of category-specific estimates.

4. **Large number of single-review products:** A large proportion of products have only one review, preventing estimation of their within-product sample variance, standard deviation, and standard error.

5. **Bounded rating scale:** Ratings are restricted to values from 1 to 5. This contributes to non-normality and limits the suitability of some conventional regression assumptions.

6. **Regression assumptions:** Residual diagnostics showed substantial non-normality. Conventional OLS standard errors and p-values should therefore be interpreted cautiously.

7. **Low explanatory power:** The regression models explain only a small proportion of the variation in average product ratings.

8. **Project-defined classification thresholds:** The precision, consistency, and evidence-volume thresholds are analytical choices made for this project, not universally accepted reliability standards.

9. **Pooled variance reference:** The multi-product theoretical standard error comparison uses a common pooled standard deviation, although actual product rating variances differ.

10. **No causal interpretation:** Correlation and regression identify associations, not causal effects. The study does not establish that increasing the number of reviews causes a product's rating to change.

---

# 11. Conclusion

This project examined the statistical reliability of online product ratings using a cleaned Amazon reviews dataset containing 366,692 reviews and 75,680 unique products.

The first objective investigated the relationship between review count and average product rating. The results showed that raw review count had almost no linear association with average product rating. After accounting for product categories, the estimated relationship changed direction, demonstrating the importance of category differences. Nevertheless, the explanatory power of the regression models remained low.

The second objective investigated rating reliability using variance, standard deviation, standard error, the Central Limit Theorem, and Chebyshev's inequality. The results demonstrated that standard error generally decreases as review count increases. Simulation results were consistent with the Central Limit Theorem, while Chebyshev's inequality provided upper bounds on deviations of sample means.

The third objective developed a reliability measurement framework based on precision, consistency, and evidence volume. The results showed that a large proportion of products had only one review, making it impossible to estimate their within-product sample variability.

Overall, the study demonstrates that an average product rating should not be interpreted in isolation. The number of reviews and the variation among individual ratings provide important additional information for understanding rating reliability.

A product rating supported by a larger amount of review evidence may provide a more precise estimate of the average rating, but high precision does not necessarily mean that all customers agree. Therefore, consumers and analytical systems should consider average ratings together with review volume and rating variability.

---

# 12. Project Reproducibility

## 12.1 Technologies used

- Python 3.11
- NumPy
- Pandas
- Matplotlib
- Seaborn
- SciPy
- Statsmodels
- Jupyter Notebook

## 12.2 Project structure

```text
statistical-reliability-online-product-ratings/
│
├── data/
│   ├── raw/
│   │   └── amazon_reviews.csv
│   │
│   └── processed/
│       └── amazon_reviews_cleaned.csv
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
├── .gitignore
├── README.md
└── requirements.txt
```

## 12.3 Installation

Create and activate a Python virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 12.4 Execution order

Run the scripts from the project root directory in the following order:

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

The scripts generate statistical reports, CSV summaries, and plots inside the `outputs/` directory.

---

# 13. References

1. McAuley Lab. *Amazon Reviews 2023*. University of California, San Diego. Dataset website: https://amazon-reviews-2023.github.io/
2. Course syllabus: Advanced Statistics — Random Variables, Multiple Random Variables, Operations on Multiple Random Variables, Regression Analysis, and Design of Experiments.
3. Python documentation: https://docs.python.org/3/
4. NumPy documentation: https://numpy.org/doc/
5. Pandas documentation: https://pandas.pydata.org/docs/
6. SciPy documentation: https://docs.scipy.org/doc/scipy/
7. Statsmodels documentation: https://www.statsmodels.org/

---

**End of Project Report**