import time
import re
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from decimal import *

class ClassName:
    Company = '//div[@class="Lh(20px) Fw(600) Fz(16px) Ell"]'


Options = webdriver.ChromeOptions()
Options.add_argument('--ignore-certificate-errors')
Options.add_argument('--ignore-ssl-errors')
Options.add_argument("--disable-proxy-certificate-handler")
browser = webdriver.Chrome(options = Options)

browser.get("https://tw.stock.yahoo.com/class-quote?sectorId=44&exchange=TAI")
time.sleep(1)
Page = browser.find_element(By.TAG_NAME, 'body')
DataNum = browser.find_element(By.TAG_NAME, 'p')
CompanyListLength = int(re.findall(r'\d++ ', DataNum.text)[0])
Scrolls =  CompanyListLength // 30

while Scrolls:
    Page.send_keys(Keys.END)
    time.sleep(1.2)
    Scrolls-=1
time.sleep(1.2)

Company = browser.find_elements(By.XPATH, '//div[@class="Lh(20px) Fw(600) Fz(16px) Ell"]')  # gets the name of the stock
CompanySymbol = browser.find_elements(By.XPATH, '//div[@class="D(f) Ai(c)"]/span[@class="Fz(14px) C(#979ba7) Ell"]')  # gets the symbol of the stock
SharePrice = browser.find_elements(By.XPATH, '//li[@class="List(n)"]//span[contains(@class, "Jc(fe) Fw(600)")]') # gets the current share price
Records = browser.find_elements(By.XPATH, '//li[@class="List(n)"]//span[@class="Jc(fe)"]')  # open previousClose high low numOfTransactions
FormattedSharePrice = []
FormattedRecords = []

for sharePrice in range(CompanyListLength):
    FormattedSharePrice.append(SharePrice[sharePrice].text.replace(",", ""))

for records in range(len(Records)):
    FormattedRecords.append(Records[records].text.replace(",", ""))


# handling of number of transactions for those without data is yet to be handled
# problem: the - sign is not under <span class="Jc(Fe)"></span>, instead, it's under the parent <div> with a different classname from those data with numbers


List = np.reshape(FormattedRecords, (-1, 5))     # making the incoming data as an n by 5 list where the 5 data are that of Records

for company in range(CompanyListLength):
    print(Company[company].text , " " ,  CompanySymbol[company].text[0:4], " ", SharePrice[company].text, " ", Decimal(float(FormattedSharePrice[company]) - float(List[company, 1])).quantize(Decimal('.01'), rounding=ROUND_HALF_UP) , " " , Decimal((float(FormattedSharePrice[company]) - float(List[company, 1])) / float(List[company, 1]) * 100).quantize(Decimal('.01'), rounding=ROUND_HALF_UP),  "% ", sep = "", end = "")
    for data in range(5):       # the 5 Records return
        print(List[company, data] , " ", sep = "", end = "")
    print("\n")


browser.close()