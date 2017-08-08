# install.packages("devtools")
# library(devtools)
# install.packages("Hmisc")
# install_github('arilamstein/choroplethrZip@v1.5.0')

library(choroplethrZip)
library(ggplot2)
library(plyr)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/maps")
data(df_zip_demographics)

zip_data <- ddply(scraped_data, .(zipcode), summarise,
                  residents_mexican = mean(zip_ethnicity_mexican_percent, na.rm=T),
                  mexican_mentioned = mean(mexican_present, na.rm=T))
zip_data <- rename(zip_data, replace=c("zipcode"="region"))
zip_data$region <- as.character(zip_data$region)

leading_zeros <- function(z) {
  leading <- paste(rep("0", 5 - nchar(z)), sep="", collapse="")
  return(paste0(leading, z))
}
zip_data$region <- sapply(zip_data$region, leading_zeros)
zip_data <- na.omit(zip_data)

cols <- c("residents_mexican")
cols <- c("residents_mexican", "mexican_mentioned")
for (col in cols) {
  # set the value and title
  zip_data$value = zip_data[, col]
  title = paste0("Zip Codes:\n", col)
  
  # print the map
  choro = zip_choropleth(zip_data, title=title)
  print(choro)
}