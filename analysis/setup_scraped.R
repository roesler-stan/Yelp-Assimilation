rm(list = ls())
options(scipen=999)

# set the working directory to the data folder
setwd("/Users/katharina/Dropbox/Projects/Yelp/Data")
scraped_file <- "yelp_reviews_merged.csv"
scraped_image <- "scraped.Rdata"
source("/Users/katharina/Dropbox/Projects/Yelp/Code/analysis/helper/make_title.R")

# Load the image, if it's present and up to date
load(scraped_image)

scraped_data <- read.csv(scraped_file)
#table(scraped_data$is_mexican)

scraped_data$cbsa_hisp_div_white_lt_hs <- scraped_data$cbsa_hispanic_educ_lt_hs / scraped_data$cbsa_white_educ_lt_hs

scraped_data$cbsa_cbsaname <- sapply(as.character(scraped_data$cbsa_cbsaname), function(x) {
  return(gsub("Metro Area", "", x))
})

scraped_data$business_name <- sapply(as.character(scraped_data$business_name),
                                     function(x) { return(make_title(x)) })

scraped_data_nochains <- subset(scraped_data, is_chain == 0)
scraped_data_chains <- subset(scraped_data, is_chain == 1)
scraped_data_chains <- subset(scraped_data, is_chain == 1)
subsets <- list(scraped_data, scraped_data_nochains, scraped_data_chains)

cbsa_subsets <- lapply(seq_along(subsets), function(i) {
  subset <- subsets[[i]]
  cbsa_clean <- ddply(subset, .(cbsa_cbsaname), numcolwise(mean, na.rm = T))
  cbsa_clean <- subset(cbsa_clean, !is.na(cbsa_cbsaname))
  cbsa_clean <- subset(cbsa_clean, cbsa_cbsaname != "")
  
  cbsa_business_data <- ddply(subset, .(cbsa_cbsaid, business_id),
                              summarise,
                              business_name = unique(business_name),
                              reviews = sum(!is.na(business_id)),
                              is_chain = mean(is_chain))
  
  max_reviews <- ddply(cbsa_business_data, .(cbsa_cbsaid),
                         function(x) x[which.max(x$reviews), ])
  
  max_reviews <- rename(max_reviews, replace = c("business_name" = "top_business",
                                                 "reviews" = "top_business_reviews",
                                                 "is_chain" = "top_is_chain"))
  max_reviews$business_id <- NULL
  
  cbsa_data_custom <- ddply(cbsa_business_data, .(cbsa_cbsaid), summarise,
                            restaurant_count = length(unique(reviews)),
                            review_count = sum(reviews, na.rm = T))
  
  cbsa_clean <- merge(cbsa_clean, cbsa_data_custom, by = "cbsa_cbsaid",
                     all.x = T, all.y = F)
  
  cbsa_clean <- merge(cbsa_clean, max_reviews, by = "cbsa_cbsaid",
                     all.x = T, all.y = F)
  
  vars <- grep('_present$', names(cbsa_clean), value = T, perl = T)
  for (var in vars) {
    cbsa_clean[, var] <- cbsa_clean[, var] * 100
  }
  
  cbsa_clean$cbsa_ethnicity_mexican_percent_log <- log(cbsa_clean$cbsa_ethnicity_mexican_percent + 0.0001)
  cbsa_clean$cbsa_ethnicity_mexican_percent_log_sq <- cbsa_clean$cbsa_ethnicity_mexican_percent_log ** 2
  cbsa_clean$cbsa_language_spanish_english_notwell_log <- log(cbsa_clean$cbsa_language_spanish_english_notwell + 0.0001)
  
  cbsa_clean$cbsa_nativity_pct_foreign_hispanic_sq <- cbsa_clean$cbsa_nativity_pct_foreign_hispanic ** 2
  cbsa_clean$cbsa_language_spanish_english_notwell_log_sq <- cbsa_clean$cbsa_language_spanish_english_notwell_log ** 2
  
  cbsa_clean$cbsa_origin_mexican_pct_log <- log(cbsa_clean$cbsa_origin_mexican_pct + 0.0001)
  cbsa_clean$cbsa_origin_mexican_pct_log_sq <- cbsa_clean$cbsa_origin_mexican_pct_log ** 2
  
  cbsa_clean
})

cbsa_data <- cbsa_subsets[[1]]
cbsa_data_nochains <- cbsa_subsets[[2]]
cbsa_data_chains <- cbsa_subsets[[3]]

save.image(scraped_image)
