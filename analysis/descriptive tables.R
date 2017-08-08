setwd("/Users/katharina/Dropbox/Projects/Yelp/Output")

descriptive_row <- function(x) {
  c(Mean = mean(x, na.rm=T), SD = sd(x, na.rm=T), N = sum(!is.na(x)))
}

# Scraped reviews table
grep("date", names(scraped_data), value=T)
cols <- c("word_count", "is_chain", "mexican_present", "authentic_present",
          "dollars", "reviewer_rating")
table <- data.frame(t(apply(scraped_data[, cols], 2, descriptive_row)))
table$Mean <- round(table$Mean, 2)
table$SD <- round(table$SD, 2)
table
write.csv(table, "desc_scraped_reviews.csv")

table(scraped_data$state)

# Scraped CBSA Table
grep("hisp", names(cbsa_data_nochains), value=T)
cols <- c("cbsa_total_residents", "cbsa_mean_inc",
"cbsa_summary_perc_hispanic", "cbsa_ethnicity_mexican_percent",
"cbsa_nativity_pct_foreign_hispanic",
"cbsa_language_spanish_english_notwell", "cbsa_hisp_div_white_lt_hs")
table <- data.frame(t(apply(cbsa_data_nochains[, cols], 2, descriptive_row)))
table$Mean <- round(table$Mean, 2)
table$SD <- round(table$SD, 2)
table
write.csv(table, "desc_scraped_cbsa_nochains.csv")

# List of scraped CBSA's
cbsas <- unique(cbsa_data_nochains$cbsa_cbsaname)
write.csv(cbsas, "desc_cbsa_list.csv")


# Academic Reviews table
table(academic_data$category)
table(academic_data$year)

grep("mexican", names(academic_data), value=T)
cols <- c("word_count", "stars_business", "stars_review", "average_stars",
          "authentic_present", "ethnicity_present")
academic_data$word_count <- as.numeric(academic_data$word_count)
academic_data$stars_business <- as.numeric(academic_data$stars_business)
academic_data$stars_review <- as.numeric(academic_data$stars_review)
academic_data$average_stars <- as.numeric(academic_data$average_stars)
academic_data$authentic_present <- as.numeric(academic_data$authentic_present)
academic_data$ethnicity_present <- as.numeric(academic_data$ethnicity_present)
table <- data.frame(t(apply(academic_data[, cols, with=F], 2, descriptive_row)))
table$Mean <- round(table$Mean, 2)
table$SD <- round(table$SD, 2)
table
write.csv(table, "desc_academic_reviews.csv")
