library(ggplot2)
library(plyr)
library(grid)
library(gridExtra)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots")

p <- ggplot(cbsa_data_nochains, aes_string(x = "cbsa_nativity_pct_foreign_entered_before_90",
                                           y = "mexican_present", label = "cbsa_cbsaname")) +
  geom_point() + guides(size = F, color = F) +
  geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Foreign Born Entered US before 1990") +
  ylab("Percent Reviews Mention Mexican") + theme(text = element_text(family="serif"))

g <- arrangeGrob(p, sub = textGrob("Note: Data are scraped from Yelp.com.  Each dot represents a CBSA, and the red line is a locally weighted regression fit.",
                                   x = unit(0.02, "npc"), just = "left",
                                   gp = gpar(fontsize = 10, fontfamily="serif")),
                 nrow = 2, heights = c(20, 1))

ggsave("foreign_entered_before1990_nochains.png", g, dpi = 250)


p <- ggplot(cbsa_data_nochains, aes_string(x = "cbsa_nativity_pct_foreign_entered_before_2010",
                                           y = "mexican_present", label = "cbsa_cbsaname")) +
  geom_point() + guides(size = F, color = F) +
  geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Foreign Born Entered US before 2010") +
  ylab("Percent Reviews Mention Mexican") + theme(text = element_text(family="serif"))

g <- arrangeGrob(p, sub = textGrob("Note: Data are scraped from Yelp.com.  Each dot represents a CBSA, and the red line is a locally weighted regression fit.",
                                   x = unit(0.02, "npc"), just = "left",
                                   gp = gpar(fontsize = 10, fontfamily="serif")),
                 nrow = 2, heights = c(20, 1))

ggsave("foreign_entered_before2010_nochains.png", g, dpi = 250)



ggplot(cbsa_data_nochains, aes_string(x = "cbsa_nativity_pct_foreign_entered_after_1999",
                             y = "mexican_present", label = "cbsa_cbsaname")) +
  geom_point(size = 1) + guides(size = F, color = F) +
  geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Foreign Born Entered US after 1999") +
  ylab("Percent Reviews Mention Mexican")
ggsave("foreign_entered_after1999_nochains.png", dpi = 250)


ggplot(cbsa_data_nochains, aes_string(x = "cbsa_nativity_pct_foreign_hispanic", y = "mexican_present")) +
  geom_point(size = 1) + geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Residents are Foreign-Born Hispanics") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Percent Reviews Mentioning Mexican")
ggsave("foreign_hisp_nochains.png", dpi = 250)

ggplot(cbsa_data_nochains, aes_string(x = "cbsa_nativity_pct_foreign_hispanic", y = "mexican_present")) +
  geom_point(size = 1) + geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Residents are Foreign-Born Hispanics") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Percent Reviews Mentioning Mexican") + scale_x_log10()
ggsave("foreign_hisp_log_nochains.png", dpi = 250)

ggplot(cbsa_data_nochains, aes_string(x = "cbsa_nativity_pct_foreign_hispanic", y = "mexican_present",
                             label = "cbsa_cbsaname")) +
  geom_text(size = 1.8) + guides(size = F, color = F) +
  geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Mexican") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Percent Reviews Mentioning Mexican by Percent Mexican")
ggsave("foreign_hisp_text_nochains.png", dpi = 250)


# Percent of Hispanics that are foreign-born
ggplot(cbsa_data_nochains, aes_string(x = "cbsa_nativity_h_foreign_pct", y = "mexican_present")) +
  geom_point(size = 1) + geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent of Hispanics Foreign-Born") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Percent Reviews Mentioning Mexican")
ggsave("hisp_foreign_nochains.png", dpi = 250)

grep('foreign', names(cbsa_data_nochains), value = T)
