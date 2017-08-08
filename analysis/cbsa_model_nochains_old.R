library(texreg)
library(plyr)
library(stats)
library(Hmisc)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output")

cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log <- log(cbsa_data_nochains$cbsa_ethnicity_mexican_percent + 0.0001)
cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log_sq <- cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log ** 2
cbsa_data_nochains$cbsa_language_spanish_english_notwell_log <- log(cbsa_data_nochains$cbsa_language_spanish_english_notwell + 0.0001)

cbsa_data_nochains$cbsa_nativity_pct_foreign_hispanic_sq <- cbsa_data_nochains$cbsa_nativity_pct_foreign_hispanic ** 2
cbsa_data_nochains$cbsa_language_spanish_english_notwell_log_sq <- cbsa_data_nochains$cbsa_language_spanish_english_notwell_log ** 2


controls1 = c("cbsa_ethnicity_mexican_percent_log")
controls2 = c("cbsa_ethnicity_mexican_percent_log", "cbsa_ethnicity_mexican_percent_log_sq")
controls3 = c("cbsa_language_spanish_english_notwell_log")
controls4 = c("cbsa_ethnicity_mexican_percent_log", "cbsa_language_spanish_english_notwell_log")
controls5 = c("cbsa_nativity_pct_foreign_entered_before_90")
controls6 = c(controls4, "cbsa_nativity_pct_foreign_entered_before_90")

# Standardize independent variables
cbsa_data_nochains_std <- cbsa_data_nochains
standardize_vars <- c("cbsa_ethnicity_mexican_percent_log", "cbsa_language_spanish_english_notwell_log",
                      "cbsa_nativity_pct_foreign_entered_before_90")
for (var in standardize_vars) {
  cbsa_data_nochains_std[, var] <- (cbsa_data_nochains[, var] - mean(cbsa_data_nochains[, var], na.rm = T)) / sd(cbsa_data_nochains[, var], na.rm = T)  
}
all_vars <- c("mexican_present", standardize_vars, "cbsa_ethnicity_mexican_percent_log_sq")
cbsa_data_nochains_std <- na.omit(cbsa_data_nochains_std[, all_vars])

vars1 <- c(controls1, "mexican_present")
vars2 <- c(controls2, "mexican_present")
vars3 <- c(controls3, "mexican_present")
vars4 <- c(controls4, "mexican_present")
vars5 <- c(controls5, "mexican_present")
vars6 <- c(controls6, "mexican_present")

model1 <- lm(mexican_present ~ ., data = cbsa_data_nochains_std[, vars1])
model2 <- lm(mexican_present ~ ., data = cbsa_data_nochains_std[, vars2])
model3 <- lm(mexican_present ~ ., data = cbsa_data_nochains_std[, vars3])
model4 <- lm(mexican_present ~ ., data = cbsa_data_nochains_std[, vars4])
model5 <- lm(mexican_present ~ ., data = cbsa_data_nochains_std[, vars5])
model6 <- lm(mexican_present ~ ., data = cbsa_data_nochains_std[, vars6])

AIC(model1, model2, model3, model4, model5, model6)

rcorr(cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log, cbsa_data_nochains$cbsa_language_spanish_english_notwell)
var.test(model1, model4)
var.test(model3, model4)
var.test(model3, model6)
var.test(model1, model6)

outfile <- "models_nochains2.doc"
htmlreg(list(model1, model2, model3, model4, model5, model6),
        center = F, file = outfile, digits = 2,
        custom.model.names = c("Model 1", "Model 2", "Model 3", "Model 4", "Model 5", "Model 6"),
        caption = paste0("Non-Chains' Linear Regression Predicting % Reviews Mentioning Mexican"),
        caption.above = T, inline.css = F, longtable = T)
