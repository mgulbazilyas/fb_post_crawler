
# In[1]
import pickle
import re
from random import randint

import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import time
from bs4 import BeautifulSoup as bs
from DocumentRetrievalModel import DocumentRetrievalModel as DRM
from ProcessedQuestion import ProcessedQuestion as PQ
import re
import sys
import mysqldata


with open('title.pickle','rb') as file:
	TITLES = pickle.load(file)
greetPattern = re.compile("^\ *((hi+)|((good\ )?morning|evening|afternoon)|(he((llo)|y+)))\ *$",re.IGNORECASE)

chrome_options = Options()
# chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
chrome_options.add_argument('user-data-dir=user_data')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = Chrome(chrome_options=chrome_options)
driver.get('https://facebook.com')
with open('cookies.pickle','rb') as file:
    cookies = pickle.load(file)

for cookie in cookies:
    cookie.pop('expiry',None)
    driver.add_cookie(cookie)