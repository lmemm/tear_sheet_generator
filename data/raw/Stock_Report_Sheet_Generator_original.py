import yfinance as yf
import xlwings as xw
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

wb = xw.Book("Tear Sheet Class.xlsx")
ws = wb.sheets["Sheet1"]
ticker = input("Please enter the stock ticker of the company you're interested in. ")
stock = yf.Ticker(ticker)
stock.info
stock.incomestmt

info_list = [["A1", "shortName"],["R1","symbol"],["C4","industry"],["C5","longBusinessSummary"],["G4","city"],["K4","state"],["P4","fullTimeEmployees"],["D18","currentRatio"],["D19","quickRatio"],["C36","forwardPE"],["R36","marketCap"]]
for i in info_list:
    try:
        ws.range(i[0]).value = stock.info[i[1]]
    except:
        ws.range(i[0]).value = " "

if len(str(stock.info["marketCap"]))>12:
    num = stock.info["marketCap"]/1000000000000
    ws.range("R36").value = f"{num:.2F} T"
elif len(str(stock.info["marketCap"]))>9:
    num = stock.info["marketCap"]/1000000000
    ws.range("R36").value = f"{num:.2F} B"
else:
    num = stock.info["marketCap"]/1000000
    ws.range("R36").value = f"{num:.2F} M"

df = stock.incomestmt
col_names = df.columns.tolist()
if pd.isnull(df.loc["Total Revenue", col_names[-1]]):
    df = df.drop(df.columns[-1], axis=1)

years = []
years = df.columns.sort_values()
df = df.reindex(columns = years)
df = df.T
df

fig = flt.figure(figsize - (4,2))
plt.plot(df.index, df['Total Revenue']/df.loc[df.index[0], 'Total Revenue'])
plt.ylabel('Revenue Growth')
plt.title(f"{ticker} Revenue Growth", fontsize = 14)
plt.xticks(rotation=35)

ws.pictures.add(fig, name = "Revenue", update=True, top=ws.range("A11").top, left = ws.range(A11.left))

































