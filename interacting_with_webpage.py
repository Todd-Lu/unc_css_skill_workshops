#in this script, we are going to do various things to interact with a webpage

from selenium import webdriver

beginning_url = 'https://flps.newberry.org/'
driver = webdriver.Chrome()
driver.get(beginning_url)


# now let us try to locate elements, and select data from these elements
# https://selenium-python.readthedocs.io/locating-elements.html

my_css_selector = ''
element = driver.find_element_by_css_selector(my_css_selector)

element.text
element.get_attribute('href')
       
#we can move the page (first number is x axis, second number is y axis)
driver.execute_script('window.scrollTo(0, 500)')
                                    

#we can search in search bars
searchbar = driver.find_element_by_css_selector('#search_terms')
searchbar.send_keys('Poland')                                                
                                    
# AND we can click buttons
searchbutton = driver.find_element_by_css_selector('#search_button')
searchbutton.click()               

#don't forget to close the driver
driver.close()