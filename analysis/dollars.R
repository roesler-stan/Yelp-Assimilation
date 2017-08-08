library(plyr)

table <- ddply(scraped_data_nochains, .(dollars), summarise,
      mexican_present = mean(mexican_present, na.rm=T) * 100,
      authentic_present = mean(authentic_present, na.rm=T) * 100,
      exotic_present = mean(exotic_present, na.rm=T) * 100,
      N = sum(!is.na(text)))
table = na.omit(table)

table

## BINARY, so don't do t-test


# At the business level - not sure this is meaningful
businesses <- ddply(scraped_data_nochains, .(business_id), summarise,
                    dollars = mean(dollars, na.rm=T),
                    mexican_present = mean(mexican_present, na.rm=T),
                    authentic_present = mean(authentic_present, na.rm=T),
                    N = sum(!is.na(text)))
businesses = na.omit(businesses)

tapply(businesses$mexican_present, businesses$dollars, function(x) mean(x, na.rm=T) * 100)
tapply(businesses$authentic_present, businesses$dollars, function(x) mean(x, na.rm=T) * 100)
