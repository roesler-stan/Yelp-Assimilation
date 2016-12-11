# Standardize continuous meausures to be between 0 and 1
# Var is a dataset column

min_max <- function(var) {
  return ((var - min(var, na.rm = T)) / (max(var, na.rm = T) - min(var, na.rm = T)))
}