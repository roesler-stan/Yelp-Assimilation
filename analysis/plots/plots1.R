library(ggplot2)
library(plyr)
library(grid)
library(gridExtra)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots")

# ggplot(cbsa_data, aes(x = cbsa_dissim_idx_hisp_2010)) + geom_histogram(aes(y = ..density..), bins = 100)

ggplot(cbsa_data, aes_string(x = "cbsa_ethnicity_mexican_percent", y = "mexican_present")) +
  geom_point(size = 1) +
  #geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Residents Mexican") + ylab("Percent Reviews Mention Mexican") +
  theme(text = element_text(family="serif")) +
  ggtitle("Percent Reviews Mentioning Mexican")
ggsave("mexican.png", dpi = 250)


ggplot(cbsa_data, aes_string(x = "cbsa_ethnicity_mexican_percent", y = "mexican_present",
                             label = "cbsa_cbsaname")) +
  geom_text(size = 1.8) + guides(size = F, color = F) +
  geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Mexican") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Percent Reviews Mentioning Mexican by Percent Mexican")
ggsave("mexican_text.png", dpi = 250)


ggplot(cbsa_data, aes_string(x = "cbsa_ethnicity_mexican_percent", y = "mexican_present")) +
  geom_point() +
  #geom_smooth(method = "lm", color = "red", se = T) +
  theme_bw() + xlab("Percent Mexican") +
  ylab("Percent Reviews Mention Mexican") +
  ggtitle("Percent Reviews Mentioning Mexican by Percent Mexican") +
  scale_x_log10()
ggsave("mexican_log.png", dpi = 250)


ggplot(cbsa_data, aes_string(x = "cbsa_ethnicity_mexican_percent", y = "mexican_present",
                             label = "top_business")) +
  geom_text(size = 1.8, aes(color = factor(top_is_chain))) + guides(size = F) +
  geom_smooth(method = "loess", color = "red", se = F, size = 0.3) +
  theme_bw() + xlab("Percent Mexican (Log)") +
  ylab("Percent Reviews Mention Mexican") +
  ggtitle("CBSAs' Most Reviewed Restaurants") + scale_x_log10() +
  scale_color_brewer("Is Chain", palette = "Set1", labels = c("No", "Yes"), direction = -1)
ggsave("mexican_log_topbusiness.png", dpi = 250)


ggplot(cbsa_data, aes_string(x = "cbsa_percent_foreign_born", y = "mexican_present",
                             label = "cbsa_cbsaname")) +
  geom_point(size = 0.8) + geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Foreign Born") + ylab("Percent Reviews Mention Mexican")
ggsave("foreign.png", dpi = 250)

# Check that this matches the plot above - it roughly does
ggplot(cbsa_data, aes_string(x = "cbsa_nativity_pct_foreign_entered", y = "mexican_present",
                             label = "cbsa_cbsaname")) +
  geom_point(size = 0.8) + guides(size = F, color = F) +
  geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Foreign Born Entered US") + ylab("Percent Reviews Mention Mexican")
ggsave("foreign_entered.png", dpi = 250)


ggplot(cbsa_data, aes_string(x = "cbsa_nativity_pct_foreign_entered_after_1999",
                             y = "mexican_present", label = "cbsa_cbsaname")) +
  geom_point(size = 1) + guides(size = F, color = F) +
  geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Foreign Born Entered US after 1999") +
  ylab("Percent Reviews Mention Mexican")
ggsave("foreign_entered_after1999.png", dpi = 250)


ggplot(cbsa_data, aes_string(x = "cbsa_language_spanish_english_notwell",
                             y = "mexican_present")) +
  geom_point(size = 0.8) + geom_smooth(method = "lm", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent who Speak Only Spanish") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Percent Reviews Mentioning Mexican")
ggsave("spanish_only.png", dpi = 250)


ggplot(subset(cbsa_data, cbsa_language_spanish_english_notwell > 1),
       aes_string(x = "cbsa_language_spanish_english_notwell",
                             y = "mexican_present")) +
  geom_point(size = 0.8) + geom_smooth(method = "lm", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent who Speak Only Spanish") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Percent Reviews Mentioning Mexican")


ggplot(cbsa_data, aes_string(x = "cbsa_language_spanish_english_notwell",
                             y = "mexican_present")) +
  geom_point() +
  #geom_smooth(method = "lm", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent who Speak Only Spanish") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Percent Reviews Mentioning Mexican") + scale_x_log10()
ggsave("spanish_only_log.png", dpi = 250)


ggplot(cbsa_data_nochains, aes_string(x = "cbsa_language_spanish_english_notwell",
                             y = "mexican_present")) +
  geom_point() +
  theme_bw() + xlab("Percent who Speak Only Spanish") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Non-Chains' Percent Reviews Mentioning Mexican") + scale_x_log10()
ggsave("spanish_only_nonchains_log.png", dpi = 250)


ggplot(cbsa_data, aes_string(x = "cbsa_summary_dissim_idx_hisp_2010",
                             y = "mexican_present")) +
  geom_point(size = 0.8) + guides(size = F, color = F) +
  geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Dissimilarity Index") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Percent Reviews Mentioning Mexican")
ggsave("dissimilarity.png", dpi = 250)


ggplot(cbsa_data, aes_string(x = "cbsa_hisp_div_white_lt_hs", y = "mexican_present")) +
  geom_point(size = 0.8) + guides(size = F, color = F) +
  geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("% Hispanic / % White Less than High School") +
  ylab("Percent Reviews Mention Mexican") + ggtitle("Percent Reviews Mentioning Mexican")
ggsave("educ.png", dpi = 250)
