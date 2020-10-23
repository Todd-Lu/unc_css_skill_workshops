# UNC-CH Computational Social Science Workshop
# First thing we do is import the modules we're going to need from selenium. This list expand or contract based
# on the particular code you are working with, for now it will be relatively short

# The selenium developers have very good documentation. For many questions you have on how to interact with specific
# types of web elements or website structures like iframes, the documentation provides good and clear examples.
# https://www.selenium.dev/documentation/en/webdriver/browser_manipulation/

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# This chunk of code is important for one thing - Selenium cannot access your computer, it only interacts with the
# webbrowser. The dialogue box that shows up when you click "download" and asks if you want to open it, save it, or
# save to a location, is part of your computer and not the webbrowser. This lets you automatically download files to
# a specific location on your computer. It defines a function with no arguments that sets the options for selenium.
# the second preference setting disables browswer level notifications. Reddit started showing a notification for some
# reason and it was getting in the way.


def chromeprofile():
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': 'C:\\Users\\Will\\Documents\\ArticleLinks',
             "profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    return driver


# What we're gonna do right now is navigate through a couple webpages using selenium.
# Now start a selenium instance of chrome, using the function we just defined.
driver = chromeprofile()

# First thing we're going to do is go to google. You can go to any url with driver.get('url')
driver.get('https://www.google.com')

# Now we're gonna do a google search. We'll do this in a couple steps. The first step is to find the search bar.
# Remember that everything on the page is an element that's accessible through finding the right code that locates it.
# To do the google search bar, you just have to find the right css selector or xpath. Inspect the search bar on google's
# home page, but notice that if you highlight the code that immediately pops up something doesn't seem right. The entire
# page here is highlighted. Often you can just try again and the right code will show up. This shows that the search
# bar has an "input" tag, with a large number of options set to it, note just that these exist for later. To actually
# locate this, you can right click this chunk of code in the developer console and copy the selector. We can then
# use this to interact with the search bar. There are a couple ways to do this, I'll show you both. They're useful for
# different things. First we'll do it by defining a variable.

googlebar = driver.find_element_by_css_selector("#tsf > div:nth-child(2) > div.A8SBwf > div.RNNXgb > "
                                                "div > div.a4bIc > input")

# To find elements on a webpage using selenium, note the syntax i use.
# driver is what we defined the chromeprofile as, it's the standard name to use.
# In the same way that we do driver.get to tell selenium to go to a particular webpage, we do
# driver.find_element_by_css_selector("css selector here") to find elements. There are a lot of ways to find elements,
# and the reasoning for which one you use varies by your goals and the particular structure of the webpage. Sometimes
# it can be easier to just use different options that css selectors, but for now this is fine. So we define this
# particular element as "googlebar", and can now use the variable googlebar to interact with the element.
# When you write code, make sure the names of your variables are unique and easily identifiable, you will thank
# yourself later.

# So there are a lot of options for interacting with this. If you want to type in the bar, use send_keys. Send_keys can
# be used to not only type, but can send the enter keys, tab keys, arrow keys, etc. For now we'll just type. We can
# search for anything, but just as a default lets search for something innocuous. Lets search for office chair reviews.

googlebar.send_keys("Best office chair review 2020")

# If you send that code once, it will send that exact text to the search bar. If you send it again, it will do it again.
# So now we have the search query typed into the search bar. There are a couple options for actually searching. First,
# we can simply send the enter key to the search bar. We import Keys at the start to do this. If we don't import this,
# the code is a lot messier.

googlebar.send_keys(Keys.ENTER)

# So thats one way to do this. But let's go back to the previous page and try another way. You can manually click the
# back button, but you can also do this through selenium code. Let's do that instead.

driver.back()

# This time instead of sending enter, we'll actually click Google Search. This will also illustrate not just two methods
# of interacting with webpages, but also how to think about what webpages are and how to think about interacting
# with them in selenium. First lets find the css selector of the Google Search button. You may have to inspect twice
# again to find the correct selector.

googlesearchbutton1 = driver.find_element_by_css_selector('#tsf > div:nth-child(2) > div.A8SBwf > div.FPdoLc.tfB0Bf > '
                                                          'center > input.gNO89b')

# If you use the .click() command, it clicks on the button, but since there's nothing typed into the search bar
# nothing actually happens, but it works. This'll be important in a second.

googlesearchbutton1.click()

# Let's retype the search terms. To do this, we have to find the element again, and define googlebar again. Whenever
# you go to a new page, or if you refresh a page, you need to re-find any elements. If you don't, selenium will throw an
# error.

googlebar = driver.find_element_by_css_selector("#tsf > div:nth-child(2) > div.A8SBwf > div.RNNXgb > "
                                                "div > div.a4bIc > input")
googlebar.send_keys("Best office chair review 2020")

# Now let's try to click on the button.
googlesearchbutton1.click()

# You'll notice that you get a big angry error here, that tells you the click was intercepted. If you look
# at the google page, you might be able to guess why. When you typed the text into the search box, the webpage
# changed. A window dropped down from the search box. This is actually preventing you from accessing that first search
# button. This window is covering up the button that you saw before.
# This makes more sense when you inspect the button that you see currently on the page. The css selector of the Google
# Search button in this dropdown window is actually slightly different, its a different button.


googlesearchbutton2 = driver.find_element_by_css_selector('#tsf > div:nth-child(2) > div.A8SBwf.emcav > div.UUbT9 > '
                                                          'div.aajZCb > div.tfB0Bf > center > input.gNO89b')

# You should now be able to click this new button, and actually do your search.
googlesearchbutton2.click()

# A few big takeaways from this that I want to stress. First is that when you use selenium, you basically navigate
# on the internet in the same way you normally do. You type words, you hit the back button on your browser, and you
# click buttons. Second, is that what I just showed you is what you will essentially be doing for most of the selenium
# code you write. It falls into this exact pattern of find element, execute command on element. It can get more complex,
# particularly on webpages with more complex setups than the google homepage, but we'll talk a little bit more about
# that in a second, and most websites are surprisingly simple. Third, there are some things, like that search
# button issue, that seem unintuitive but actually make a fair bit if sense when you start to get used to it.


# Now we'll actually collect some data by webscraping. Let's go to reddit and scrape the currently trending topics, and
# in particular lets just get the top trending topics. This is more complex than the previous scraping, because the
# trending topics change over time. They're generated by the traffic within reddit. So first step is go to the reddit
# homepage.

driver.get('https://www.reddit.com/')

# Next step is we have to figure out how to select the things we're interested in. The page is a mess that's a little
# difficult to deal with. But if we look at what we can highlight with the insepct tool, notice that there seems to be a
# specific area for the trending topics. We can actually save everything in this particular chunk of code, this area
# of the website, as a variable, by just finding it using css selector.

trendingtoday = driver.find_element_by_css_selector('#TrendingPostsContainer > div')

# Now we can parse out the contents of this section of the home page, the trending posts. If you look at the structure
# of the html, each of these posts is in a div tag, with an attribute called a title, and the title has exactly what
# we're looking for. We can just scrape the titles of these elements and that'll show us what people are talking about
# on reddit. Now the way we are going to do this is using a couple slightly new methods. Instead of finding a single
# element, we're going to find all of the elements that match what we're looking for. The variable we assign this to is
# then generated as a list structure within python, which importantly you can iterate over. So the second new part we're
# going to be using is finding elements by their xpath rather than css_selector. We're going to find every element that
# is in a div tag, with a title, within the trendingtoday chunk of code. We're also going to check how many of these
# elements there are. You can see that these things are div elements and have titles when you inspect the web element.
# div means division, it defines a new section in the html document and is a container for code.

trendingtitles = trendingtoday.find_elements_by_xpath('//div[@title]')
len(trendingtitles)

# Strangely, you will see there there are actually 8 things that fit this, even though we only see 4 on the main page.
# Let's write a quick loop and print everything out.

test = trendingtoday.find_elements_by_partial_link_text()

for i in range(0, len(trendingtitles)):
    print(i)
    print(trendingtitles[i].get_attribute("title"))


# (Importantly, this actually changed between when I wrote the code and the day of the workshop. Had to change some
# code to make it work correctly. This happens, webpages change, and code wont always last.)

# Looks like the reddit main page has some sort of setup that displays only a certain number of trending topics and not
# all of their trending topics. Not entirely sure why that is or what the purpose is, it might have to do with certain
# regions, maybe there's something with the reddit app, i'm not entirely sure. But what's important is that we can see
# that there are actually 6 trending topics. Numbers 8 is an emote. We can deal with this pretty easily by writing
# some text parsing code that deletes anything with an emote structure, where it's contained within ::, but that's
# a little beyond the scope of the purpose of this particular demonstration. If we wanted to gather these data for a
# project, we would use this code inside of a loop, set it on a timer, and have it save to a dataframe on every pass
# with various important metadata like time of day, location scraped from, etc. You could also follow the links,
# scrape comments and entire threads, usernames of commenters, etc. Importantly all of this can be automated. You can
# set a loop to check these trending topics every day, every hour, every 15 minutes, and scrape this information. If you
# actually put this type of code into production, you'll want to check it at the very least every day to make sure
# it doesn't throw weird errors and so that you make sure it continues collecting the data you want.


# Now we'll go through an example that's again a bit different. We're going to access some archives through the
# UNC library. You'll have to authenticate your credentials, click a bunch of buttons, input search terms, set options,
# and a bunch of other stuff. But if you look at the basic steps, it's pretty simple and follows the pattern of find
# web element, execute command on web element.

# So this is going to go through some slightly edited code that I wrote to scrape from ProQuest's ABI/INFORM
# collection. The goal here is to access the archive through python and selenium, and to connect certain types of
# data.

# First, we go to the library website and input credentials.


# This is easy, it's just going to a particular website like we did before.
# But first we're going to define this variable original_window. This will be used later to deal with having multiple
# tabs open.
original_window = driver.current_window_handle
driver.get('https://auth.lib.unc.edu/ezproxy_auth.php?url=http://www.nclive.org/cgi-bin/nclsm?rsrc=29')


# Finding the element by xpath, and then clicking on it, to log in and authenticate.
driver.find_element_by_xpath('//input[@value="Onyen Sign In"]').click()

# Defining a variable for the username box, to then eventually pass characters to. Rather than finding an element by
# CSS_Selector or xpath, here we're doing it by id. If you look at the html of the webpage, you can see the id in the
# coding of the page. It is an input element, with id='username" which means we can find it using that id. The reason
# this works here, is that this is the only element on the page with this id. This can run into issues if there
# are multiple elements with the same id, which can actually happen pretty often. The plus side of identifying by id
# is it makes the code much more readable.


onyen_username = driver.find_element_by_id('username')

# Sending keys to the username.
onyen_username.send_keys("type your username here keep the quotes")

# Defining a variable for the password box, to then eventually pass characters to.
onyen_password = driver.find_element_by_id('password')


# Send keys to web element.
# Sending password using a defined function so you don't have to save your password in plain text. There are more
# secure, best practice ways to do this that involve saving the password on your computer and accessing it
# using python, but setting that up is a little beyond the scope of this. What you should do here is define the
# function in the script, then type out the function and your password in the console.

def send_password(password):
    onyen_password.send_keys(password)

# In the console you then just type out send_password("your password here"), make sure you keep quotes around the
# password you type.


# Sending enter to the password box. This logs us into the archive, and specifically to the Wall Street Journal.
onyen_password.send_keys(Keys.ENTER)

# The next step here is to navigate within this page to where we want to go, so we can do a narrower search. We're
# going to click on the advanced search web element. This brings us to the search page we want.
driver.find_element_by_css_selector("#searchWithinPubForm > div.publicationBrowseSearch > div "
                                    "> div.col-md-3.col-lg-3 > a").click()


# So what you'll see on this window is that we are at the advanced search page in proquest. The newspaper that we want
# to search within is selected by pubid(10482) in the search bar, now have to input our search terms actually search.

# Rather than finding by css selector, we're finding the element by id again. We're selecting the second bar for the
# search to input terms.
secondsearchfield = driver.find_element_by_id("queryTermField_0")

# Going to search for something inoccuous, and also something that has fairly limited results just for the sake of
# demonstration. Sending our search term keys to the second part.
secondsearchfield.send_keys('(Office near/5 Chair) OR ("Best Office Chair") OR (Greatest near/5 Chair)')

# Sending an enter keystroke through a different method for the sake of demonstration.
secondsearchfield.send_keys(u'\ue007')


# So here we're going to again use another method of interacting with web elements. We're defining the variable
# "sortbar" which is for the mechanism or button that you use to sort the results to your search. By default it
# sorts by relevance, but we want to organize our results by date. Importantly, note the html of the web element
# here. Previously we interacted with div elements, but here we're interacting with a select element. Selenium
# has a built in method for doing this, which is to put the driver.find_element_by code in Select(). This lets you
# easily and simply interact with the dropdown menu and change how the page is ordered. So first we define the
# variable sortbar, using Select().

sortbar = Select(driver.find_element_by_xpath('//*[@id="sortType"]'))

# Then we use the sortbar variable and the Select method's built in tools. If you again look at the html you can
# see the options in the drop down menue. You can see the line that says
# <option value="relevance">Relevance</option>. That bit there between the >< is "visible text," it's what is
# displaying to the user on the webpage. You can choose your particular drop down choice by selecting on visible text
# within this sortbar element that we just defined, using the select tools. We're gonna pick to order it with the
# oldest articles first. You don't have to use click() or anything else because you're using the select methods.

sortbar.select_by_visible_text("Oldest first")


# Next, notice how there are only 20 articles displaying on the page. That's not very many, it's pretty inefficient
# to do this 20 at a time. Let's see if we can display more than that. At the bottom of the page, note the little
# dropdown menu for "items per page." Let's find this and change it to 100. This time we'll figure out if we can use
# id. We did this once before with the reddit example, but instead of finding a single element we're finding all
# elements that match this. You can use this to see if using id works by just looking at the length of the list.

perpage_list = driver.find_elements_by_id("itemsPerPage")

len(perpage_list)

# Its length is 1, so we can be pretty sure it works. It's not foolproof, but it's a pretty quick way to be pretty sure.

items_per_page = Select(driver.find_element_by_id("itemsPerPage"))

# Selecting based on visible text again, with the string 100 this time, since it's the visible text in the html.

items_per_page.select_by_visible_text("100")

# Now that we've set up the page, we're going to find the button that selects every article and then click it.

select_all = driver.find_element_by_id("mlcbAll")

# Now we'll click it, which selects every article on the page.
select_all.click()

# Next we have to actually save all of the articles we've selected. The way you do that as a normal computer user is
# by clicking the three dots in the right corner of the window, then a popup window comes up, and you select the
# various options for how and in what format you want to download your results. So we're going to do the exact same
# thing using selenium.

# We can find the button by just using css selector, because there's nothing more readable than that we can use.
all_save_options = driver.find_element_by_css_selector("#allSaveOptionsLink > span.tool-option.dot-dot-dot > span")
all_save_options.click()

# Notice that this brings up a popup window. Popup windows, as you saw with the google example, can do weird things.
# For some reason, the methods we have used up until now might seem like they work, but are actually unreliable. When
# you do this process of writing the code for selenium, you want to make sure it works in an automated fashion. As you
# interact with the page, you're changing what is called focus. Think back to the google example again. As you open
# the search bar, the focus is taken off of the normal search button and is placed onto the top search button. As you
# interact with different parts of the webpage here, certain elements are similarly only accessible when the focus is
# on particular areas of the webpage. If you are clicking around this popup window and focus on it, you can interact
# with the web elements we need by css selector and xpath just fine. If you restart the browser and do it in an
# automated fashion, it breaks because of where the focus on the page is.

# What does work though, is trying to find the element by partial link text. This is similar to selecting by visible
# text. If you look at the html of the web element, you'll see again the visible text between the carats,
# in class="buttonText">XLS</span>. You can see that this text is here by also looking at the button, it says XLS in
# there and you can guess that's something you might be able to interact with. Turns out that XLS is something we can
# in fact find the element using, and luckily it works.
xls_click = driver.find_element_by_partial_link_text("XLS")
xls_click.click()

# We want to deselect all items we have selected so far when we're done with this pass through the data collection,
# so we find the button using normal inspect/css selector means and it works.
deselect_when_done = driver.find_element_by_css_selector("#saveAsFileResultsCount > div.col-md-8 > label")
deselect_when_done.click()

# Next we want to continue and save the files. We run into the same problem as before with clicking the xls button, and
# again finding the element by partial link text works. This time, you can see it again on the page where the button
# has "Continue" inside of it, and you can see it in the html with id="submitButton_56e19a60425e">Continue</a>. This is
# where the chunk of code at the start that defined options for the chrome profile come in handy. Normally a dialogue
# window would pop up and ask you what you want to do with the file you are downloading. Selenium can't interact with
# that dialogue window, it's operating on your computer rather than on the browser. The options we set let this
# file automatically download.
continue_save_button = driver.find_element_by_partial_link_text('Continue')
continue_save_button.click()

# When you hit the continue button, it opens another tab. Tabs are dealt with through what are called window handles.
# Each tab is its own "handle." Remember that at the start of the proquest process we defined a variable named
# "original_window". That identifies what the original window is that we want to keep open. What we want to do here is
# we want to close this second tab. If you leave hundreds of tabs open, your browser and computer get pretty unhappy,
# so we want to close these when they're no logner useful. The way we're going to close the tab we don't want is to get
# a list of all open handles. Python indexes lists at 0, so the first tab is 0 in the list and the second tab is 1.

window_handles = driver.window_handles

# Importantly, focus is still on the first tab. Even though you see the second tab, the first one is still active. If
# you close the current tab, that first tab will close. So before we close anything we need to switch to the second
# tab.
driver.switch_to.window(window_handles[1])

# Now that the focus is on this second tab, we can simply close it then swap focus back to the first tab which we
# defined at the start.
driver.close()
driver.switch_to.window(original_window)

# Finally, there are more results to grab here, so we want to go to the next page. We're going to use one last new way
# of finding web elements. With find_element_by_xpath, you can select web elements by their specific html parts. If you
# look at the next page button, the > at the bottom, you can see that it has an "a" tag, which defines a hyperlink, and
# has the title "Next Page". We can use these with find_element_by_xpath to find this web element.
next_page = driver.find_element_by_xpath('//a[@title="Next Page"]')

# Now that we found it, we can click it to go to the next page, and continue data collection.
next_page.click()

driver.close()
