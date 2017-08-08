library(texreg)
library(plyr)
library(stats)
library(Hmisc)
library(ggplot2)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output")

cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log <- log(cbsa_data_nochains$cbsa_ethnicity_mexican_percent + 0.0001)
cbsa_data_nochains$cbsa_language_spanish_english_notwell_log <- log(cbsa_data_nochains$cbsa_language_spanish_english_notwell + 0.0001)
cbsa_data_nochains$exotic_present_log <- log(cbsa_data_nochains$exotic_present + 0.0001)

ggplot(cbsa_data_nochains, aes(x=cbsa_ethnicity_mexican_percent_log, y=exotic_present_log)) +
  geom_point() + theme_bw()

grep("foreign", names(cbsa_data_nochains), value=T)

rcorr(cbsa_data_nochains$cbsa_nativity_pct_foreign_hispanic, cbsa_data_nochains$cbsa_nativity_pct_foreign_entered_before_90, type="pearson")

hist(cbsa_data_nochains$exotic_present)

outcomes = c("Mexican"="mexican_present", "Authentic"="authentic_present",
             "Exotic"="exotic_present")
nothing <- lapply(seq_along(outcomes), function(i) {
  outcome <- outcomes[[i]]
  outcome_nice <- names(outcomes)[[i]]
  controls1 = c("cbsa_ethnicity_mexican_percent_log")
  controls2 = c("cbsa_language_spanish_english_notwell_log")
  controls3 = c("cbsa_nativity_pct_foreign_hispanic")
  controls4 = c("cps_mex_interracial_pct")
  controls5 = c(controls1, controls2, controls3, controls4)
  
  # Standardize independent variables
  cbsa_data_nochains_std <- cbsa_data_nochains
  standardize_vars <- c("cbsa_ethnicity_mexican_percent_log", "cbsa_language_spanish_english_notwell_log",
                        "cbsa_nativity_pct_foreign_hispanic", "cps_mex_interracial_pct")
  for (var in standardize_vars) {
    cbsa_data_nochains_std[, var] <- (cbsa_data_nochains[, var] - mean(cbsa_data_nochains[, var], na.rm = T)) / sd(cbsa_data_nochains[, var], na.rm = T)  
  }
  all_vars <- c(outcome, standardize_vars, "cbsa_ethnicity_mexican_percent_log_sq")
  cbsa_data_nochains_std <- na.omit(cbsa_data_nochains_std[, all_vars])
  
  vars1 <- c(controls1, outcome)
  vars2 <- c(controls2, outcome)
  vars3 <- c(controls3, outcome)
  vars4 <- c(controls4, outcome)
  vars5 <- c(controls5, outcome)
  
  formula = paste0(outcome, " ~ .")
  model1 <- lm(formula, data = cbsa_data_nochains_std[, vars1])
  model2 <- lm(formula, data = cbsa_data_nochains_std[, vars2])
  model3 <- lm(formula, data = cbsa_data_nochains_std[, vars3])
  model4 <- lm(formula, data = cbsa_data_nochains_std[, vars4])
  model5 <- lm(formula, data = cbsa_data_nochains_std[, vars5])
  
  # BIC(model1, model2, model3, model4, model5)
  
  ## F-test
  # rcorr(cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log, cbsa_data_nochains$cbsa_language_spanish_english_notwell)
  # var.test(model1, model4)
  # var.test(model3, model4)
  # var.test(model3, model5)
  
  outfile <- paste0("models_nochains_", outcome, ".doc")
  title = paste0("Non-Chains' Linear Regression Predicting % Reviews Mentioning '", outcome_nice,"'")
  htmlreg(list(model1, model2, model3, model4, model5),
          center = F, file = outfile, digits = 2,
          custom.model.names = c("Model 1", "Model 2", "Model 3", "Model 4", "Model 5"),
          caption = title,
          caption.above = T, inline.css = F, longtable = T)
})