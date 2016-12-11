## Plot term percentages by % Mexican residents

library(tm)
library(ggplot2)
library(ggrepel)
library(scales)
library(grid)
library(gridExtra)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots")

cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log <- log(cbsa_data_nochains$cbsa_ethnicity_mexican_percent + 0.0001)
mean(cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log, na.rm = T)
sd(cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log, na.rm = T)
quantile(cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log, c(0.25, 0.5, 0.75))

cbsa_data_nochains$many_mexicans[cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log < 0.7886] <- 0
cbsa_data_nochains$many_mexicans[cbsa_data_nochains$cbsa_ethnicity_mexican_percent_log > 3.2367] <- 1

cbsa_data_nochains$Italian_pct <- (cbsa_data_nochains$Italian / sum(cbsa_data_nochains$Italian, na.rm = T)) * 100
cbsa_data_nochains$Mexican_pct <- (cbsa_data_nochains$Mexican / sum(cbsa_data_nochains$Mexican, na.rm = T)) * 100
cbsa_data_nochains$American_pct <- (cbsa_data_nochains$American / sum(cbsa_data_nochains$American, na.rm = T)) * 100

# Calculate ratio of low Mexican to high Mexican term percentage
cbsa_data_nochains$MexIt_pct_ratio <- cbsa_data_nochains$Mexican_pct / cbsa_data_nochains$Italian_pct
cbsa_data_nochains$MexIt_pct_ratio[cbsa_data_nochains$Mexican_pct < cbsa_data_nochains$Italian_pct] <-
  (-1 / cbsa_data_nochains$MexIt_pct_ratio[cbsa_data_nochains$Mexican_pct < cbsa_data_nochains$Italian_pct])

cbsa_data_nochains$rare_term <- 0
cbsa_data_nochains$rare_term[cbsa_data_nochains$Mexican < 5 | cbsa_data_nochains$Italian < 5] <- 1
table(cbsa_data_nochains$rare_term)
cbsa_data_nochains <- subset(cbsa_data_nochains, rare_term == 0)

# Create measure for terms that are distinctly Italian or Mexican
cbsa_data_nochains$big_ItMex_pct <- 0
cbsa_data_nochains$big_ItMex_pct[abs(cbsa_data_nochains$MexIt_pct_ratio) > 25] <- 1
table(cbsa_data_nochains$big_ItMex_pct)

ggplot(cbsa_data_nochains, aes(MexIt_pct_ratio)) + geom_histogram(bins = 300)

# Scatter plot with a log scale b/c a few words are very frequent
p <- ggplot(cbsa_data_nochains, aes(x = Italian_pct, y = Mexican_pct)) +
  geom_point(aes(color = factor(big_ItMex_pct))) +
  scale_color_manual(values = c("grey", "red")) + guides(color = F) +
  theme_bw(base_size = 16) + ggtitle("Adjective Frequency by Cuisine") +
  xlab("Italian Term Percentage") + ylab("Mexican Term Percentage") +
  coord_fixed() + geom_abline(intercept = 0, slope = 1, linetype = "dashed") +
  geom_text_repel(data = subset(cbsa_data_nochains, big_ItMex_pct == 1), aes(label = term), size = 4,
                  box.padding = unit(0.01, "lines"), point.padding = unit(0.01, "lines")) +
  scale_y_log10() + scale_x_log10() # log scales include 0

grid.newpage()
footnote <- "Note: Only terms occurring at least 5 times in both cuisines are included."
g <- arrangeGrob(p, bottom = textGrob(footnote, x = 0, hjust = -0.05, vjust=0.1, gp = gpar(fontface = "italic", fontsize = 10)))

ggsave('it_mex_adj.png', g, dpi = 300, width = 12, height = 10)
