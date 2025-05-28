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

1. [Abstract](#abstract)
2. [Background and Motivation](#background-and-motivation)
3. [Problem Statement](#problem-statement)
4. [Research Gap](#research-gap)
5. [Aim](#aim)
6. [Proposed Solution](#proposed-solution)
7. [Research Methodology](#research-methodology)
  7.1 [Data Collection](#data-collection)
9. [Experiment Setup and Implementation](#experiment-setup-and-implementation)
10. [Results and Analysis](#results-and-analysis)
11. [Conclusion](#conclusion)
12. [Publications](#publications)
13. [Links](#links)

---

<!-- 
DELETE THIS SAMPLE before publishing to GitHub Pages !!!
This is a sample image, to show how to add images to your page. To learn more options, please refer [this](https://projects.ce.pdn.ac.lk/docs/faq/how-to-add-an-image/)
![Sample Image](./images/sample.png) 
-->


## Abstract
Accurately predicting tradable moments, price entry and exit points, and managing risks is crucial in today’s highly volatile financial markets. Macroeconomic fluctuations and geopolitical factors significantly impact asset prices, making it essential for traders and financial analysts to identify reliable opportunities. Gold (XAU/USD) remains a preferred asset due to its high liquidity and resilience against market manipulation. However, traditional technical analysis methods often struggle to differentiate between genuine breakouts and false signals, leading to inefficient trading decisions and increased risk exposure.

This research develops a machine learning-based approach to distinguishing breakouts from fakeouts by analyzing key market factors. The model takes historical price data, trading volume,    macroeconomic data as inputs. By leveraging multi-modal data fusion, the system captures the relationships between market structure and external economic events to enhance breakout classification. Traders and financial analysts can use this system to improve decision-making by identifying high-probability tradable opportunities while minimizing false signals.

The implementation involves collecting data from trading platforms (MetaTrader 5, Binance API) and economic reports, performing feature engineering, and training a deep learning model—such as LSTM or Transformer—to recognize breakout patterns. By integrating technical and macroeconomic factors, this research aims to provide a data-driven framework for traders to make more informed decisions, reduce risks, and optimize profitability in financial markets.


## Background and Motivation
Stock market forecasting is critical for investors and institutions due to its potential to reduce risk and optimize trading strategies. The global financial market, valued at over $110 trillion, is highly sensitive to factors such as interest rates, inflation, and employment statistics. Despite its importance, many investors still depend on conventional technical analysis methods, such as moving averages and candlestick patterns, which often fail to account for sudden market shifts. Research indicates that approximately 70–90% of retail traders incur losses due to emotional trading and insufficient analytical tools.

Advancements in machine learning have opened new possibilities by analyzing large datasets to detect complex patterns beyond human capability. Recent studies emphasize that integrating macroeconomic factors into analytical models can significantly improve prediction accuracy, as these indicators often precede market movements. However, many existing solutions are limited by their reliance on singular data sources or rigid models.
The motivation for this research is to address these gaps by creating a comprehensive prediction framework that utilizes multiple data types—historical trends, market patterns, and macroeconomic conditions—to improve accuracy and support data-driven trading decisions. The proposed solution aims to empower traders with actionable insights that combine multiple perspectives into a cohesive prediction strategy.

## Problem Statement
Accurate prediction of tradable moments, entry prices, and exit points remains a significant challenge in financial markets, particularly in volatile assets like gold (XAU/USD). Traditional forecasting models, which mainly rely on historical price data and technical indicators, fail to capture the complex interplay between market behavior and external macroeconomic factors, such as inflation, employment rates, and interest rate fluctuations. These models over-rely on historical data while neglecting the critical influence of macroeconomic indicators, leading to inaccurate predictions and missed opportunities. Additionally, they fail to account for the interdependencies between market trends and external economic conditions, resulting in fragmented insights. Existing approaches often analyze time series data in isolation, and the lack of an integrated, multi-modal framework that combines historical price patterns with macroeconomic contexts further limits the precision and adaptability of predictive tools.

## Research Gap
The current landscape of trading market price forecasting is limited by several key gaps, particularly in the integration of multi-modal data. Most existing models predominantly rely on price data and technical indicators, often overlooking crucial factors like macroeconomic events. Real-world trading decisions are influenced by a broad array of factors beyond just price action, and failing to incorporate these elements leads to incomplete and less reliable predictions.

Another significant gap is the lack of sentiment control in trading models. Many traders make decisions based on emotional reactions like fear-of-missing-out (FOMO) or panic selling, which can result in irrational choices. While some models incorporate sentiment analysis, they do not actively help control emotional biases. There is a need for machine learning models that can effectively filter out irrational noise and assist traders in making more data-driven, objective decisions. Additionally, a major challenge is the poor interpretability of AI models such as LSTMs and transformers. While these models may offer good predictive accuracy, they often lack transparency, making them difficult for traders to trust when making critical decisions. Without clear explanations behind model predictions, traders may struggle to rely on these AI-driven insights effectively.

Another limitation is the inability of many existing models to adapt to different market conditions. Most trading models are trained on historical data without considering the influence of market regimes (bullish, bearish, sideways), leading to struggles during market shifts or periods of high volatility. Developing adaptive models that can adjust to varying market conditions is crucial for maintaining accuracy and reliability.

## Aim
The aim of this research is to forecast trading moments, entry prices, and exit prices for gold (XAU/USD) by analyzing the relationship between historical price movement patterns, market trading volume, and key macroeconomic indicators such as CPI, GDP, PPI, PCE, NFP, and interest rates. The research seeks to develop a multi-modal machine learning framework that enhances the predictive accuracy of trading decisions by integrating these factors.

## Proposed Solution
This research proposes a multi-modal machine learning framework designed to address the limitations of existing financial forecasting models by predicting trade entry and exit prices through the integration of historical data analysis, market trading volume, and macroeconomic factor assessment. The solution aims to leverage advanced machine learning techniques to enhance predictive accuracy and decision-making transparency.

The framework will incorporate deep learning models to analyze historical price trends and use market trading volume to assess the strength of price trends. Additionally, macroeconomic analysis will capture the impact of external factors, such as inflation rates, employment statistics, and interest rate fluctuations, on market price movements.

To enhance risk management, the model will predict optimal stop-loss levels, minimizing trading losses during market volatility. This comprehensive approach will enable traders to make data-driven decisions by combining multiple perspectives into a cohesive prediction strategy. By integrating these elements, the proposed solution aims to bridge research gaps and provide a robust tool for navigating complex financial markets.


## Research Methodology
## Data Collection
A robust dataset is critical for accurate price forecasting. Our approach involves gathering data from multiple sources:
![image](https://github.com/user-attachments/assets/b5c70746-40e8-4829-bee0-0574fd6200b3)

• Gold Price Data (XAU/USD): We will collect historical XAU/USD OHLCV (Open, High, Low, Close, Volume) data across multiple timeframes (30-minute, hourly, 4-hourly, daily, weekly, and monthly) using the MetaTrader5 local terminal. This ensures we capture both short-term fluctuations and long-term trends. The data will cover the period from 2015 to 2025.
• Macroeconomic Indicators: These fundamental factors drive long-term price movements and market sentiment. We will focus on:
•	Interest Rate (Federal Reserve Rate): Determines monetary policy direction.
•	Consumer Price Index (CPI): Reflects inflationary pressures.
•	Non-Farm Payrolls (NFP): Measures employment trends and economic health.
•	Personal Consumption Expenditures (PCE): Tracks consumer spending behavior.
•	Gross Domestic Product (GDP): Indicates overall economic growth.
•	Producer Price Index (PPI): Represents inflation at the producer level.

Integration Strategy: Web scraping from Investing.com and manually extracting Federal Reserve statements. Data will be collected for the 2015-2025 range to cover multiple economic cycles.

![image](https://github.com/user-attachments/assets/bd5ce218-da41-4a8f-ba0a-21d3337c15b7)

![image](https://github.com/user-attachments/assets/4e11ccc9-2616-4ab9-8003-94152994f61e)


## Experiment Setup and Implementation

## Results and Analysis

## Conclusion

## Publications
[//]: # "Note: Uncomment each once you uploaded the files to the repository"

<!-- 1. [Semester 7 report](./) -->
<!-- 2. [Semester 7 slides](./) -->
<!-- 3. [Semester 8 report](./) -->
<!-- 4. [Semester 8 slides](./) -->
<!-- 5. Author 1, Author 2 and Author 3 "Research paper title" (2021). [PDF](./). -->


## Links

[//]: # ( NOTE: EDIT THIS LINKS WITH YOUR REPO DETAILS )

- [Project Repository](https://github.com/cepdnaclk/repository-name)
- [Project Page](https://cepdnaclk.github.io/repository-name)
- [Department of Computer Engineering](http://www.ce.pdn.ac.lk/)
- [University of Peradeniya](https://eng.pdn.ac.lk/)

[//]: # "Please refer this to learn more about Markdown syntax"
[//]: # "https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet"
