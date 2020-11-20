# UNC-CH Computational Social Science Workshop
# First thing we do is import all of the options we're going to need from selenium. This list expand or contract based
# on the particular code you are working with, for now it will be relatively short
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.support.ui import Select
import pandas as pd



# This chunk of code is important for one thing - Selenium cannot access your computer, it only interacts with the
# webbrowser. The dialogue box that shows up when you click "download" and asks if you want to open it, save it, or
# save to a location, is part of your computer and not the webbrowser. This lets you automatically download files to
# a specific location on your computer. It defines a function with no arguments that sets the options for selenium.


def chromeprofile():
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': 'C:\\Users\\Will\\Documents\\ArticleLinks'}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    return driver

driver = chromeprofile()

original_window = driver.current_window_handle

def login(username, password):
    # We do things within the framework of "try" and "except" blocks of code. This lets us do some error handling, and
    # in particular lets us know if, when, and why our code fails. Instead of just breaking, it'll give us an easily
    # identifiable error and tell us what happened, and potentially let us make our code continue rather than just dying.
    # So first we enclose the code within a try block, and then an except block at the end. If it runs into the error
    # that we think may happen, it'll print a specific message letting us know what's going on.
    try:
        # This is easy, it's just going to a particular website like we did before.
        driver.get(
            'https://auth.lib.unc.edu/ezproxy_auth.php?url=http://www.nclive.org/cgi-bin/nclsm?rsrc=29'
        )
        # This however is different. What this is doing is it's telling selenium to wait. Remember that you are doing
        # this webscraping on the internet, things have load times and those load times vary. If you don't write your
        # code allowing for load times, you run into a problem called racing. There's a race between your code running
        # and what you want it to do. If your code runs before the webpage loads, it fails, because it can't find the
        # thing you're looking for. So here we have an explicit wait, we're telling selenium to wait for 20 seconds.
        # We're telling it to wait until the element we're looking for is clickable. It checks every half second. If
        # it fails for 20 seconds, it will give us a specific error telling us why.
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@value="Onyen Sign In"]'))
        )
        # Once this is clickable, it'll go to the next step, which is to actually click the button. We don't need to
        # always define things as variables, so here we simply find the element and click on it in the same line of
        # code.
        driver.find_element_by_xpath('//input[@value="Onyen Sign In"]').click()
        # We then come to another wait, which is waiting for the username box to load, just to make sure it's working.
        # Also note that here instead of finding the element by css selector or xpath, we're finding it only by its ID.
        # ID is similar to the title we used before, you can see it if you inspect the web element. If there's only
        # one element with a particular ID on a page, in my opinion it makes for more readable and understandable code
        # to just find it by ID. It doesn't do anything different funciontally, it's just easier to understand and to
        # troubleshoot if and when you need to because it's very clear what it's trying to access, rather than being
        # some massive string.
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "username")))
        onyenUsername = driver.find_element_by_id('username')
        # This here is another wait, but it's telling python, not selenium, to wait for a random time between 0 and 1
        # seconds, to simulate a person's reaction time. This is trying to make it look like a person is running the
        # webbrowser rather than it being done by a computer.
        time.sleep(random.uniform(0, 1))
        # The username here is from the first argument of the function, it simply passes through what you typed as your
        # username.
        onyenUsername.send_keys(username)
        # Another sleep command.
        time.sleep(random.uniform(0, 1))
        # Waiting for the password box to be clickable, making sure it's there.
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "password")))
        # Finding the password box.
        onyenPassword = driver.find_element_by_id('password')
        time.sleep(random.uniform(0, 1))
        # Your password is generated by the second argument for the function, it's input then we hit the enter key.
        onyenPassword.send_keys(password + Keys.ENTER)
    except NoSuchElementException:
        print("No Such Element Found, Check ID of Username or Password")


login(username, password)


def advanced_search():
    try:
        # One important thing to note here, the code I had written previously no longer worked. This particular
        # website has changed since I last interacted with it. This is a thing that will happen if you webscrape.
        # Websites change, and you will have to adapt to them, especially if you are scraping over a long period of time.

        # Waiting for the Advanced Search link to be clickable
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '#searchWithinPubForm > div.publicationBrowseSearch > div > div.col-md-3.col-lg-3 > a')))
        driver.find_element_by_css_selector(
            "#searchWithinPubForm > div.publicationBrowseSearch > div > div.col-md-3.col-lg-3 > a").click()
    except NoSuchElementException:
        print("No Such Element Found, Advanced Search link after login")


advanced_search()
# So what you'll see on this window is that we are at the advanced search page in proquest. The newspaper that we want
# to search within is selected by pubid(10482) in the search bar, so we now have to input our search terms and set up
# our search. Now we need to input some more text so we can search for something.

def create_search():
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "queryTermField")))
    time.sleep(random.uniform(0.5, 1.3))
    #Rather than finding by css selector, we're finding the ele
    secondsearchfield = driver.find_element_by_id("queryTermField_0")
    secondsearchfield.send_keys('("alt-right") OR (altright)')
    time.sleep(random.uniform(0.4, 0.8))
    secondsearchfield.send_keys(u'\ue007') #This is another way of sending enter.

create_search()


def change_sorting():
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="sortType"]')))
    # So here we're going to again use another method of interacting with web elements. We're defining the variable
    # "sortbar" which is for the mechanism or button that you use to sort the results to your search. By default it
    # sorts by relevance, but we want to organize our results by date. Importantly, note the html of the web element
    # here. Previously we interacted with div elements, but here we're interacting with a select element. Selenium
    # has a built in method for doing this, which is to put the driver.find_element_by code in Select(). This lets you
    # easily and simply interact with the dropdown menue and change how the page is ordered. So first we define the
    # variable sortbar, using Select().
    sortbar = Select(driver.find_element_by_xpath('//*[@id="sortType"]'))
    # Then we wait.
    time.sleep(random.uniform(0.1, 0.5))
    # Then we use the sortbar variable and the Select method's built in tools. If you again look at the html you can
    # see the options in the drop down menue. You can see the line that says
    # <option value="relevance">Relevance</option>. That bit there between the >< is "visible text," it's what is
    # displaying to the user on the webpage. You can pick your particular drop down choice by selecting on visible text
    # within this sortbar element that we just defined, using the select tools. We're gonna pick to order it with the
    # oldest articles first.
    sortbar.select_by_visible_text("Oldest first")

# Just for reference, here's what the function looks like without all the comments. This is actually pretty simple to
# do, half of this function is waiting alone.

#def change_sorting():
#    WebDriverWait(driver, 20).until(
#        EC.element_to_be_clickable((By.XPATH, '//*[@id="sortType"]')))
#    sortbar = Select(driver.find_element_by_xpath('//*[@id="sortType"]'))
#    time.sleep(random.uniform(0.1, 0.5))
#    sortbar.select_by_visible_text("Oldest first")

change_sorting()

# Next, notice how there are only 20 articles displaying on the page. That's not very many, it's pretty inefficient
# to do this 20 at a time. Let's see if we can display more than that. At the bottom of the page, note the little
# dropdown menue for "items per page." Let's find this and change it to 100.


def items_per_page():
    items_per_page = Select(driver.find_element_by_id("itemsPerPage"))
    items_per_page.select_by_visible_text("100")

items_per_page()

# Select all on page

def select_all():
    select_all = driver.find_element_by_id("mlcbAll")
    select_all.click()

select_all()

# We can find the button by just using css selector, because there's nothing more readable than that we can use.
def all_save():
    all_save_options = driver.find_element_by_css_selector("#allSaveOptionsLink > span.tool-option.dot-dot-dot > span")
    all_save_options.click()

all_save()



#Save as xls
def save_xls():
    xls_click = driver.find_element_by_partial_link_text("XLS")
    xls_click.click()

save_xls()

#Deselect when done
def deselect():
    deselect_when_done = driver.find_element_by_css_selector("#saveAsFileResultsCount > div.col-md-8 > label")
    deselect_when_done.click()

deselect()

#Click the save button
def save_button():
    continue_save_button = driver.find_element_by_partial_link_text('Continue')
    continue_save_button.click()

save_button()

def window_handles_handling():
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    driver.close()
    driver.switch_to.window(original_window)

window_handles_handling()


driver = chromeprofile()
original_window = driver.current_window_handle
login(username, password)
advanced_search()
create_search()
change_sorting()
items_per_page()
select_all()
save_xls()
deselect()
save_button()
window_handles_handling()



# Now that we have the xls, let's open it and look at the data.
newspaperxls = pd.read_excel('C:\\Users\\Will\\Documents\\ArticleLinks\\ProQuestDocuments-2020-11-20.xls')

#Get the header
data_top = newspaperxls.head()

#Look at the column names
list(newspaperxls)


# What we really want here is the content of the column DocumentURL.

url = newspaperxls.iloc[2].DocumentURL

# Print this out and take a look at it, it's a usable url.
print(url)

# We can use this url to go to the specific newspaper article. It's a stable link. Importantly, it brings us straight to
# the full text. We can then gather the text on this page, and record it in pandas.
driver.get(url)

# This is all in very simple full text. If we look at the html, it's contained within p elements. So let's find the
# area of the page that has the p elements we want first.

full_text_area = driver.find_element_by_xpath('//div[@class="contentPadingDocview"]')

#Then let's find the child p elements.
page_text = full_text_area.find_elements_by_xpath('.//p')

# And print them all out to see if we have what we want.
for page_text in page_text:
    print(page_text.text)

# Seems like we do! Now let's save these data as a string.
test = ""
page_text = full_text_area.find_elements_by_xpath('.//p')

page_text_list = []
for page_text in page_text:
    page_text_list.append(str(page_text.text))

page_text_string = ""
for i in page_text_list:
    page_text_string += i+" "

# We have some new data here, so let's add a column to our data frame

newspaperxls['fulltext'] = ""

# Take a look at the column names again. You can see a new column at the very end.
list(newspaperxls)

# We can now assign our data to the dataframe in this column.
# newspaperxls is the dataframe, loc is an access method
newspaperxls.loc[2, 'fulltext'] = page_text_string
newspaperxls.fulltext[2]
