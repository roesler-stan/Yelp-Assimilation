library(plyr)

## Create subsets
italian_data <- subset(academic_data, category == "Italian")
mexican_data <- subset(academic_data, category == "Mexican")
american_data <- subset(academic_data, category == "American")

## Create dataset where category is either Italian, Mexican, or American
cat_data <- subset(academic_data, category %in% c("Mexican", "Italian", "American"))
cat_data$category <- droplevels(cat_data$category)

dim(cat_data)
