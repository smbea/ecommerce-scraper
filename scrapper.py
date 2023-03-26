from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from urllib.parse import urlsplit

from scrapper_util import findElement


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
  base_url = urlsplit(url).netloc
  websiteName = base_url.split('.')[1]

  if websiteName == 'asos':
    productInfo = scrapper(driver, url, selectorsCSV.loc['asos'])
    return productInfo

  elif websiteName == 'zalando':
    productInfo = scrapper(driver, url, selectorsCSV.loc['zalando'])
    return productInfo
  
  else:
    return "Not supported yet"


def scrapper(driver, url, selectors):
  driver.get(url)

  try:
    element = EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    WebDriverWait(driver, 5).until(element)
  except TimeoutException:
      print("Timed out waiting for page to load")
      return

  return {
    'title': findElement(driver, selectors["title"], True, None),
    'price': findElement(driver, selectors["price"], True, None),
    'image': findElement(driver, selectors["img"], False, 'src')
  }

def scrapeUrl(url):
  global selectorsCSV

  selectorsCSV = pd.read_csv('./websites.csv')
  selectorsCSV.set_index("website", inplace = True)
  info = get_product_info(url)

  return info