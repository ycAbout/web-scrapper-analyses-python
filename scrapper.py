#For get url, 
import urllib
import time
#For scrapping
from bs4 import BeautifulSoup
#For plot
import matplotlib.pyplot as plt

from scipy import stats
import numpy as np


symbols = [
  'https://www.nasdaq.com/symbol/fb',
  'https://www.nasdaq.com/symbol/aapl',
  'https://www.nasdaq.com/symbol/msft',
  'https://www.nasdaq.com/symbol/googl',
  'https://www.nasdaq.com/symbol/tsla',
  'https://www.nasdaq.com/symbol/intc',
  'https://www.nasdaq.com/symbol/amzn',
]

#for downloaded data files
fileName = [
    './data/HistoricalQuotes.FB.csv',
    './data/HistoricalQuotes.MSFT.csv',
    './data/HistoricalQuotes.AAPL.csv',
    './data/HistoricalQuotes.TSLA.csv',
    './data/HistoricalQuotes.GOOGL.csv',
]


def getHistory(link):
  """take in a link corresponding to history price
  return a list with history price [[date, open, high, low, close, volume],...]
  """
  historyPage = urllib.request.urlopen(link)
  soup = BeautifulSoup(historyPage,'html.parser')
  #get the history price table for last three months
  table = soup.find(id="historicalContainer").table
  body = table.tbody
  row = []
  historyPrice = []
  for string in body.stripped_strings:
    row.append(string)
    # every row tr contains 6 td elements
    if len(row) == 6:
      #using copy to generate a new list, otherwise list will be cleared.
      historyPrice.append(row.copy())  
      row.clear()
  return historyPrice

def plot(name, x,y):
  """take in list x and list y to make a plot
  print a plot
  """
  x = np.array(x)
  y = np.array(y)
  plt.plot(x, y)
  plt.title(name)
  plt.ylabel('price')
  plt.xlabel('days before')

  #liner regression
  slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
  plt.plot(x, intercept + slope*x, 'r', label='fitted line')

  plt.show()

def loadData():
  """ load Data in
  DisPlay a plot
  """
  for file in fileName:
    historyPrice = np.loadtxt(file, dtype=str, delimiter=",", skiprows=1)
    # x for trading days
    x = []
    for i in range(len(historyPrice)):
      x.append(0-i)
    # y for price    
    y = []
    for item in historyPrice:
      y.append(float(item[4].replace('"', '')))
    plot(file, x, y)


def main():
  for symbol in symbols:
    page = urllib.request.urlopen(symbol)
    soup = BeautifulSoup(page,'html.parser')
  
    name = soup.find(id="qwidget_pageheader").get_text().split(' ')[0]
      
    #last sale price
    price = soup.find(id="qwidget_lastsale").get_text()
    print(name, price)
  #  time.sleep(1)
    historyLink = soup.find(id="historical_quoteslink").get('href')
    historyPrice = getHistory(historyLink)
    # x into trading days before the current trading day
    x = []
    for i in range(len(historyPrice)):
      x.append(0-i)
    # y for price    
    y = []
    for item in historyPrice:
      y.append(float(item[4].replace(',', '')))
#    y = list(reversed(y))
    plot(name, x,y)

#main()
loadData()
