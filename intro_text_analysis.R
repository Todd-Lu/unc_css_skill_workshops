library(stringr)
library(tidyverse)
library(ggplot2)

wd = ''
setwd(wd)


# In this workshop, we are going to use text data on a random sample of newspaper articles covering George Floyd's death (5k articles, between May and July 2020)


## Importing and Managing Text Data

  # In general, I like to keep the "text data" and the "metadata" (md) in separate files, connected together via an common id
floyd_fulltext = read_csv('floyd_news_fulltext.csv')
floyd_md = read_csv('floyd_news_md.csv')

head(floyd_md)
head(floyd_fulltext)

## Pre-Processing Text Data in Tidy Text Format
library(tidytext)

# unnest tokens turns text data into a "document - term" format
floyd_words = floyd_fulltext %>%
  unnest_tokens(word, fulltext)

floyd_words %>%
  count(word, sort = T) %>%
  head(20)


# using a dictionary of "Stop Words" to remove noise

data(stop_words)

  # you can use your own stop words as well
custom_stop_words = read_csv('custom_stop_words.csv')

stop_words = stop_words %>%
  bind_rows(custom_stop_words)

stop_words

# remove stop words from tokens

floyd_words = floyd_words %>%
  anti_join(stop_words)

  # seems reasonable
floyd_words %>%
  count(word, sort = T) %>%
  head(20)


# can combine with meta data (e.g. census region)
floyd_words = floyd_words %>%
  left_join(floyd_md %>%
              select(pq_id, census_region))

top_words_census = floyd_words %>%
  group_by(census_region) %>%
  count(word, sort = T)

head(top_words_census %>% filter(census_region == 'Northeast'), 20)
head(top_words_census %>% filter(census_region == 'North Central'), 20)
head(top_words_census %>% filter(census_region == 'South'), 20)
head(top_words_census %>% filter(census_region == 'West'), 20)


## Dictionary Methods

# One thing we can do is search documents to identify specific terms:

crime_frame = c('riot',
                  'lawlessness',
                  'damage',
                  'smashed',
                  'graffiti',
                  'burn',
                  'burglary',
                'looting')

floyd_fulltext$crime = str_detect(floyd_fulltext$fulltext,
                                  str_c(crime_frame,
                                        collapse =  '|')) %>%
  as.numeric()
  

floyd_fulltext[floyd_fulltext$crime == 1,]$fulltext[1]



# Sentiment analysis

  # there are a wide variety of "sentiment" dictionaries from which to choose. And each one is coded differently depending on the atuhor. The "right" one depends on your research question. 

afinn = get_sentiments('afinn') # negative to positive scores (-5 to 5)
bing = get_sentiments('bing') # brinary positive and negative
nrc = get_sentiments('nrc') # categorical into emotions

afinn
bing 
nrc


nrc_floyd = floyd_words %>%
  inner_join(nrc)


  # not necessarily applicable for some words
nrc_floyd %>%
  count(word, sentiment, sort = TRUE) %>%
  head(20)


  # how positive and negative is each document?
afinn_floyd = floyd_words %>%
  inner_join(afinn)

afinn_floyd

afinn_floyd %>%
  count(word, value, sort = TRUE) %>%
  head(20)

  #calculate the sentiment "value" of each document:

doc_sentiment = afinn_floyd %>%
  group_by(pq_id) %>%
  summarise(doc_value = sum(value))


  #summary statistics reveal that coverage is largely of "negative" sentiment -- although not sure what this means 
summary(doc_sentiment$doc_value)

ggplot(doc_sentiment, aes(x = doc_value)) +
  geom_histogram(colour = 'black',
                 fill = 'white') +
  theme_minimal()



## Named-Entity Recognition
library(spacyr)

spacy_initialize()


# apply NER -- this usually takes a while, so we only sampled 30 articles
sample_floyd_fulltext = floyd_fulltext %>%
  sample_n(30)

floyd_ent = spacy_parse(sample_floyd_fulltext$fulltext,
                        lemma = TRUE,
                        entity = TRUE,
                        nounphrase = TRUE)


  # now let's take a look at the structure:
floyd_ent


  # from here, we can identify specific rows we might want
entities_in_text = entity_extract(floyd_ent)

orgs_people = entities_in_text %>%
  filter(entity_type %in% c('ORG', 
                            'PERSON',
                            'NORP')) %>%
  distinct(doc_id,
           entity,
           entity_type)

orgs_people %>% head(20)



  # we can also have spacy extract words that have entities attached to them
entities_only = spacy_extract_entity(sample_floyd_fulltext$fulltext)

entities_only


  #closes the session for spacy, as uses a lot of space
spacy_finalized()




## Structural Topic Modeling
library(stm) #structuraltopicmodel.com

# combine together fulltext and metadata into one dataset
floyd_fulltext = read_csv('floyd_news_fulltext.csv')
floyd_md = read_csv('floyd_news_md.csv')
floyd_fulltext_md = floyd_md %>%
  left_join(floyd_fulltext)

# select only 

custom_stop_words = read_csv('custom_stop_words.csv')

# pre-process the text -> becomes a list of various datasets used inthe topic model
blm_processed_text = textProcessor(floyd_fulltext_md$fulltext,
                                   metadata = floyd_fulltext_md,
                                   customstopwords = custom_stop_words$word)


# prepare the documents
out = prepDocuments(blm_processed_text$documents,
                    blm_processed_text$vocab,
                    blm_processed_text$meta,
                    lower.thresh = 5)


# now let's run the actual structural topic model -- if you have a big dataset, this will take a while!!!
blm_fit20 = stm(documents = out$documents,
                vocab = out$vocab,
                K = 20,
                max.em.its = 75, 
                data = out$meta, 
                init.type = "Spectral") 


# we can begin looking at the specific topics themselves:

# 1) Looking at collections of words associated with each topic
#FREX words = WIEGHTS WORDS BY FREQUENCY AND EXCLUSIVITY IN TOPIC -- words that are more exclusive to a topic
#lift words = give words higher precedence that appear less frequently in other topics
#score words = similar to lift except a different measurement of log frequency of word in topic / log frequency of word in other topics

labelTopics(blm_fit20, c(1:20))

 

# 2) Examine documents highly associated with each topic

thoughts = findThoughts(blm_fit20,
                        texts = out$meta$fulltext %>%
                          substr(1, 200),
                        n = 5,
                        topics = 15)

thoughts

# 3) eventually, can output topic proportions into your original dataset and work with these topic proportions

fit_df = make.dt(blm_fit20) 

fit_df %>% head(10)


combined_df = fit_df %>%
  bind_cols(out$meta)

