# These are important variables.  If any row is missing on any of theses, remove that row.
varlist <- c("race", "age", "year", "region", "degree")
missing_values <- c("iap", "na", "dk", "refused", "not assigned", "no answer", "not applicable")

for (var in varlist) {
  # relabel common missing values (DK, NA, IAP, refused) as NA
  dataset[,var][dataset[,var] %in% missing_values] <- NA
  
  # remove rows with missing values for any of the variables
  dataset <- subset(dataset, !is.na(dataset[,var]))
  
  # drop empty levels from factor variables
  if(class(dataset[,var]) == "factor") {
    dataset[var] <- droplevels(dataset[var])
  }
}
