
install.packages('stringi')
library(stringr)
library(stringi)


academic_data$strange_present <- grepl('strange', academic_data$text, ignore.case = T)

ac_small <- data[1:50,]

regex_list <- list('strange' = 'strange|weird|foreign',
                   'authentic' = 'authentic|traditional|real',
                   'ranking' = 'best|worst|average',
                   'frequency' = 'often|always|week|day|daily',
                   'authority' = 'expert|connoisseur')


for (i in seq_along(regex_list)) {
  var <- names(regex_list)[[i]]
  pattern <- regex_list[[i]]
  # add to the pattern to exclude 'not' right before word
  pattern <- paste0('(?<!not )(?<!no )', pattern)
  
  count_var <- paste0(var, '_count')
  present_var <- paste0(var, '_present')
  
  # count function
  ac_small[, count_var] <- sapply(ac_small$text, str_count, pattern = pattern)

  # present function
  ac_small[, present_var] <- grepl(pattern, ac_small$text, ignore.case = T, perl = T)
}

mean(ac_small$authentic_count)
mean(ac_small$frequency_count)

ac_small[,ac_small]