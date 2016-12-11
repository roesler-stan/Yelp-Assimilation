## Return a data frame with the % of each feature missing

missing_rates <- function(data) {
  return (data.frame(sapply(data, function(x) sum(is.na(x)) / length(x))))
}
