from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

from scrapper_util import findElement, LANGUAGE_CODES


driver = None
selectorsCSV = None

def init_driver():
  options = Options()
  options.headless = True
  options.add_argument('--no-sandbox')
  options.add_argument('--headless')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument("--disable-setuid-sandbox")
  options.add_argument('--disable-gpu')
  options.add_argument("--window-size=1920,1080")
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--allow-running-insecure-content')
  user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005 Safari/537.36"
  options.add_argument(user_agent)

  global driver
  driver = webdriver.Chrome(options=options)
  return driver


def get_product_info(url):

  websiteName = parseUrl(url)
  print("Website name: " + websiteName)

  try: 
    websiteSelector = selectorsCSV.loc[websiteName]
    productInfo = scrapper(driver, url, websiteSelector)
    return productInfo
  except:
    return "Not supported yet"


def scrapper(driver, url, selectors):
  driver.get(url)

  try:
    element = EC.presence_of_element_located((By.CSS_SELECTOR, selectors["img"]))
    WebDriverWait(driver, 5).until(element)
  except TimeoutException:
      print("Timed out waiting for page to load")
      return "Timed out waiting for page to load"
  
  page_source = driver.page_source
  soup = BeautifulSoup(page_source, 'html.parser')

  return {
    'title': findElement(soup, selectors["title"], True, None),
    'price': findElement(soup, selectors["price"], True, None),
    'image': findElement(soup, selectors["img"], False, 'src')
  }

def scrapeUrl(url):
  global selectorsCSV

  selectorsCSV = pd.read_csv('./websites.csv')
  selectorsCSV.set_index("website", inplace = True)
  info = get_product_info(url)

  return info


def parseUrl(url):
  # get hostname
  base_url = urlsplit(url).netloc

  # Remove www. from url
  if base_url.startswith('www.'):
    base_url = base_url[4:]

  # Remove language code from url
  langIndex = base_url.find('.')
  langCode = base_url[:langIndex]

  if (len(langCode) == 2) & (base_url[:langIndex] in LANGUAGE_CODES):
    base_url = base_url[3:]

  # Remove tld from url
  tldIndex = base_url.find('.')
  base_url = base_url[:tldIndex]

  return base_url