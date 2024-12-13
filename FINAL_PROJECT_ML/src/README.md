# **Data-Driven Real Estate: Find the dream home for your business**.

In the competitive real estate market, making decisions based on intuition can lead to risky and unprofitable investments. This project, **Data-Driven Real Estate**, leverages the power of Machine Learning to classify properties based on their **Return on Investment (ROI)**, helping investors prioritize the most lucrative opportunities.

With a precise and reliable predictive model, this project transforms thousands of data points into actionable decisions, optimizing portfolios and reducing risks.

## **Table of contents**   
1. [Repository structure](#id1)
2. [Summary of contents](#id2)
3. [Key findings](#id3)

## Repository structure <a name="id1"></a>
- `src/`: Directory that stores all the data files used in the analysis.
- `src/utils`: Directory that includes all the modules and auxiliary functions created for the development of the project.
- `src/data/raw`: Directory that stores all the data files needed to start with the analysis and modeling.
- `src/data/processed`: Directory that stores data already processed that will go into the model.
- `src/notebooks`: Directory that stores all the cleaning notebooks, processing, EDA and Machine Learning models.
- `src/model`: Models already trained and ready to go into production.

## Summary of contents <a name="id2"></a>
### Aim of the project
The main objective of this project is to use Machine Learning techniques to classify properties based on their Return on Investment (ROI), focusing on:

- Automating the evaluation process to reduce time and manual effort.
- Identifying high-potential investment opportunities.
- Reducing risks associated with unprofitable investments.
- Prioritizing properties that maximize portfolio returns.

### Metodology

1. Data collection and cleaning

  - Datasets were sourced from Zillow, Realtor, and the U.S. Census Bureau.
  - Cleaning involved handling missing values, removing outliers, and normalizing variables.

2. Exploratory Data Analysis (EDA)

  - Trends were analyzed to identify the factors most correlated with ROI, such as location, price per square meter, and amenities.

3. Model training and evaluation

  - Algorithms tested: Logistic Regression, Decision Trees, Random Forest.
  - Final Model: Logistic Regression, achieving a 97% accuracy.
  
4. Implementation of the model

  - Developed a model for automated property classification.
  - ROI prediction for new properties based on historical patterns.

## Key findings <a name="id3"></a>

**Performance of the model**

The Logistic Regression model achieved:

- **Overall Accuracy**: 97%.
- **Precision by category**:
  - Highly Profitable: 94%
  - Somewhat Profitable: 97%
  - Not Profitable: 94%

 ### Business impact

1. **Risk reduction**   
2. **Time efficiency**
3. **Portfolio optimization**



In summary, with this project, investors gain a reliable tool to make faster, data-driven decisions in real estate, minimizing risks and maximizing returns. By automating the classification process, this project paves the way for smarter and more efficient property investments.
