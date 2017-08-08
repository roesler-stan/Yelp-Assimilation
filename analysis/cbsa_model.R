library(texreg)
library(plyr)
library(stats)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output")

cor.test(cbsa_data$cbsa_ethnicity_mexican_percent, cbsa_data$mexican_present,
         method = "pearson", use="pairwise.complete.obs")

cor.test(cbsa_data$cbsa_ethnicity_mexican_percent_log, cbsa_data$mexican_present,
    method = "pearson", use="pairwise.complete.obs")

controls1 = c("cbsa_ethnicity_mexican_percent_log", "cbsa_ethnicity_mexican_percent_log_sq")
controls2 = c(controls1, "cbsa_nativity_pct_foreign_hispanic", "cbsa_nativity_pct_foreign_hispanic_sq",
              "cbsa_summary_dissim_idx_hisp_2010",
              "cbsa_language_spanish_english_notwell_log", "cbsa_language_spanish_english_notwell_log_sq",
              "cbsa_hisp_div_white_lt_hs")
controls3 = c("cps_mex_interracial_pct", "cbsa_origin_mexican_pct_log", "cbsa_origin_mexican_pct_log_sq")


# Standardize independent variables
cbsa_data_std <- cbsa_data
for (var in c(controls2, controls3)) {
  cbsa_data_std[, var] <- (cbsa_data[, var] - mean(cbsa_data[, var], na.rm = T)) / sd(cbsa_data[, var], na.rm = T)  
}

vars1 <- c(controls1, "mexican_present")
vars2 <- c(controls2, "mexican_present")
vars3 <- c(controls3, "mexican_present")
vars4 <- c(controls2, controls3, "mexican_present")

model1 <- lm(mexican_present ~ ., data = cbsa_data_std[, vars1])
model2 <- lm(mexican_present ~ ., data = cbsa_data_std[, vars2])
model3 <- lm(mexican_present ~ ., data = cbsa_data_std[, vars3])
model4 <- lm(mexican_present ~ ., data = cbsa_data_std[, vars4])

outfile <- "models.doc"
htmlreg(list(model1, model2, model3, model4),
        center = F, file = outfile, digits = 2,
        custom.model.names = c("Model 1", "Model 2", "Model 3", "Model 4"),
        caption = paste0("Linear Regression Predicting % Reviews Mention 'Mexican'"),
        caption.above = T, inline.css = F, longtable = T)
