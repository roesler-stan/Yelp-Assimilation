# Histograms
library(ggplot2)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots/scraped")

vars <- c("cbsa_ethnicity_mexican_percent", "cbsa_summary_dissim_idx_hisp_2010",
                 "cbsa_percent_foreign_born", "cbsa_language_spanish",
                 "cbsa_language_spanish_english_notwell", "cbsa_hisp_div_white_lt_hs",
                 "dollars", "average_rating")

for (var in vars) {
  ggplot(cbsa_data, aes_string(x = var)) +
    geom_histogram(stat = "bin", bins = 20) +
    theme_bw()
  filename <- paste0("hist_", var, ".png")
  ggsave(filename, width = 12, height = 10)
}


vars <- c("mexican_present", "authentic_present")
for (var in vars) {
  ggplot(cbsa_data, aes_string(x = var)) +
    geom_histogram(stat = "bin", bins = 100) +
    theme_bw()
  filename <- paste0("hist_", var, ".png")
  ggsave(filename, width = 12, height = 10)
}

cor(cbsa_data$mexican_present, cbsa_data$authentic_present, method = "pearson")
