#!pip install git+https://github.com/akhils19/yfinance.git

import numpy as np
import pandas as pd
import yfinance as yf
import statistics as stats
import tqdm

def get_gscore(symbol,df,market='NSE',download = False):
    
    '''
    
    This function finds the gscores 1-7 for Companies in NYSE, NSE and BSE.
    
    Input: 
    1) symbol: List of Company symbol depending on the markets, NYSE, NSE and BSE.('List')
    2) df: Dataframe where you want the final GScores concatenated
    3) market: Market name ('NSE','NYSE','BSE')('String')
    4) Download: Bool. If true, csv will get downloaded
    
    Output:
    1) Netincome (G1 Score)
    2) Total Assets (G1 Score)
    3) CFROA (G2 Score)
    4) VARROA (G3 Score)
    5) VARSGR (G4 Score)
    6) RDINT (G5 Score)
    7) CAPINT (G6 Score)
    8) price to market ratio
    
    G Scores:
    1) G1: Return on Assets (ROA = Net Income/ Total Assets) > Industry Median
    2) G2: Cash Flow from Operating Activities (CFROA) > Industry Median
    3) G3: Comparison ROA and CFROA (CFROA > ROA)
    4) G4: Variance of ROA (VARROA) < Industry Median
    5) G5: Variance in annual sales growth(VARSGR) < Industry Median
    6) G6: Research and Development Investment Scaled by Total Assets (RDINT) > Industry Median
    7) G7: Capital Expenditure Scaled by Total Assets (CAPINT) > Industry Median
    8) G8: Advertising Expenses Scaled by Total Assets (ADINT) > Industry Median
    
    NOTE: Advertising Expense (G8) is not calculated in this function since the information is not available in the APIs. 
    
    '''
    
    global netincome 
    global totalassets 
    global cfroa 
    global varroa 
    global varsgr 
    global rdint 
    global capint 
    global b2m 
    
    netincome = []
    totalassets = []
    cfroa = []
    varroa = []
    varsgr = []
    rdint = []
    capint = []
    b2m = []
    
    if market.upper() == 'NSE':
        
        comp = yf.Ticker(symbol[0]+'.ns')
        print('Years Available')
        for n in list(comp.get_financials(freq='yearly').columns):
            print(n.date())

        r = str(input('Enter the date'))
        for a,i in tqdm.tqdm(enumerate(symbol)):
            
            #initiating ticker
            comp = yf.Ticker(i+'.ns')
             
            try:
                #netincome
                netincome.append(comp.get_financials(freq='yearly').loc['Net Income',r][0])
            except:
                netincome.append(None)
            finally:
                try:
                    #total assets
                    totalassets.append(comp.get_balancesheet(freq='yearly').loc['Total Assets',r][0])
                except:
                     totalassets.append(None)
                finally:
                    try:
                        #cfroa
                        cfroa.append(comp.get_cashflow(freq='yearly').loc['Total Cash From Operating Activities',r][0])
                    except:
                        cfroa.append(None)
                    finally:
                        try:
                            #varroa
                            netincome_varroa = []
                            totalassets_varroa = []

                            date_list = []
                            
                            for m in comp.get_financials(freq='yearly').columns:
                                date_list.append(str(m.date()))

                            for o in range(date_list.index(r),len(date_list)-1):
                                netincome_varroa.append(comp.get_financials(freq='yearly').loc['Net Income',date_list[o]][0])
                                totalassets_varroa.append(comp.get_balancesheet(freq='yearly').loc['Total Assets',date_list[o]][0])

                            varroa.append(stats.variance(list(np.array(netincome_varroa)/np.array(totalassets_varroa))))
                        except:
                            varroa.append(None)
                        
                        finally:
                            try:
                                #varsgr
                                date_list = []
                                for p in comp.get_financials(freq='yearly').columns:
                                    date_list.append(str(p.date()))

                                intermidate_list = []
                                for q in range(date_list.index(r),len(date_list)-1):
                                    intermidate_list.append(comp.get_financials(freq='yearly').loc['Total Revenue',date_list[q]][0])

                                rev_list = []
                                for t in range(len(intermidate_list)-1):
                                    rev_list.append(((intermidate_list[t] - intermidate_list[t+1])/intermidate_list[t+1])*100)

                                varsgr.append(stats.variance(rev_list))
                            except:
                                varsgr.append(None)
                            finally:
                                try:    
                                    #rdint
                                    rdint.append(comp.get_financials(freq='yearly').loc['Research Development',r][0])
                                except:
                                    rdint.append(None)
                                finally:
                                    try:
                                        #capint
                                        capint.append(comp.get_cashflow(freq='yearly').loc['Capital Expenditures',r][0])
                                    except:
                                        capint.append(None)
                                    finally:
                                        try: 
                                            #book to market ratio
                                            b2m.append(1/(comp.get_info(freq='yearly').get('priceToBook')))
                                        except:
                                            b2m.append(None)
    if  market.upper() == 'NYSE': 

        comp = yf.Ticker(symbol[0])
        print('Years Available:')
        for n in list(comp.get_financials(freq='yearly').columns):
            print(n.date())
        r = str(input('Enter the date'))
        for a,i in tqdm.tqdm(enumerate(symbol)):
            
            #initiating ticker
            comp = yf.Ticker(i+'.ns')
            
            try:
                #netincome
                netincome.append(comp.get_financials(freq='yearly').loc['Net Income',r][0])
            except:
                netincome.append(None)
            finally:
                try:
                    #total assets
                    totalassets.append(comp.get_balancesheet(freq='yearly').loc['Total Assets',r][0])
                except:
                    totalassets.append(None)
                finally:
                    try:
                        #cfroa
                        cfroa.append(comp.get_cashflow(freq='yearly').loc['Total Cash From Operating Activities',r][0])
                    except:
                        cfroa.append(None)
                    finally:
                        try:
                            #varroa
                            netincome_varroa = []
                            totalassets_varroa = []

                            date_list = []
                            
                            for m in comp.get_financials(freq='yearly').columns:
                                date_list.append(str(m.date()))

                            for o in range(date_list.index(r),len(date_list)-1):
                                netincome_varroa.append(comp.get_financials(freq='yearly').loc['Net Income',date_list[o]][0])
                                totalassets_varroa.append(comp.get_balancesheet(freq='yearly').loc['Total Assets',date_list[o]][0])

                            varroa.append(stats.variance(list(np.array(netincome_varroa)/np.array(totalassets_varroa))))
                        except:
                            varroa.append(None)
                        
                        finally:
                            try:
                                #varsgr
                                date_list = []
                                for p in comp.get_financials(freq='yearly').columns:
                                    date_list.append(str(p.date()))

                                intermidate_list = []
                                for q in range(date_list.index(r),len(date_list)-1):
                                    intermidate_list.append(comp.get_financials(freq='yearly').loc['Total Revenue',date_list[q]][0])

                                rev_list = []
                                for t in range(len(intermidate_list)-1):
                                    rev_list.append(((intermidate_list[t] - intermidate_list[t+1])/intermidate_list[t+1])*100)

                                varsgr.append(stats.variance(rev_list))
                            except:
                                varsgr.append(None)
                            finally:
                                try:    
                                    #rdint
                                    rdint.append(comp.get_financials(freq='yearly').loc['Research Development',r][0])
                                except:
                                    rdint.append(None)
                                finally:
                                    try:
                                        #capint
                                        capint.append(comp.get_cashflow(freq='yearly').loc['Capital Expenditures',r][0])
                                    except:
                                        capint.append(None)
                                    finally:
                                        try: 
                                            #book to market ratio
                                            b2m.append(1/(comp.get_info(freq='yearly').get('priceToBook')))
                                        except:
                                            b2m.append(None)

    df['Net Income'] = np.array(netincome)
    df['Total Assets'] = np.array(totalassets)
    df['CFROA'] = np.array(cfroa)
    df['VARROA'] = np.array(varroa)
    df['VARSGR'] = np.array(varsgr)
    df['RDINT'] = np.array(rdint)
    df['CAPINT'] = np.array(capint)
    df['Book to Market Ratio'] = np.array(b2m)

    df['Net Income'] = df['Net Income'].fillna(np.nan)
    df['Total Assets'] = df['Total Assets'].fillna(np.nan)
    df['CFROA'] = df['CFROA'].fillna(np.nan)
    df['VARROA'] = df['VARROA'].fillna(np.nan)
    df['VARSGR'] = df['VARSGR'].fillna(np.nan)
    df['RDINT'] = df['RDINT'].fillna(np.nan)
    df['CAPINT'] = df['CAPINT'].fillna(np.nan)
    df['Book to Market Ratio'] = df['Book to Market Ratio'].fillna(np.nan)

    df['ROA'] = df['Net Income']/df['Total Assets']
    df['G1'] = np.where(df['ROA'] > stats.median(df['ROA']),1,0)
    df['G1'] = np.where(df['ROA'].isna(),np.nan,df['G1'])

    df['G2'] = np.where(df['CFROA'] > stats.median(df['CFROA']),1,0)
    df['G2'] = np.where(df['CFROA'].isna(),np.nan,df['G2'])

    df['G3'] = np.where(df['CFROA']>df['ROA'],1,0)
    df['G3'] = np.where(df['CFROA'].isna()|df['ROA'].isna() ,np.nan,df['G3'])

    df['G4'] = np.where(df['VARROA'] < stats.median(df['VARROA']),1,0)
    df['G4'] = np.where(df['VARROA'].isna(),np.nan,df['G4'])

    df['G5'] = np.where(df['VARSGR'] < stats.median(df['VARSGR']),1,0)
    df['G5'] = np.where(df['VARSGR'].isna(),np.nan,df['G5'])

    df['G6'] = np.where(df['RDINT'] > stats.median(df['RDINT']),1,0)
    df['G6'] = np.where(df['RDINT'].isna(),np.nan,df['G6'])

    df['G7'] = np.where(df['CAPINT'] > stats.median(df['CAPINT']),1,0)
    df['G7'] = np.where(df['CAPINT'].isna(),np.nan,df['G7'])

    if download:
        df.to_csv ('gcore.csv', index = False)

    return df

if __name__ == '__main__':
    get_gscore(symbol,df,market='NSE')