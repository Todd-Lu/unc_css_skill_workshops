library(tidyverse)
library(googlesheets4)
source("~/GitHub/state-corrections-scraper/cleaning/state_ocr_functions.R")
state_url_key = read_csv('~/GitHub/state-corrections-scraper/config/state_url_key.csv')


#HARD CODED PARAMETERS:
  #set working directory to where data are located on local hard drive (not ideal, need to find a streamlined solution to set where directory is located...)
set_wd_locally = 'C:/Users/toddj/Documents/Research Projects/COVID 19 Web Scraping'
setwd(set_wd_locally)

sheet_url = 'https://docs.google.com/spreadsheets/d/1CHWo0gIwAz7xlsFwqHEbS0Z0bN9etPlv8TzrR-TIilU/edit#gid=1923746239'

current_date = today()
date_as_string = format(current_date, '%Y-%m-%d')

#set up google sheets authentication in text file
email_auth = read_file('email_gs4.txt')
gs4_auth(email = email_auth)


#set up diagnostics file...
diag_df = state_url_key %>%
  select(state)
diag_filename = 'data/diagnostics_cleanerfile.txt'
diag_df$cleaner_date = today()

#the file goes through each state based on the state_url_key list and current date
#then it applies state_uploader function all the states
#cleans and uploads pdf/image files online onto google sheets, whichever one works

for (state in state_url_key$state)
{
  print(state)
  
  tryCatch(
    
    state_uploader(state = state,
                   sheet_url = sheet_url,
                   date = current_date),
    
    error = function(e)
    {
      print('Failed')
  
      output_file = paste('Failed:', state,'-', current_date, 'RUNTIME:', Sys.time())
      cat(output_file,
          file = diag_filename,
          sep = "\n",
          append = TRUE)

    }
    
    
  )
  
}
