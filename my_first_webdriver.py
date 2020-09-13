#following script opens up your first webdriver browser and goes to the specified link
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.google.com/')

