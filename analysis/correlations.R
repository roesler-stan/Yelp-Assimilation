## Plot correlations and distributions of county utilization and health rankings data

library(Hmisc)
library(corrplot)
library(plyr)
library(reshape2)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots/scraped")
source("/Users/katharina/Dropbox/Projects/Yelp/Code/analysis/scraped/cor_mtest.R")

vars <- c("cbsa_ethnicity_mexican_percent", "cbsa_summary_dissim_idx_hisp_2010",
          "cbsa_percent_foreign_born", "cbsa_language_spanish",
          "cbsa_language_spanish_english_notwell",
          "dollars", "average_rating")

cor_subset <- cbsa_data[, vars]
M <- cor(cor_subset, use = "pairwise.complete.obs")
cor_data <- data.frame(M)
# Find p-values
res1 <- cor.mtest(cor_subset, 0.95)

png('corr.png')
# Only show correlations that are sig. at 0.05 level
corrplot(M, type = "lower", diag = F, p.mat = res1[[1]], insig = "blank")
#          , method = 'square', type = "lower", na.label = " ", tl.offset = 0.6,
#          tl.srt = 60, tl.cex = 2.5, cl.cex = 2, p.mat = res1[[1]], insig = "blank")
title(main = "CBSA-Level Correlations")
dev.off()

