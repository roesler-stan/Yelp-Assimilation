library(texreg)
library(plyr)
library(stats)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output")

cor.test(cbsa_data$cbsa_ethnicity_mexican_percent, cbsa_data$mexican_present,
         method = "pearson", use="pairwise.complete.obs")

cor.test(cbsa_data$cbsa_ethnicity_mexican_percent_log, cbsa_data$mexican_present,
    method = "pearson", use="pairwise.complete.obs")


cbsa_data$cbsa_ethnicity_mexican_percent_log <- log(cbsa_data$cbsa_ethnicity_mexican_percent + 0.0001)
cbsa_data$cbsa_ethnicity_mexican_percent_log_sq <- cbsa_data$cbsa_ethnicity_mexican_percent_log ** 2
cbsa_data$cbsa_language_spanish_english_notwell_log <- log(cbsa_data$cbsa_language_spanish_english_notwell + 0.0001)

cbsa_data$cbsa_nativity_pct_foreign_hispanic_sq <- cbsa_data$cbsa_nativity_pct_foreign_hispanic ** 2
cbsa_data$cbsa_language_spanish_english_notwell_log_sq <- cbsa_data$cbsa_language_spanish_english_notwell_log ** 2

controls1 = c("cbsa_ethnicity_mexican_percent_log", "cbsa_ethnicity_mexican_percent_log_sq")
controls2 = c(controls1, "cbsa_nativity_pct_foreign_hispanic", "cbsa_nativity_pct_foreign_hispanic_sq",
              "cbsa_summary_dissim_idx_hisp_2010",
              "cbsa_language_spanish_english_notwell_log", "cbsa_language_spanish_english_notwell_log_sq",
              "cbsa_hisp_div_white_lt_hs")

# Standardize independent variables
cbsa_data_std <- cbsa_data
for (var in controls2) {
  cbsa_data_std[, var] <- (cbsa_data[, var] - mean(cbsa_data[, var], na.rm = T)) / sd(cbsa_data[, var], na.rm = T)  
}

vars1 <- c(controls1, "mexican_present")
vars2 <- c(controls2, "mexican_present")
vars3 <- c(controls1, "authentic_present")
vars4 <- c(controls2, "authentic_present")

model1 <- lm(mexican_present ~ ., data = cbsa_data_std[, vars1])
model2 <- lm(mexican_present ~ ., data = cbsa_data_std[, vars2])
model3 <- lm(authentic_present ~ ., data = cbsa_data_std[, vars3])
model4 <- lm(authentic_present ~ ., data = cbsa_data_std[, vars4])

outfile <- "models.doc"
htmlreg(list(model1, model2, model3, model4),
        center = F, file = outfile, digits = 2,
        custom.model.names = c("Mexican Present", "Mexican Present",
                               "Authentic Present", "Authentic Present"),
        caption = paste0('Linear Regression'),
        caption.above = T, inline.css = F, longtable = T)
