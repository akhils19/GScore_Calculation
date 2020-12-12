# G Score Calculation
G Score is a technique used for analysing the investability of a company. This work as been built on the paper [Separating Winners from Losers Among Low Book-to-Market Stocks Using Financial Statement Analysis](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=403180) by Partha S. Mohanram. This paper proposes criterias ranging from profitability and cash flows to earning varibiabilities and accounting conservatism to calculate a parameter called G Score which would help separate out investable companies amongst the low book to market ratios companies. 

## Methodology
---
8 criterias are considered in G Score Calculation.
- G1 - Return on Asset (ROA): Ability of the company to generate profit from its Assets. If ROA > Industry Median, GScore1(G1) = 1, else 0.
```math
                    ROA = Net Income / Total Assets
```
- G2 - Cash Flow from Operating Activities (CFROA): Cash generated during the ongoing operation of the company. If CFROA > Industry Median, G2 = 1, else 0.
- G3 - Comparison between CFROA and ROA. If CFROA > ROA, then G3 = 1, else 0.
- G4 - Variance of ROA (VARROA): Variance of ROAs from past 3 to 5 years of a company. If VARROA < Ind. Median, G4 = 1, else 0.
- G5 - Variance in Annual Sales Growth (VARSGR): Variance in Annnual Sales Growth from past 3 to 5 years of a company. If VARSGR < Ind. Median, G5 = 1, else 0.
- G6 - Research and Developmemt Investment scaled by Total Assets (RDINT): If RDINT > Ind. Median, G6 = 1, else 0.
- G7 - Capital expenditure scaled by Total Assets (CAPINT): If CAPINT > Ind. Median, G7 = 1, else 0. 
- G8 - Advertising Expense scaled by Total Assets (ADINT): If ADINT > Ind. Median, G7 = 1, else 0.

## Installation 
---
 
```python
pip install git+https://github.com/akhils19/yfinance.git
```

## Usage
---
This script built on top of yfinance package with slight modification. 

Clone this repo.

```python
from GScore import get_gscore

df_gscore = get_gscore(list(df['SYMBOL']),df,market='NSE',download = False)
```
Input: 
1) symbol: List of Company symbol depending on the markets, NYSE, NSE and BSE.('List')
2) df: Dataframe where you want the final GScores concatenated ('Dataframe')
3) market: Market name ('NSE','NYSE','BSE')('String')
4) download: If true, csv will get downloaded ('Bool')

Output: G1-7 calculated and concatenated to the dataframe with the inputted gcode 

## Things to keep in mind
---
- Ensure the list of tickers inputted is equal to the length of dataframe.
- This is script is still at its preliminary stage. Not all features may be accessible.
- When date is asked to be inputted, write the date in the same format as displayed.

## Status
---
**Version 1.0.0**
- Script Under Development but can be used for certain fundamental analysis. 
- The criteria are not compared to the industry median but to the median of all the tickers inputted. 
- BSE market information is to be added. 
- RDINT is not available on any APIs, so that data is not available yet. 
