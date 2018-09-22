#For get url, 
import urllib
import time
#For scrapping
from bs4 import BeautifulSoup

symbols = [
  'https://www.nasdaq.com/symbol/fb',
  'https://www.nasdaq.com/symbol/aapl',
  'https://www.nasdaq.com/symbol/msft',
  'https://www.nasdaq.com/symbol/googl',
  'https://www.nasdaq.com/symbol/tsla',
  'https://www.nasdaq.com/symbol/intc',
  'https://www.nasdaq.com/symbol/amzn',
]

for symbol in symbols:
  page = urllib.request.urlopen(symbol)
  soup = BeautifulSoup(page,'html.parser')

  name = soup.find(id="qwidget_pageheader").get_text().split(' ')[0] + '               '
    
  #last sale price
  price = soup.find(id="qwidget_lastsale").get_text()
  print(name[:15], price)
  time.sleep(1)
