library(texreg)
library(plyr)
library(stats)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output")

cor(cbsa_data_nochains$cbsa_ethnicity_mexican_percent, cbsa_data_nochains$cbsa_hisp_div_white_lt_hs,
    method = "pearson", use="pairwise.complete.obs")

cor.test(cbsa_data_nochains$cbsa_ethnicity_mexican_percent, cbsa_data_nochains$cbsa_hisp_div_white_lt_hs,
         method = "pearson", use="pairwise.complete.obs")


subsets <- list("nochains.doc" = cbsa_data_nochains, "chains.doc" = cbsa_data_chains)

nothing <- lapply(seq_along(subsets), function(i) {
  model_data <- subsets[[i]]
  outfile <- names(subsets)[[i]]
  
  model_data$cbsa_ethnicity_mexican_percent_log <- log(model_data$cbsa_ethnicity_mexican_percent + 0.0001)
  model_data$cbsa_language_spanish_english_notwell_log <- log(model_data$cbsa_language_spanish_english_notwell + 0.0001)
  
  model_data$mexican_present <- (model_data$mexican_present - mean(model_data$mexican_present, na.rm = T)) / sd(model_data$mexican_present, na.rm = T)
  model_data$authentic_present <- (model_data$authentic_present - mean(model_data$authentic_present, na.rm = T)) / sd(model_data$authentic_present, na.rm = T)
  model_data_std <- model_data
  model_data_std$cbsa_ethnicity_mexican_percent_log <- (model_data_std$cbsa_ethnicity_mexican_percent_log - mean(model_data_std$cbsa_ethnicity_mexican_percent_log, na.rm = T)) / sd(model_data_std$cbsa_ethnicity_mexican_percent_log, na.rm = T)
  
  vars <- "mexican_present + authentic_present"
  
  model1 <- lm(paste("cbsa_summary_dissim_idx_hisp_2010 ~", vars), data = model_data)
  model2 <- lm(paste("cbsa_ethnicity_mexican_percent_log ~", vars), data = model_data)
  model3 <- lm(paste("cbsa_language_spanish_english_notwell_log ~", vars), data = model_data)
  model4 <- lm(paste("cbsa_hisp_div_white_lt_hs ~ ", vars), data = model_data)
  model5 <- lm(paste("cbsa_hisp_div_white_lt_hs ~ cbsa_language_spanish_english_notwell_log +", vars), data = model_data_std)
  
  htmlreg(list(model1, model2, model3, model4, model5),
          center = F, file = outfile, digits = 2,
          custom.model.names = c("Dissimilarity", "Percent Mexican (Log)", "Poor English (Log)",
                                 "Hispanic / White < HS", "Hispanic / White < HS"),
          caption = paste0('Linear Regression'),
          caption.above = T, inline.css = F, longtable = T)
  NULL
})


chipotle <- subset(scraped_data, business_name == "chipotle mexican grill")
model_data <- ddply(chipotle, .(cbsa_cbsaname), numcolwise(mean, na.rm = T))

model_data$mexican_present <- (model_data$mexican_present - mean(model_data$mexican_present, na.rm = T)) / sd(model_data$mexican_present, na.rm = T)
model_data$authentic_present <- (model_data$authentic_present - mean(model_data$authentic_present, na.rm = T)) / sd(model_data$authentic_present, na.rm = T)

model1 <- lm(cbsa_summary_dissim_idx_hisp_2010 ~ authentic_present, data = model_data)
model2 <- lm(cbsa_ethnicity_mexican_percent ~ authentic_present, data = model_data)
model3 <- lm(cbsa_language_spanish_english_notwell ~ authentic_present, data = model_data)

htmlreg(list(model1, model2, model3),
        center = F, file = "chains_authentic.doc", digits = 2,
        custom.model.names = c("Dissimilarity", "Percent Mexican", "Poor English"),
        caption = paste0('Linear Regression'),
        caption.above = T, inline.css = F, longtable = T)
