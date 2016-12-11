rm(list = ls())
library(texreg)
library(plyr)

install.packages('acs')
library(acs)
setwd("/Users/annaboch/Dropbox/Yelp (1)/Data")
data <- read.csv("yelp_reviews_merged.csv")
save.image("analysis_models_AB.Rdata")

data$old_gateway <- 0
data$old_gateway[data$business_state %in% c("ca", "tx")] <- 1
data$old_gateway[data$business_city == "chicago"] <- 1

table(data$is_chain)
data <- subset(data, is_chain == 0)


acs1<- acs.fetch(2014,
                 span=5, 
                 geography=geo.make( msa="*"), 
                 table.number="S0501",  
                 key="2aff42c768f5e828524b7803ab1cbf42e50bbe2c", 
                 col.names="pretty")

acs1<- as.data.frame(acs_download)
acs_download@acs.colnames

##CBSA level analysis

cbsa_data <- ddply(data, .(cbsa_cbsaname), numcolwise(mean, na.rm = T))
cbsa_data$mexican_present = cbsa_data$mexican_present * 100

indep_vars <- c("dollars", "average_rating", "frequency_present", "authentic_present", "exotic_present")

# Standardize independent variables (subtract mean and divide by SD)
cbsa_data[, indep_vars] <- (cbsa_data[, indep_vars] - sapply(cbsa_data[, indep_vars], mean, na.rm = T)) /
  sapply(cbsa_data[, indep_vars], sd, na.rm = T)

model <- lm(mexican_present ~ ., data = cbsa_data[, c("mexican_present", indep_vars)])
summary(model)


names(cbsa_data)[!names(cbsa_data) %in% indep_vars]
indep_vars[!indep_vars %in% names(cbsa_data)]


zip_data <- ddply(data, .(zipcode), numcolwise(mean, na.rm = T))
zip_data$mexican_present = zip_data$mexican_present * 100
# Remove CBSA columns to avoid confustion
cbsa_cols <- grep('cbsa', names(zip_data), value=T)
non_cbsa_cols <- names(zip_data)[! names(zip_data) %in% cbsa_cols]
zip_data <- zip_data[, non_cbsa_cols]

zip_data$zip_white_educ_hs_orless <- zip_data$zip_white_educ_lt_hs + zip_data$zip_white_educ_hs
zip_data$zip_hispanic_educ_hs_orless <- zip_data$zip_hispanic_educ_lt_hs + zip_data$zip_hispanic_educ_hs

indep_vars <- c("dollars", "average_rating", "frequency_present", "authentic_present", "exotic_present",
                "zip_language_spanish", "zip_language_spanish_english_notwell", "zip_ethnicity_mexican_percent",
                "zip_white_educ_hs_orless", "zip_hispanic_educ_hs_orless")

# Standardize independent variables (subtract mean and divide by SD)
zip_data[, indep_vars] <- (zip_data[, indep_vars] - sapply(zip_data[, indep_vars], mean, na.rm = T)) /
  sapply(zip_data[, indep_vars], sd, na.rm = T)

model <- lm(mexican_present ~ ., data = zip_data[, c("mexican_present", indep_vars)])
summary(model)









filename <- "cbsa_models"
texreg(list(model_ip_simple, model_op_simple),
         center = F, file = filename, digits = 2,
         custom.model.names = c("In-Patient", "Out-Patient"),
         caption = paste0('Linear Reg. Predicting Residuals by Utilization'),
         caption.above = T, inline.css = F, longtable = T)
