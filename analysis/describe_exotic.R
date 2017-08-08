library(Hmisc)

rcorr(cbsa_data_nochains$exotic_present, cbsa_data_nochains$mexican_present, type="pearson")

rcorr(cbsa_data_nochains$exotic_count, cbsa_data_nochains$mexican_count, type="pearson")


rcorr(scraped_data$exotic_present, scraped_data$mexican_present, type="pearson")

rcorr(scraped_data$exotic_count, scraped_data$mexican_count, type="pearson")


## Given mentioning exotic, do they mention Mexican?
tapply(scraped_data$mexican_present, scraped_data$exotic_present, function(x) mean(x, na.rm=T) * 100)

