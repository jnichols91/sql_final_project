rm ( list = ls() )
library(tidyverse)
library(reshape2)

load('../data/my_fires.rda')
fires_with_regions <- readRDS('../data/fires_clean.rds')

my_data <- my_data %>% 
  filter(STATE != 'IN')
my_fires <- my_data %>% 
  select(-c('FIRE_CODE', 'OWNER_CODE', 'OWNER_DESCR'))
my_fires$date <- as.Date(my_fires$date)
my_fires$cont_date <- as.Date(my_fires$cont_date)

# work around to replace blank cells with common NA
ix <- which(my_fires$CONT_TIME=='')
my_fires$CONT_TIME[ix] <-1
my_fires$CONT_TIME[ix] <- NA

regions <- fires_with_regions %>% 
  filter(STATE %in% c('FL', 'CO', 'WY', 'AL', 'DE', 'CT')) %>% 
  select(c('FPA_ID', 'eco1', 'STATE')) %>% 
  mutate(colsplit(eco1, ' ', c('eco_id', 'eco_region'))) %>% 
  select(-eco1)


regions_glimpse <- regions %>% 
  group_by(STATE) %>% 
  slice(1:2)

fires_glimpse <- my_fires %>% 
  group_by(STATE) %>% 
  slice(1:6)


