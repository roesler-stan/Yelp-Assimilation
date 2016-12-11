rm(list = ls())
library(data.table)
options(scipen=999)

# set the working directory to the data folder
setwd("/Users/katharina/Dropbox/Projects/Yelp/Data")
academic_file <- "academic/academic_dataset_cleaned.csv"
scraped_file <- "yelp_reviews_merged.csv"
academic_image <- "academic.Rdata"

# Load the image, if it's present and up to date
load(academic_image)

length(unique(academic_data$business_id))

table(academic_data$year)

# Otherwise, clean the data
academic_cols <- names(read.csv(academic_file, nrows = 100))
academic_cols

# Read in select columns from academic file, which is otherwise 3GB
cols <- c("text", "year", "date", "category", "stars_review", "stars_business", "average_stars",
          "is_chain", "city", "state", "name_business", "name_review", "business_id", "user_id")
counts <- grep("_count", academic_cols, value = T)
present <- grep("_present", academic_cols, value = T)
cols <- c(cols, counts, present)
cols <- grep("^((?!perword).)*$", cols, value = T, perl = T)

# Check which columns will be excluded
academic_cols[!academic_cols %in% cols]

academic_data <- data.table::fread(academic_file, sep = ",", select = cols, verbose = T)
# 1,630,712 rows

# Check if any columns weren't included
cols[!cols %in% names(academic_data)]

table(academic_data$year)

# Only include academic data from 2015 and 2016 to be comparable to scraped data and each other?
# academic_data <- subset(academic_data, year == 2015 | year == 2016)

save.image(academic_image)
