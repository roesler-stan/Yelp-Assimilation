library(texreg)
library(plyr)
library(stats)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output")

cbsa_data_chains$cbsa_ethnicity_mexican_percent_log <- log(cbsa_data_chains$cbsa_ethnicity_mexican_percent + 0.0001)
cbsa_data_chains$cbsa_ethnicity_mexican_percent_log_sq <- cbsa_data_chains$cbsa_ethnicity_mexican_percent_log ** 2
cbsa_data_chains$cbsa_language_spanish_english_notwell_log <- log(cbsa_data_chains$cbsa_language_spanish_english_notwell + 0.0001)

cbsa_data_chains$cbsa_nativity_pct_foreign_hispanic_sq <- cbsa_data_chains$cbsa_nativity_pct_foreign_hispanic ** 2
cbsa_data_chains$cbsa_language_spanish_english_notwell_log_sq <- cbsa_data_chains$cbsa_language_spanish_english_notwell_log ** 2

controls1 = c("cbsa_ethnicity_mexican_percent_log")
controls2 = c("cbsa_ethnicity_mexican_percent_log", "cbsa_ethnicity_mexican_percent_log_sq")
controls3 = c("cbsa_language_spanish_english_notwell_log")
controls4 = c("cbsa_ethnicity_mexican_percent_log", "cbsa_language_spanish_english_notwell_log")

# Standardize independent variables
cbsa_data_chains_std <- cbsa_data_chains
for (var in c(controls2, "cbsa_language_spanish_english_notwell_log")) {
  cbsa_data_chains_std[, var] <- (cbsa_data_chains[, var] - mean(cbsa_data_chains[, var], na.rm = T)) / sd(cbsa_data_chains[, var], na.rm = T)  
}

vars1 <- c(controls1, "mexican_present")
vars2 <- c(controls2, "mexican_present")
vars3 <- c(controls3, "mexican_present")
vars4 <- c(controls4, "mexican_present")

model1 <- lm(mexican_present ~ ., data = cbsa_data_chains_std[, vars1])
model2 <- lm(mexican_present ~ ., data = cbsa_data_chains_std[, vars2])
model3 <- lm(mexican_present ~ ., data = cbsa_data_chains_std[, vars3])
model4 <- lm(mexican_present ~ ., data = cbsa_data_chains_std[, vars4])

AIC(model1, model2, model3, model4)

outfile <- "models_chains.doc"
htmlreg(list(model1, model2, model3, model4),
        center = F, file = outfile, digits = 2,
        custom.model.names = c("Model 1", "Model 2", "Model 3", "Model 4"),
        caption = paste0("Chains' Linear Regression Predicting % Reviews Mentioning Mexican"),
        caption.above = T, inline.css = F, longtable = T)
