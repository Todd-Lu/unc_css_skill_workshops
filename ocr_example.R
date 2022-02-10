# the following script enables us to upload and edit images 
# then, we will apply optical character recognition on images
# then, we will learn ways to troubleshoot optical character recognition
# most of this involves cleaning the image and tinkering with the actual OCR settings

library(tidyverse) # data science 
library(stringr) # text manipulation
# note: maybe need to install RTools: https://cran.rstudio.com/bin/windows/Rtools/rtools40.html

library(tesseract) # the ocr package
library(magick) # the image editing package


# set current working directory:

  #set working directory to where data are located on local hard drive
set_wd_locally = ''
setwd(set_wd_locally)

## Let's take a look at the images we are going to work with. 
## These are images taken from state department of corrections websites that report covid cases

# set text editing function we will use in the future
split_all_words_then_nums = function(s, target_length = 6){
  #this script first takes each row of text, then splits it by white space
  s_split = s %>% str_split(" ", simplify = T)
  
  #then it identities which text are characters and which as numbers
  s_split_word_positions = suppressWarnings(s_split %>% as.numeric) %>% is.na
  
  #then using the word positions can select which in vector are numbers 
  s_split_nums = s_split[!s_split_word_positions]
  
  #can then identify and paste together the text
  s_split_words = s_split[s_split_word_positions] %>% paste0(collapse = " ")
  
  #concatenate the words and numbers
  v_to_return = c(s_split_words, s_split_nums)
  
  # if the length is greater than target length, set as 0
  if(length(v_to_return) > target_length) {v_to_return = v_to_return[target_length]}
  
  #if length is less than target length (missing values), set equal to concatenate of v_to_return and repeated NA depending on target length
  if(length(v_to_return) < target_length) {v_to_return = c(v_to_return, rep(NA, target_length - length(v_to_return)))}
  
  v_to_return = set_names(v_to_return, paste0("V", 1:target_length)) %>% as_tibble_row
  return(v_to_return)
}

split_words_large_space = function(s, target_length = 6)
{
  s_split = s %>% str_split(" ", simplify = T)
  s_split_positions = suppressWarnings(s_split %>% str_detect(""))
  s_split_words = s_split[s_split_positions] %>%
    str_trim()
  
  v_to_return = c(s_split_words)
  
  # if the length is greater than target length, set as 0
  if(length(v_to_return) > target_length) {v_to_return = v_to_return[target_length]}
  
  #if length is less than target length (missing values), set equal to concatenate of v_to_return and repeated NA depending on target length
  if(length(v_to_return) < target_length) {v_to_return = c(v_to_return, rep(NA, target_length - length(v_to_return)))}
  
  v_to_return = set_names(v_to_return, paste0('V', 1:target_length)) %>% as_tibble_row
  return(v_to_return)
}

## Working with Image Magick: 
## It is a cross-platform open source tool we can use to create and edit images
## https://docs.ropensci.org/magick/articles/intro.html

## Working with Tesseract OCR engine (supports multiple languages): 
## https://docs.ropensci.org/tesseract/articles/intro.html

# magick allows us to read images like data files
ky_image = image_read('images/KY_2020-10-12.jpg')
ky_image #notice that this also outputs characteristics of image at bottom console

# what happens if we just apply OCR to this right away?
string_output = ocr(ky_image, engine = tesseract('eng'))
string_output

lines_output = string_output %>%
  str_split('\n') %>%
  unlist()
lines_output ## not great

# we can manipulate this image using image magick -- most important is to set things to grayscale
ky_image = ky_image %>%
  image_convert(type = 'grayscale')
ky_image

# alternatively, we can also force colors into black or white using image_threshold() and set a threshold value
ky_image %>%
  image_threshold(threshold = '60%')

# we can also remove vertical lines by identifying lines, then negating them (turn into white)
image_hlines = ky_image %>%
  image_morphology('Close', 'Rectangle:80, 1, 0') %>%
  image_negate()

image_hlines

ky_image = image_composite(ky_image,
                            image_hlines,
                            operator = 'Add')
ky_image

# now we can crop out the top (remember, we can see dimensions when we output images)
ky_image = image_crop(ky_image, "1340x838+0+50")
ky_image

# now finally let's apply OCR
string_output = ocr(ky_image, engine = tesseract('eng'))
string_output

lines_output = string_output %>%
  str_split('\n') %>%
  unlist()
lines_output #seems weird?

# let's extract the prison names in first column using regular expressions
prisons = str_extract_all(lines_output, 
                '[A-Za-z ]+',
                simplify = T)
prisons = prisons[,1] 
prisons = prisons %>%
  str_trim()

prisons

# let's try setting tesseract engine to restrict characters -- only numbers?
numbers_only = tesseract('eng',
                         options = list(tessedit_char_whitelist = "0123456789"))

string_output = ocr(ky_image,
                    engine = numbers_only)
string_output
lines_output = string_output %>%
  str_split('\n') %>%
  unlist()

lines_output # numbers look accurate!

#set column names and then put them all into a data table
col_names = c("institution",
              "staff_positives", 
              "staff_deaths", 
              "inmates_positives", 
              "inmate_deaths")


ocr_data_tbl = lines_output %>% 
  map_dfr(split_all_words_then_nums, 5) %>% # we're calling function we set above
  set_names(col_names) 

ocr_data_tbl

ocr_data_tbl$institution = prisons
ocr_data_tbl = ocr_data_tbl %>%
  filter(institution != '')

ocr_data_tbl # looks good overall, but some missing data




# another example of image.. Indiana web scrape - example of what you can do with colors

in_image = image_read('images/IN_2020-11-30.jpg')
in_image

# it is terrible if you applied OCR right away:
string_output = ocr(in_image, engine = tesseract('eng'))
string_output

lines_output = string_output %>%
  str_split('\n') %>%
  unlist()
lines_output # no idea what is going on


# apply different functions to edit image
in_image = in_image %>%
  image_crop('1791x794+0+150') %>%
  image_negate() %>%
  image_convert(type = 'grayscale') %>%
  image_threshold(threshold = '45%') %>%
  image_negate() 

in_image

# let's remove the black lines
image_vlines = in_image %>%
  image_morphology('Close', 'Rectangle:1, 80, 0') %>%
  image_negate()
image_vlines

image_hlines = in_image %>%
  image_morphology('Close', 'Rectangle:80, 1, 0') %>%
  image_negate()
image_hlines

# remove black lines using image_composite
in_image = image_composite(in_image,
                            image_hlines,
                            operator = 'Add')
in_image

in_image = image_composite(in_image,
                            image_vlines,
                            operator = 'Add')
in_image

# now let's apply ocr
string_output = ocr(in_image, engine = tesseract('eng'))
string_output

lines_output = string_output %>%
  str_split('\n') %>%
  unlist()
lines_output # not looking great

# splitting into numbers and locations
image_numbers = in_image %>%
  image_crop('1791x794+350')

image_locations = in_image %>%
  image_crop('350x794')

# detect numbers
numbers = tesseract(options = list(tessedit_char_whitelist = "0123456789"))
string_output = ocr(image_numbers, 
                    engine = numbers)

numbers_output = string_output %>%
  str_split('\n') %>%
  unlist()

numbers_output # not bad

# detect facilities
string_output = ocr(image_locations, 
                    engine = tesseract('eng'))
facilities_output = string_output %>%
  str_split('\n') %>%
  unlist()

facilities_output = facilities_output[facilities_output != '']
facilities_output # not bad

# now let's put these in a data table
col_names = c('facility',
              'staff_tests',
              'staff_positives',
              'staff_recovered',
              'staff_deaths',
              'inmate_quarantine',
              'inmate_isolation',
              'inmate_tests',
              'inmate_positives',
              'inmate_recovered',
              'inmate_deaths_presumed',
              'inmate_deaths_confirmed')

df = numbers_output %>%
  map_dfr(split_all_words_then_nums, 12) %>%
  set_names(col_names) %>%
  filter(!is.na(staff_tests)) 

df #looks like this still has issues

df$facility = facilities_output
df

utils::View(df)