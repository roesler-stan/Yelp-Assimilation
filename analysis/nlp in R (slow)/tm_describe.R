library(tm)
library(ggplot2)
library(ggrepel)
library(scales)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output")

term_data$Italian_pct <- (term_data$Italian / sum(term_data$Italian, na.rm = T)) * 100
term_data$Mexican_pct <- (term_data$Mexican / sum(term_data$Mexican, na.rm = T)) * 100
term_data$American_pct <- (term_data$American / sum(term_data$American, na.rm = T)) * 100

# Calculate ratio of Mexican to Italian term percentage
# Only include terms present at least ten times in each type
term_data$MexIt_pct_ratio <- term_data$Mexican_pct / term_data$Italian_pct
term_data$MexIt_pct_ratio[term_data$Mexican_pct < term_data$Italian_pct] <-
  (-1 / term_data$MexIt_pct_ratio[term_data$Mexican_pct < term_data$Italian_pct])
term_data$MexIt_pct_ratio[term_data$Mexican < 10] <- NA
term_data$MexIt_pct_ratio[term_data$Italian < 10] <- NA

# Create measure for terms that are distinctly Italian or Mexican
term_data$big_ItMex_pct <- 0
term_data$big_ItMex_pct[abs(term_data$MexIt_pct_ratio) > 60] <- 1

# Bar plot with ratio of Mexican-Italian term percentages
ggplot(subset(term_data, big_ItMex_pct == 1),
       aes(x = reorder(term, MexIt_pct_ratio), y = MexIt_pct_ratio,
           fill = MexIt_pct_ratio)) + 
  geom_bar(stat = "identity") + theme_bw() +
  ggtitle("Most Distinctive Terms") + xlab("Term") +
  ylab("Mexican to Italian Ratio") +
  theme(axis.text.x = element_text(angle = 65, vjust = 0.5)) +
  scale_fill_distiller(palette = "OrRd", direction = 1) + guides(fill = F)

ggsave('mex_it_terms_ratio.png', dpi = 300, width = 12, height = 10)

# Scatter plot with a log scale b/c a few words are very frequent
ggplot(term_data, aes(x = Italian_pct, y = Mexican_pct)) +
  geom_point(aes(color = factor(big_ItMex_pct))) +
  scale_color_manual(values = c("grey", "red")) + guides(color = F) +
  theme_bw(base_size = 16) + ggtitle("Term Frequency by Cuisine") +
  xlab("Italian Term Percentage") + ylab("Mexican Term Percentage") +
  coord_fixed() + geom_abline(intercept = 0, slope = 1, linetype = "dashed") +
  geom_text_repel(data = subset(term_data, big_ItMex_pct == 1),
                  aes(label = term), size = 5,
        box.padding = unit(0.05, "lines"), point.padding = unit(0.05, "lines")) +
  scale_y_log10() + scale_x_log10()

ggsave('it_mex_terms_log10.png', dpi = 300, width = 12, height = 10)


# Remove food words / focus on particular types of words
# Such as adjectives or pre-defined lists
# E.g. generate list of words using themes regex
# Like what is commonly used / indicative of "frequency"


# And check tm indicitiveness


# Find frequent terms - at least 10 occurences
findFreqTerms(termDocMatrix, 10)

## Find words often appearing with "Mexican"
findAssocs(termDocMatrix, "mexican", 0.9)
findAssocs(termDocMatrix, "italian", 0.9)
findAssocs(termDocMatrix, "american", 0.9)


## Add meta data, such as recency of immigration
