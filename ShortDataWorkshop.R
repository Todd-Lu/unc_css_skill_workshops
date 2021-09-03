library(tidyverse)
library(magrittr)
library(jsonlite)
library(tm)
library(tidytext)
library(lubridate)

#First thing we need to do is load the data into R. Since it's a json, we'll use stream_in from jsonlite to read the data into a data frame.
reviews <- stream_in(file("Appliances_50.json\\Appliances_5.json"))

#Now that we have it loaded, we can take a quick look at what we have here.
head(reviews)
utils::View(reviews)


#We're going to approach the text data here in two ways. First we'll look at it in a corpus format, and second we'll do tidytext.
#There are a couple of things we need to do first.
#First let's clean up some of the metadata, in particular the time variables reviewTim eand unixReviewTime. 
#reviewTime is in an ugly format so it's best to just clean it up since it's fast to do. unixReviewTime is actually perfectly fine but isn't really human interpretable, 
#and may have more detailed information than just day/month/year.
head(reviews$reviewTime)
class(reviews$reviewTime)

#reviewTime is in a mm dd, yyyy format, and it's a string. 
#So let's get this a little cleaner and easier to work with using the lubridate package, which ispart of tidyverse. mdy() is a lubridate function, telling it to recognize
#a string as being organized as month, day, then year.
reviews$date <- mdy(reviews$reviewTime) 
head(reviews$date)

class(reviews$date)
#The date is a bit easier and more standardized to read now, and instead of being saved as a character it's saved as a date object. Date objects are much easier
#to work with than strings. You can operate on them with addition, subtraction, easily plot with them, etc. For example, if you add 1 to one of these dates, it adds a day.
reviews$date[1] + 1


#unixReviewTime can also be reformatted using lubridate. Unix timestamps are the number of seconds since January 1, 1970. 
reviews$time <- as_datetime(reviews$unixReviewTime)
head(reviews$time)

#looks like it was just another representation of the day of sale. It is stored differently though. If you add 1 to one of these, it adds a second instead of a day.
reviews$time[1] + 1

#Before going too much further, let's organize this by date to give it a little more structure. We'll use the arrange() function, which is part of dplyr/tidyverse.
reviews <- arrange(reviews, date)
utils::View(reviews)

#Some weird sparsity in terms of dates, it jumps a bunch of years for some reason. Also, it looks like there are a fair amount of duplicates. Also also, it looks like
#one of the reviewers is having a bit of a reflective moment as they review their dryer vent. Well let's take care of the duplicates first. Can use another dyplr/tidyverse
#function for this, distinct()
nrow(reviews)
reviews <- distinct(reviews)
nrow(reviews)

#Still more than enough left to work with here. We have the duplicates cleaned, and have it arranged by date, so we can put in some unique doc ids now to keep track
#of our observations. seq_len is a sequence generator, and seq_len(nrow(reviews)) is going to create a sequence from 1 to the number of rows of the data frame reviews
#and we can use that to create the unique doc ids. 
seq_len(nrow(reviews))
reviews$doc_id <- seq_len(nrow(reviews)) 

#The corpus format needs doc_id as the first column, and then needs the text as the second column, so we'll rename the review text and then move both cols up front.
colnames(reviews)
colnames(reviews)[8]
colnames(reviews)[8] <- "text"


reviews <- reviews %>%
  select(doc_id, text, date, everything())
  

#Now we'll put this in a corpus structure, from the tm package. This structure is good for document level work. If you care about word distributions across documents etc.
#The VCorpus has a few arguments you need to give it. First is the data. You can give it data from a vector, from a file, from a PDF, there's a lot of sources.
#getReaders() will give you a list of the current options. We have it already loaded in as a DF so we'll give it the data frame variable, and tell the vcorpus that
#it's reading a data frame. 

corpus <- VCorpus(DataframeSource(reviews))

#You can easily filter, print, stem, clean, and deal with the corpus as a whole.
#There are two different storages for metadata in the corpus. First is at the corpus level, and second is at the document level.
#meta is the function, corpus our corpus here, and the subset of [1] is telling meta to give us the metadata of the first document in our corpus.
meta(corpus[1])
#You can also tell R to give you multiple sets of metadata at once. 1:5 is giving us the metadata for documents 1:5. Document level metadata are stored
#as dataframes, which you can start to see when it prints out multiple. 
meta(corpus[1:5])

#To access each different review's text, you can use the content function, and you need to use double brackets instead of single brackets. 
content(corpus[[1]])

#Now that we have our reviews in a corpus we can do some transformations here. You can use getTransformations() to see what the options within tm are.
#We'll be doing a few specific cleaning transformations on the data that are fairly standard, and help in reducing complexity and making sense of text across a corpus of documents.
#We'll do the following.

#1 - transforming all text to lowercase. 
#2 - stripping out punctuation
#3 - stemming
#4 - remove extra whitespace
#5 - remove numbers

#Lowercase. Helps to reduce complexity of your text data. 
corpus <- tm_map(corpus, content_transformer(tolower))

#
content(corpus[[1]])
content(corpus[[10]])
content(corpus[[100]])

#Punctuation. This also reduces complexity. If you care about contractions there are options to keep intra word contractions.
#The basic removePunctuation works off a standard regular expression [:punct:]. 
corpus <- tm_map(corpus, removePunctuation)

#Stemming removes the ends of words, for example "likes" can be stemmed to "like." There are more and less aggressive versions of stemming, this is a medium variant.
#Can see how it works in action here. It again reduces complexity of the langauge and allows later analysis to interact with less word forms.
content(corpus[[1]])
corpus <- tm_map(corpus, stemDocument)
content(corpus[[1]])

#we'll strip any extra whitespace that might be in the documents.
corpus <- tm_map(corpus, stripWhitespace)


#We'll remove the numbers since they're just hard to interpret in this sort of approach.
corpus <- tm_map(corpus, removeNumbers)

#Lastly we'll remove stopwords, which are very common words that are generally not meaningful (words like for, and, etc). When you remove these you're making some assumptions
#about the language of the documents, primarily that the distribution of the stopwords are fairly evenly distributed across the documents in the corpus. Depending
#on your data and your question you may or may not want to remove them. Stopwords are available in many languages, and you can import them as a vector and use them. 
corpus <- tm_map(corpus, removeWords, stopwords("english"))

#Now we can create a document term matrix, which is exactly what it sounds like. it's a matrix representation of your documents. Each row is a document, and each column
#is a word that is present in the corpus. Each cell is how many times in a particular document a particular word appears. This is one fundamental structure of text analysis.
dtm <- DocumentTermMatrix(corpus)

#To look at it in a non list format, can transform to a matrix just to look at it. 
dtmdf <- as.matrix(dtm)




#Next we'll look at the data in a tidytext format. We'll use the same review data, which is already cleaned.
#Tidytext is part of the tidyverse set of packages, and we'll be operating on the dataframe itself.
#The ultimate goal of a tidytext format is to split documents into individual words, or tokens. You can also tokenize bigrams if you'd like (two sequential words), or
#This sort of format is useful if you want to do word level analysis, like sentiment analysis.

#First we'll split up each review into unigram tokens using unnest_tokens from the tidytext package. The first argument is the data frame, the second argument
#is the output column name (this will be generated), the third argument is the input column that has the text we're tokenizing, and the fourth argument is
#the format of how we're tokenizing. It's first set as words, so it'll just do unigrams. We're also transforming everything to lower case here.
tidyreviews <- unnest_tokens(reviews, word, text, token = "words", to_lower = TRUE)

#Let's take a look at what the most common words are.
tidyreviews %>% count(word, sort = TRUE)

#So we can see that there are still stop words in here, lots of words we really don't care about. Tidytext has a built in stopword library we can use.
tidyreviews <- tidyreviews %>%
  anti_join(stop_words)

#Also have some numbers in there. There's not a great, clean way to remove numbers built into tidytext, but we can use subsetting and regular expressions to do it.
#What this is doing is it's subsetting the data frame. Within the tidyreviews df, it's looking for regular expression matches in the tidyreviews$word column, then removing
#those rows. \b matches to a word boundary, \d matches any numeric character, the + matches the preceding one or more times, and \b matches a word boundary. It's searching for 
#any amount of numeric characters that are surrounded by word boundaries, then removing them.

tidyreviews <- tidyreviews[-grep("\\b\\d+\\b", tidyreviews$word),]


#Now if we print this out we get something a little cleaner.
tidyreviews %>% count(word, sort = TRUE)

#If we wanted to do this with bigrams, we could do it this way. Instead of 
bigramreviews <- unnest_tokens(reviews, bigram, text, token ="ngrams", n = 2, collapse = FALSE)

#You can then split your bigrams into two columns if you want. This is separating based on a whitespace character. You could do something similar for trigrams, or any ngrams. 
bigramreviews <- bigramreviews %>%
  separate(bigram, c("word1", "word2"), sep = " ")

