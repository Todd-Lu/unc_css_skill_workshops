from selenium import webdriver
import urllib.request
import time
#this script illustrates a few problems that could come up with webscraping
#and it demonstrates how to diagnose these problems and avoid issues


# ROBOTS.TXT FILE, access the following link:
# https://www.youtube.com/robots.txt
# More explanation here: https://www.robotstxt.org/robotstxt.html
 

# READING SELENIUM DOCUMENTATION
# https://selenium-python.readthedocs.io/index.html


# IMPORTANCE OF USER AGENT STRINGS
def chromeprofile():
    options = webdriver.ChromeOptions()
    #notice here I am explicilty setting a user agent string, in this case firefox
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0')
    driver = webdriver.Chrome(options=options)
    return driver

driver = chromeprofile()
driver.get('https://dps.hawaii.gov/blog/2020/03/17/coronavirus-covid-19-information-and-resources/')

#note: the following css selector does not seem to be stable...
img_element = driver.find_element_by_css_selector('.primary-content > p:nth-child(19) > a:nth-child(1)')

output_url = img_element.get_attribute('href')
print(output_url)

# let's try downloading this image, using the urllib.request library (different one from selenium)

    #set the path where you want the file to be
filename = 'example.jpg'
urllib.request.urlretrieve(output_url, filename)

# the above code apparently did not work -- we got an error as we were forbidden access
# so, we have to set a user agent string 
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0')]
urllib.request.install_opener(opener)    
urllib.request.urlretrieve(output_url, filename)

# after each browser session, you should close your driver
driver.close()

# PAUSING YOUR SCRIPT

    #learn to pause your script, occasionally to avoid being detected for abnormal behavior
beginning_url = 'https://flps.newberry.org/'
driver = webdriver.Chrome()
driver.get(beginning_url)

# wait for 5 seconds
time.sleep(5)
max_pages = 20

for page_num in range(2, max_pages):
    
    #make sure to print statements to know location of where your script breaks!
    print('Accessing page: ' + str(page_num))
    
    #accesses the next page
    next_page_element = driver.find_element_by_partial_link_text('Next')
    next_page_element.click()

    #do something on the page (collect data)

    # % means get the remainder when you the left number from the right number
    #in this case, we mean if page_num is divisble by 5, then let's take a break for 30 seconds
    if page_num % 5 == 0:
        print('Taking a 5 second breather!')
        time.sleep(5)
        
driver.close()


# IMPLICIT AND EXPLICIT WAITS
    #selenium has in built methods called implicit and explicit waits
    #these methods are used because sometimes only parts of websites load when you open up a page
    #explicit waits: tells the command to wait for a specified amount of time when trying to access a specific element (waits for it to load)
    #implicit waits: tells the entire page to wait for a certain amount of time

#some library imports needed for explicit waits
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 


# SOMETIMES only parts of websites load, so have to scroll down the website, and then specify my waiting to access certain elements
#for whatever reason, in the following website some images don't load unless you scroll down in the browser
driver = webdriver.Chrome()
driver.get("https://medium.com/@MichiganDOC/mdoc-takes-steps-to-prevent-spread-of-coronavirus-covid-19-250f43144337")  

#we can move the page (first number is x axis, second number is y axis)
driver.execute_script('window.scrollTo(0, 500)')

#from pixels 1000 to 9000, in intervals of 300, scroll down the website
for page_location in range(1000, 9000, 300):
    scroll_page_str = "window.scrollTo(0, " + str(page_location) + ")"
    driver.execute_script(scroll_page_str)
    time.sleep(1)
    
#examples of explicit wait commands:
    #this first one actually waits 10 seconds before throwing a TimeoutException error
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement")))
    #the second one is able to get the element right away, because the element is loaded already
staff_covid_cases_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > article > div > section:nth-child(12) > div > div > figure > div > div > div > img')))

output_url = staff_covid_cases_element.get_attribute('src')
print(output_url)

# TRY AND EXCEPT and error handling:
# this is usefu if you don't want your entire script to break if something goes wrong

try:
    no_element_here = driver.find_element_by_css_selector('wrong css selector')
    
except:
    print('The attempted code did not work, so run the following code: \n')
    correct_element_here = driver.find_element_by_css_selector('#edff')
    print(correct_element_here.text)
                                                               
                                                              