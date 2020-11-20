# UNC-CH Computational Social Science Workshop

import re #for regular expressions
import numpy as np #math functions in python
import pandas as pd #data manipulation software
from selenium import webdriver
from datetime import date


# What we're going to do here is effectively bring together a lot of what we've done so far, and we'll scrape some
# information and save it in a Python spreadsheet. Python's spreadsheet and data analysis library is
# called Pandas, which we import as pd.

# But first we need to go figure out what we want to gather and navigate there with selenium. Let's say we're
# interested in political content, so let's go check reddit again.

def chromeprofile():
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': 'INSERT WORKING DIRECTORY HERE',
             "profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    return driver


# First we need to start up chrome.
driver = chromeprofile()


# Now let's go to a political subreddit. KotakuInAction is an odd political subreddit. It's focused on a particular
# social movement, called GamerGate. GamerGate is/was focused on political issues in video games. The real specifics
# of it are a little beyond the scope of this, but it's a potential origin for some alt-right activity and mobilization,
# and got started in the mid/early 2010s. Let's see what this community is up to these days. First we'll navigate to
# the subreddit in chrome.


driver.get('https://www.reddit.com/r/KotakuInAction/')

# Now let's find the top threads on the page. This will get us a list of every element on the page with the a
# data-click-id="body" in the element. Turns out that gives us every thread on the page. Let's pick the top 10 to
# scrape, but first let's check to make sure we're getting what we want.

kiapage = driver.find_elements_by_xpath('//*[@data-click-id="body"]')


# This xpath seems to get the things we want, but let's print out the links just to check. There are some adds on the
# page that might mess things up.
for kiapage in kiapage:
    print(kiapage.get_attribute('href'))

# Turns out the ads do mess things up, so let's remove them. You'll see that some of the values are None, those are
# where the advertisements are. We need to remove those first so we can actually automate this.

# We need to redefine the kiapage variable, the loop messes with the original variable's list structure.

kiapage = driver.find_elements_by_xpath('//*[@data-click-id="body"]')

# Define a list to append the working links to.
workinglinks = []

# Loop through the front page and pull out working links. The if statement is first making sure that the content of
# kiapage.get_attribute('href') isn't None. If it is none, and the statement evaluates to False, it just skips that
# part of the loop.

for kiapage in kiapage:
    if kiapage.get_attribute('href') != None:
        workinglinks.append(kiapage.get_attribute('href'))
    else:
        continue

# Now we have a list of links to the top ten threads on this particular reddit for the day. Let's go to the first one
# by accessing it in the list.

driver.get(workinglinks[0])

# This looks like some sort of announcement or something that gets updated every once in a while. Only some of the
# comments are loaded so far, so let's open the entire discussion. There's a button on the page to do that. Let's see
# if a real simple xpath will find this.

testbutton = driver.find_elements_by_xpath('//button[@role="button"]')

#Let's check how many buttons there are that match.
len(testbutton)

# There's a few, so we need to figure out another one. Let's find how many buttons there are that have text that
# includes the text "View" in them.
testbutton = driver.find_elements_by_xpath('//button[contains(text(), "View")]')


# Just one, and hopefully this is generalizable to the other links because it's just looking one View rather than
# text that's extremely specific to this one button. Let's define a single web element variable rather than a list,
# and click on it.

alldiscussion = driver.find_element_by_xpath('//button[contains(text(), "View")]')
alldiscussion.click()

# Now let's find the web element that seems to hold the first thread on the page that we want.

thread1 = driver.find_element_by_css_selector('#SHORTCUT_FOCUSABLE_DIV > div:nth-child(4) > div > div._1npCwF50X2J7Wt82SZi6J0._3OGqXkiUb_0ZMlksb26boO > div.u35lf2ynn4jHsVUwPmNU.Dx3UxiK86VcfkFQVHNXNi._3KaECfUAGLfWQPO5eNjMNl > div.uI_hDmU5GSiudtABRz_37 > div._2M2wOqmeoPVvcSsJ6Po9-V')
# It's kind of a mess of a css selector. But, we defined it. Let's quickly see if these two things are generalizable to
# the rest of reddit. We can do this by checking on the other entries in our list.

driver.get(workinglinks[1])

# Now let's see if the button will work.
alldiscussion = driver.find_element_by_xpath('//button[contains(text(), "View")]')
alldiscussion.click()

# Looks like it works! Let's check if the thread identifier works.
thread1 = driver.find_element_by_css_selector('#SHORTCUT_FOCUSABLE_DIV > div:nth-child(4) > div > div._1npCwF50X2J7Wt82SZi6J0._3OGqXkiUb_0ZMlksb26boO > div.u35lf2ynn4jHsVUwPmNU.Dx3UxiK86VcfkFQVHNXNi._3KaECfUAGLfWQPO5eNjMNl > div.uI_hDmU5GSiudtABRz_37 > div._2M2wOqmeoPVvcSsJ6Po9-V')

# Weirdly and unexpectedly, it actually does work. So let's go back to the first thread and see if we can start
# actually scraping information we want. Ultimately we want to get this working into a loop so we can automate this, so
# we'll also be keeping that in mind.

driver.get(workinglinks[0])

#Reopen all comments
alldiscussion = driver.find_element_by_xpath('//button[contains(text(), "View")]')
alldiscussion.click()

# First thing we have to do now is get teh original post. It's in a slightly different spot than the comments.
#Took a little work, but this seems to identify the original post.
original_post = driver.find_element_by_xpath('//div[@data-test-id="post-content"]')

# Lets start looking for the information we want. First we want to find the username that is contained within this
# block of html. If we look at the html, we can see that at the start of posts where the user is listed, it links to
# their profile. We can use that to identify the poster. So within this original post's html, we find the link that
# has /user/ in it. There's only one of those, and that's the original poster. We can remove that u/ later.

original_post_username = original_post.find_element_by_xpath('.//a[contains(@href, "/user/")]')
original_poster = str(original_post_username.text)
original_poster

# Next we need the original post's title. Looks like this is saved as an h1 element, a type of heading. This one is
# fairly simple.
original_post_title_element = original_post.find_element_by_xpath('.//h1')
original_post_title = str(original_post_title_element.text)

# Now let's find the post date. This one also looks like it'll be easy.
original_post_date_element = original_post.find_element_by_xpath('.//a[@data-click-id="timestamp"]')
original_post_date_string = original_post_date_element.text

# Currently we have the date as a string, but we want to parse this out. We'll do that using regular expressions.
# The exact details of regular expressions are a bit beyond the scope of today's workshop, but we'll get into it a bit
# next semester (I think). The basic idea of regular expressions is that you can parse text by matching particular
# patterns. So what we're going to do here is match some patterns to get much more usable data.

# Creating the pattern here
original_post_time_regex = re.compile(r'(\d*)(\s*)(year|years|month|months|week|weeks|day|days|hour|hours|second|seconds)(\s*)(ago)')
# Telling python to match the pattern to the text we have
original_post_time_match = re.match(original_post_time_regex, original_post_date_string)

# Pulling out the numeric part of the time
original_post_time_numeric = int(original_post_time_match.group(1))

# Pulling out the units
original_post_time_units = original_post_time_match.group(3)

# Finally let's get the text of the original post. The text of the original post is contained within p elements. P
# elements are paragraph elements, they usually contain text.
original_post_text_element = original_post.find_elements_by_xpath('.//p')

# Lets print this out so we can see what it looks like

for original_post_text_element in original_post_text_element:
    print(original_post_text_element.text)

# This is what we want! Perfect. Let's define the list again, then turn it into a list of its text.
original_post_text_element = original_post.find_elements_by_xpath('.//p')
original_post_text_list = []
for original_post_text_element in original_post_text_element:
    original_post_text_list.append(str(original_post_text_element.text))

# Now let's paste them together to generate the string to save.
original_post_text_string = ""
for i in original_post_text_list:
    original_post_text_string += i+" "

#Now lets print this and see what we have
print(original_post_text_string)


#Now let's move on to the comments section. Let's define that chunk of text first.

thread1 = driver.find_element_by_css_selector('#SHORTCUT_FOCUSABLE_DIV > div:nth-child(4) > div > div._1npCwF50X2J7Wt82SZi6J0._3OGqXkiUb_0ZMlksb26boO > div.u35lf2ynn4jHsVUwPmNU.Dx3UxiK86VcfkFQVHNXNi._3KaECfUAGLfWQPO5eNjMNl > div.uI_hDmU5GSiudtABRz_37 > div._2M2wOqmeoPVvcSsJ6Po9-V')

# We're back on the first one page, and have defined that first thread with comments.
# So let's look for some parts of html that might identify individual comments. After some searching, tabindex="-1"
# might do the trick.

post_test = thread1.find_elements_by_xpath('.//div[@tabindex="-1"]')
len(post_test)

# This seems like it works at index 0, but once you get past it, things start to get a little weird. A few other things
# also didn't  work, so we're going to do something a little weirder, which is finding an element then moving through
# the html tree.

post_test = thread1.find_elements_by_xpath('.//span[contains(text(), "point")]')
post_test_0_1 = post_test[0].find_element_by_xpath('..')
post_test_0_2 = (post_test_0_1.find_element_by_xpath('..'))
post_test_0_3 = str(post_test_0_2.text)



post_regex = re.compile(r'(.*)(\n)(.*)(\n)(.*)(\n)(.*)(\n)(\d*)(\s*)(year|years|month|months|week|weeks|day|days|hour|hours|minute|minutes|second|seconds)(\s*)(ago)(\n)(.*)')
post_match = re.match(post_regex, post_test_0_3)
post_match.groups()

# The way the regex is constructed is again with groups, and we're pulling text matches from the groups.

comment_user_name = post_match.group(3)
comment_time_numeric = post_match.group(9)
comment_time_unit = post_match.group(11)
comment_text = post_match.group(15)

# Just to wrap this up, we have the following variables, including the original poster section and a variable
# that is generating today's date, so we can calculate the day that the post is from.


original_poster #String
original_post_title #String
original_post_time_numeric #Integer
original_post_time_units #String
original_post_text_string #String
current_date = date.today() #datetime
original_post_positive = 1
reply_negative = 0

comment_user_name #String
comment_time_numeric #integer
comment_time_unit #String
current_date = date.today()
comment_text # String
original_post_negative = 0
reply_positive = 1


# All this works great so far! Let's now set up our data frame. We're gonna put together a data frame to hold all our info,
# including the relations of things. Even though we wont be able to completely preserve the structure of the original
# data, we can still keep track of what's an original post, what's a reply, and what the replies are to.

reddit_kia = pd.DataFrame({'username': pd.Series(dtype='str'),
                    'original_post_title': pd.Series(dtype='str'),
                    'post_time_numeric': pd.Series(dtype='int64'),
                     'post_time_units': pd.Series(dtype='str'),
                           'current_date': pd.to_datetime(0),
                    'post_text': pd.Series(dtype='str'),
                    'original_post': pd.Series(dtype='int64'),
                    'reply': pd.Series(dtype='int64')})


# Now let's input our information into the pandas dataframe. We can do this by column index. Let's start with the
# original post.

reddit_kia.loc[len(reddit_kia.index)] = [original_poster, original_post_title, original_post_time_numeric,
                                         original_post_time_units, original_post_text_string, current_date,
                                         original_post_positive, reply_negative]


#Now let's add the first reply
reddit_kia.loc[len(reddit_kia.index)] = (comment_user_name, original_post_title, comment_time_numeric,
                                         comment_time_unit, current_date, comment_text, original_post_negative,
                                         reply_positive)



# Great, so now it seems to be working with what we have here. This gets more complex with the text processing once
# it hits the second comment since there's some extra text in some of the usernames that needs to be dealt with, but
# that's part of the process. Regular expressions specifically and scraping like this generally are fundamentally
# iterative processes where exceptions happen and you need to work with them.
