# Center continuous IVs around their means
# Divide by two standard deviations to make binary and continuous coefficients comparable
# var is a dataset column

standardize <- function(var) {
  var_mean <- mean(var, na.rm = T)
  var <- var - var_mean
  
  var_sd <- sd(var, na.rm = T)
  var <- var / (2 * var_sd)
}