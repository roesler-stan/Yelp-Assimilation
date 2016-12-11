# Rename column string to look nice
make_title <- function(col) {
  col <- gsub("_", " ", col)
  s <- strsplit(col, " ")[[1]]
  col <- paste(toupper(substring(s, 1, 1)), tolower(substring(s, 2)), sep = "", collapse = " ")
  return(col)  
}