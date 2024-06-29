import json
tickers = ['ABBNY', 'IBM', "RBI.VI", "SIE.DE", "UBSG.SW"]
tickers_to_company = {
    'ABBNY': 'ABB',
    'IBM': 'IBM',
    'RBI.VI': 'Raiffeisen',
    'SIE.DE': 'Siemens',
    'UBSG.SW': 'UBS'

}
import yfinance as yf

# get current directory
import os
path = os.getcwd()
print(path)

for ticker in tickers:
    ticker_info = yf.Ticker(ticker)

    tickerDf_4 = ticker_info.history(period='1d', start="2021-01-01",end=None)
    tickerDf_4_json = tickerDf_4.to_json()
    with open(f'./tools/financials/{tickers_to_company[ticker]}_financialdata_4.json', 'w+') as f:
        json.dump(tickerDf_4_json, f)

    tickerDf_up_to_date = ticker_info.history(period='1d', start="2023-12-29",end=None)
    tickerDf_up_to_date_json_records = tickerDf_up_to_date.to_json(orient="records")
    with open(f'./tools/financials/{tickers_to_company[ticker]}_financial_up_to_date_records.json', 'w+') as f:
        json.dump(tickerDf_up_to_date_json_records, f)
    tickerDf_up_to_date_json = tickerDf_up_to_date.to_json()
    with open(f'./tools/financials/{tickers_to_company[ticker]}_financial_up_to_date.json', 'w+') as f:
        json.dump(tickerDf_up_to_date_json, f)


    tickerDf_old = ticker_info.history(period='1d', start="2021-01-01",end="2023-12-31")
    tickerDf_old_json_records = tickerDf_old.to_json(orient="records")
    with open(f'./tools/financials/{tickers_to_company[ticker]}_financialdata_records.json', 'w+') as f:
        json.dump(tickerDf_old_json_records, f)
    tickerDf_old_json = tickerDf_old.to_json()
    with open(f'./tools/financials/{tickers_to_company[ticker]}_financialdata.json', 'w+') as f:
        json.dump(tickerDf_old_json, f)
