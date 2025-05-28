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
8. [High Level Design Architecture](#high-level-design-architecture)
9. [Links](#links)
<!-- 10. [Results and Analysis](#results-and-analysis)
11. [Conclusion](#conclusion)
12. [Publications](#publications)
13. [Links](#links) -->

---

<!-- 
DELETE THIS SAMPLE before publishing to GitHub Pages !!!
This is a sample image, to show how to add images to your page. To learn more options, please refer [this](https://projects.ce.pdn.ac.lk/docs/faq/how-to-add-an-image/)
![Sample Image](./images/sample.png) 
-->


## Abstract
   This research proposes a machine learning approach to accurately distinguish genuine breakouts from false signals (fakeouts) in financial markets, focusing on gold (XAU/USD) trading. By combining historical price data, trading volume, and macroeconomic factors through multi-modal data fusion, the model aims to improve breakout classification and enhance trading decisions. Using data from platforms like MetaTrader 5 and Binance API, along with economic reports, the system employs deep learning models (e.g., LSTM or Transformer) to capture complex market patterns influenced by both technical and external economic factors. This approach seeks to help traders identify high-probability trading opportunities, reduce risks, and optimize profitability amid volatile market conditions.

## Background and Motivation
   Highlights the importance of stock market forecasting for reducing risk and improving trading strategies in a $110 trillion global market influenced by factors like interest rates, inflation, and employment data. Traditional technical analysis methods often fall short, leading to high retail trader losses. Advances in machine learning enable analysis of large datasets and complex patterns, especially when integrating macroeconomic indicators that can predict market shifts. The study aims to develop a comprehensive prediction framework that combines historical data, market patterns, and macroeconomic factors to enhance accuracy and provide traders with actionable, data-driven insights for better decision-making.

## Problem Statement
   Accurate prediction of tradable moments, entry prices, and exit points remains a significant challenge in financial markets, particularly in volatile assets like gold (XAU/USD). Traditional forecasting models, which mainly rely on historical price data and technical indicators, fail to capture the complex interplay between market behavior and external macroeconomic factors, such as inflation, employment rates, and interest rate fluctuations. These models over-rely on historical data while neglecting the critical influence of macroeconomic indicators, leading to inaccurate predictions and missed opportunities. Additionally, they fail to account for the interdependencies between market trends and external economic conditions, resulting in fragmented insights. Existing approaches often analyze time series data in isolation, and the lack of an integrated, multi-modal framework that combines historical price patterns with macroeconomic contexts further limits the precision and adaptability of predictive tools.

## Research Gap
   Current trading price forecasting models face several key limitations: they mostly rely on price data and technical indicators, often ignoring important macroeconomic factors; they lack effective mechanisms to control traders’ emotional biases like FOMO or panic selling; and they suffer from poor interpretability, making it hard for traders to trust AI predictions. Additionally, many models fail to adapt to different market regimes (bull, bear, sideways), reducing their accuracy during volatile or shifting conditions. Addressing these gaps requires multi-modal, emotionally aware, interpretable, and adaptive machine learning models for more reliable trading forecasts.

## Aim
   The aim of this research is to forecast trading moments, entry prices, and exit prices for gold (XAU/USD) by analyzing the relationship between historical price movement patterns, market trading volume, and key macroeconomic indicators such as CPI, GDP, PPI, PCE, NFP, and interest rates. The research seeks to develop a multi-modal machine learning framework that enhances the predictive accuracy of trading decisions by integrating these factors.

## Proposed Solution
   Introduces a multi-modal machine learning framework to improve financial forecasting by integrating historical price data, trading volume, and macroeconomic factors. Using deep learning, the model analyzes price trends and volume to gauge trend strength, while incorporating economic indicators like inflation and interest rates to capture external influences. It also predicts optimal stop-loss levels to enhance risk management during market volatility. This comprehensive approach aims to deliver more accurate, transparent, and data-driven trade entry and exit predictions, addressing existing model limitations and supporting better decision-making in complex markets.


## Research Methodology
## Data Collection
   A robust dataset is critical for accurate price forecasting. Our approach involves gathering data from multiple sources:
![image](https://github.com/user-attachments/assets/b5c70746-40e8-4829-bee0-0574fd6200b3)

• Gold Price Data (XAU/USD): We will collect historical XAU/USD OHLCV (Open, High, Low, Close, Volume) data across multiple timeframes (30-minute, hourly, 4-hourly, daily, weekly, and monthly) using the MetaTrader5 local terminal. This ensures we capture both short-term fluctuations and long-term trends. The data will cover the period from 2015 to 2025.

• Macroeconomic Indicators: These fundamental factors drive long-term price movements and market sentiment. We will focus on: Interest Rate (Federal Reserve Rate): Determines monetary policy direction, Consumer Price Index (CPI): Reflects inflationary pressures, Non-Farm Payrolls (NFP): Measures employment trends and economic health, Personal Consumption Expenditures (PCE): Tracks consumer spending behavior, Gross Domestic Product (GDP): Indicates overall economic growth, Producer Price Index (PPI): Represents inflation at the producer level.

![image](https://github.com/user-attachments/assets/78e5ca5d-ad3b-421d-be31-4a51218f8d43)

   Integration Strategy: Web scraping from Investing.com and manually extracting Federal Reserve statements. Data will be collected for the 2015-2025 range to cover multiple economic cycles.

![image](https://github.com/user-attachments/assets/bd5ce218-da41-4a8f-ba0a-21d3337c15b7)

![image](https://github.com/user-attachments/assets/4e11ccc9-2616-4ab9-8003-94152994f61e)


## High Level Design Architecture
![image](https://github.com/user-attachments/assets/9b8eefca-db8a-41fe-af5d-1e4e24cac0e8)

<!-- ## Results and Analysis

## Conclusion

## Publications
[//]: # "Note: Uncomment each once you uploaded the files to the repository" -->

<!-- 1. [Semester 7 report](./) -->
<!-- 2. [Semester 7 slides](./) -->
<!-- 3. [Semester 8 report](./) -->
<!-- 4. [Semester 8 slides](./) -->
<!-- 5. Author 1, Author 2 and Author 3 "Research paper title" (2021). [PDF](./). -->

Access to our research mid presentation - [Mid Presentations](https://www.canva.com/design/DAGfhXIfCuo/P01LSTdVM6jMf4dF3Pbf0w/edit)

## Links

[//]: # ( NOTE: EDIT THIS LINKS WITH YOUR REPO DETAILS )

- [Project Repository](https://github.com/cepdnaclk/e19-4yp-Multi-Modal-Data-Fusion-for-Trading-Market-Price-Forecasting)
- [Project Page](https://cepdnaclk.github.io/e19-4yp-Multi-Modal-Data-Fusion-for-Trading-Market-Price-Forecasting/)
- [Department of Computer Engineering](http://www.ce.pdn.ac.lk/)
- [University of Peradeniya](https://eng.pdn.ac.lk/)

[//]: # "Please refer this to learn more about Markdown syntax"
[//]: # "https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet"
