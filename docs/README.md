---
layout: home
permalink: index.html

# Please update this with your repository name and title
repository-name: eYY-4yp-project-template
title:
---

[comment]: # "This is the standard layout for the project, but you can clean this and use your own template"

# Multi-Modal Data Fusion for Trading Market Price Forecasting

#### Team

- E/19/278, Perera A.P.T.T., [email](mailto:e19452@eng.ac.lk)
- E/19/349, Sandaruwan K.G.S.T., [email](mailto:e19452@eng.ac.lk)
- E/19/492, Somawansha M.V.N.L., [email](mailto:e19492@eng.pdn.ac.lk)
  
#### Supervisors

- Prof. Manjula Sandirigama, [email](mailto:manjula.sandirigama@eng.pdn.ac.lk)
- Dr. Sampath Deegalla, [email](mailto:sampath@eng.pdn.ac.lk)

#### Table of content

1. [Introduction](#introduction)
2. [Background and Motivation](#background-and-motivation)
3. [Problem Statement](#problem-statement)
4. [Research Gap](#research-gap)
5. [Aim](#aim)
6. [Proposed Solution](#proposed-solution)
7. [Research Methodology](#research-methodology)
8. [Data Collection](#data-collection)
9. [High Level Design Architecture](#high-level-design-architecture)
10. [Data Preprocessing & Feature Engineering](#data-preprocessing-&-feature-engineering)
11. [Links](#links)

---

<!-- 
DELETE THIS SAMPLE before publishing to GitHub Pages !!!
This is a sample image, to show how to add images to your page. To learn more options, please refer [this](https://projects.ce.pdn.ac.lk/docs/faq/how-to-add-an-image/)
![Sample Image](./images/sample.png) 
-->
## Introduction

*What is Trading?*

- Buying and selling of financial assets in markets with the aim of making a profit.

*Challenges in Traditional Trading*

- Technical analysis alone fails to capture sudden market shifts.
- Emotional trading leads to 70–90% losses among retail traders.

---

## Background and Motivation
   Highlights the importance of stock market forecasting for reducing risk and improving trading strategies in a $110 trillion global market influenced by factors like interest rates, inflation, and employment data. Traditional technical analysis methods often fall short, leading to high retail trader losses. Advances in machine learning enable analysis of large datasets and complex patterns, especially when integrating macroeconomic indicators that can predict market shifts. The study aims to develop a comprehensive prediction framework that combines historical data, market patterns, and macroeconomic factors to enhance accuracy and provide traders with actionable, data-driven insights for better decision-making.

## Problem Statement

Accurately predicting tradable moments and entry/exit points in Gold (XAU/USD) is extremely difficult due to its high volatility and sudden market shocks based on economic conditions.

## Research Gap
   Current trading price forecasting models face several key limitations: they mostly rely on price data and technical indicators, often ignoring important macroeconomic factors; they lack effective mechanisms to control traders’ emotional biases like FOMO or panic selling; and they suffer from poor interpretability, making it hard for traders to trust AI predictions. Additionally, many models fail to adapt to different market regimes (bull, bear, sideways), reducing their accuracy during volatile or shifting conditions. Addressing these gaps requires multi-modal, emotionally aware, interpretable, and adaptive machine learning models for more reliable trading forecasts.

## Aim
   The aim of this research is to forecast trading moments, entry prices, and exit prices for gold (XAU/USD) by analyzing the relationship between historical price movement patterns, market trading volume, and key macroeconomic indicators such as CPI, GDP, PPI, PCE, NFP, and interest rates. The research seeks to develop a multi-modal machine learning framework that enhances the predictive accuracy of trading decisions by integrating these factors.

## Proposed Solution
   Introduces a multi-modal machine learning framework to improve financial forecasting by integrating historical price data, trading volume, and macroeconomic factors. Using deep learning, the model analyzes price trends and volume to gauge trend strength, while incorporating economic indicators like inflation and interest rates to capture external influences. It also predicts optimal stop-loss levels to enhance risk management during market volatility. This comprehensive approach aims to deliver more accurate, transparent, and data-driven trade entry and exit predictions, addressing existing model limitations and supporting better decision-making in complex markets.

## Research Objectives

*General Objective:*  
Develop a multi-modal machine learning framework that integrates:
- Historical price data
- Market trading volume
- Macroeconomic factors
- Technical indicators

*Specific Objectives:*
- Analyze the relationship between key macroeconomic factors in the United States towards fluctuations in the XAU/USD price.

---

## Macroeconomic Factors

Macroeconomic indicators significantly influence markets, providing insights into a country's economic health and investor sentiment. Key factors include:
- Interest Rate (Federal Reserve Rate)
- Consumer Price Index (CPI)
- Non-Farm Payrolls (NFP)
- Personal Consumption Expenditures (PCE)
- Gross Domestic Product (GDP)
- Producer Price Index (PPI)

Key highlights:
- **Data Fusion**: Combining historical price data, trading volume, and macroeconomic factors.
- **Modeling**: Utilizing deep learning models like LSTM or Transformer.
- **Goal**: Improve breakout classification and support better trading decisions.

We aim to help traders identify high-probability opportunities and reduce risks amid market volatility.


## Research Methodology
   This multi-stage framework for breakout prediction is a comprehensive system that integrates multiple data-driven approaches to enhance trading accuracy. Each module plays a crucial role in processing and analyzing different aspects of financial data, ensuring a well-rounded predictive model. The structured interaction between trend analysis, volume assessment, macroeconomic influences, and support/resistance classification enables the identification of high-confidence trading signals. By leveraging machine learning and real-time market insights, this system provides traders with a powerful tool to differentiate between real breakouts and fakeouts, improving profitability and risk management.

### Data Collection

Data is collected from multiple sources:
- *Macroeconomic Indicators* from Federal Reserve Statements, Investing.com (2018-2025)
- *XAU/USD Price & Trading Volume* through MetaTrader 5 API, IC Market Broker

### Data Preprocessing & Feature Engineering
- Handling missing data, normalization, scaling, and outlier detection
- Feature engineering to create new data features and perform correlation/feature selection

![image](https://github.com/user-attachments/assets/b5c70746-40e8-4829-bee0-0574fd6200b3)

• Gold Price Data (XAU/USD): We will collect historical XAU/USD OHLCV (Open, High, Low, Close, Volume) data across multiple timeframes (30-minute, hourly, 4-hourly, daily, weekly, and monthly) using the MetaTrader5 local terminal. This ensures we capture both short-term fluctuations and long-term trends. The data will cover the period from 2015 to 2025.

• Macroeconomic Indicators: These fundamental factors drive long-term price movements and market sentiment. We will focus on: Interest Rate (Federal Reserve Rate): Determines monetary policy direction, Consumer Price Index (CPI): Reflects inflationary pressures, Non-Farm Payrolls (NFP): Measures employment trends and economic health, Personal Consumption Expenditures (PCE): Tracks consumer spending behavior, Gross Domestic Product (GDP): Indicates overall economic growth, Producer Price Index (PPI): Represents inflation at the producer level.

![image](https://github.com/user-attachments/assets/78e5ca5d-ad3b-421d-be31-4a51218f8d43)

   Integration Strategy: Web scraping from Investing.com and manually extracting Federal Reserve statements. Data will be collected for the 2015-2025 range to cover multiple economic cycles.

![image](https://github.com/user-attachments/assets/bd5ce218-da41-4a8f-ba0a-21d3337c15b7)

![image](https://github.com/user-attachments/assets/4e11ccc9-2616-4ab9-8003-94152994f61e)


## High Level Design Architecture
![image](https://github.com/user-attachments/assets/9b8eefca-db8a-41fe-af5d-1e4e24cac0e8)

## Data Preprocessing & Feature Engineering
   1. Missing data handling
              - Interpolation
              - Forward filling
   2. Normalization and scaling
   3. Outlier detection
   4. Time series data preprocessing
              - Date & Time Conversion
              - Resampling
  5. Feature Engineering
  6. Correlation & Feature Selection


### Models Used
- *ARIMA/SARIMA:* Statistical model for forecasting based on time series analysis.
- *LSTM (Long Short-Term Memory):* Deep learning approach for capturing long-term dependencies in sequential data.
- *XGBoost:* Tree-based ensemble model, capturing complex patterns from structured data.
![image](https://github.com/user-attachments/assets/3fdd6b02-968c-4048-9c20-d61e53ad37cf)

---

## Key Findings

1. *CPI, PPI, and PCE* are highly correlated with market trends.
2. *Macroeconomic Factors:* CPI, PCE, and GDP show a negative correlation with the market trend.
3. *Market Volume:* Significant variations observed in global market sessions (Sydney, Tokyo, London, New York).

---

## Model Performance

### ARIMA vs SARIMA Model Comparison
| Model   | RMSE  | MAE  | MAPE (%) |
|---------|-------|------|----------|
| ARIMA   | 11.24 | 12.03| 1.12     |
| SARIMA  | 10.42 | 8.65 | 0.71     |

### LSTM Model Results:
- *RMSE for various timeframes* ranging from 8.37 (30 min) to 287.21 (1 week).
- *Overall Accuracy with Macro:* 95.84%
- *Overall Directional Accuracy with Macro:* 72.73%
- *Hybrid (Indicators + Macro):* 96.80% Accuracy, 93.82% Directional Accuracy.

---

## Insights & Impact

1. *Regime-Aware Forecasting*: Build models to identify different market conditions.
2. *Session-Dependent Liquidity Patterns*: Tune execution algorithms based on market sessions.
3. *Automated Execution*: Leverage real-time data for risk-controlled, smart trading execution.

---

## Future Research Directions

- Manual extraction of macroeconomic factors.
- High computational power requirement.
- Overfitting risk in complex models.

---

## Limitations

1. Limited data availability for real-time forecasting.
2. The complexity of models increases the risk of overfitting.
<!-- ## Results and Analysis-->

<!--## Conclusion-->

<!--## Publications-->
<!--[//]: # "Note: Uncomment each once you uploaded the files to the repository" -->

<!-- 1. [Semester 7 report](./) -->
<!-- 2. [Semester 7 slides](./) -->
<!-- 3. [Semester 8 report](./) -->
<!-- 4. [Semester 8 slides](./) -->
<!-- 5. Author 1, Author 2 and Author 3 "Research paper title" (2021). [PDF](./). -->

## Links

[//]: # ( NOTE: EDIT THIS LINKS WITH YOUR REPO DETAILS )

- [Project Repository](https://github.com/cepdnaclk/e19-4yp-Multi-Modal-Data-Fusion-for-Trading-Market-Price-Forecasting)
- [Project Page](https://cepdnaclk.github.io/e19-4yp-Multi-Modal-Data-Fusion-for-Trading-Market-Price-Forecasting/)
- [Department of Computer Engineering](http://www.ce.pdn.ac.lk/)
- [University of Peradeniya](https://eng.pdn.ac.lk/)

[//]: # "Please refer this to learn more about Markdown syntax"
[//]: # "https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet"
