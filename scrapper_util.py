from selenium.webdriver.common.by import By

def findElement(driver, selector, text, attributeToGet):
  element = driver.find_element(By.CSS_SELECTOR, selector)

  if(text):
    return element.text
  elif(attributeToGet):
    return element.get_attribute(attributeToGet)
