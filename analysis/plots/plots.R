library(ggplot2)
library(plyr)
library(grid)
library(gridExtra)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots")

p <- ggplot(cbsa_data_chains, aes_string(x = "cbsa_ethnicity_mexican_percent",
                                         y = "mexican_present")) +
  geom_point() + geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Residents Mexican") + ylab("Percent Reviews Mention Mexican") +
  theme(text = element_text(family="serif")) +
  ggtitle("Chains' Percent Reviews Mentioning Mexican") + scale_x_log10()

g <- arrangeGrob(p, sub = textGrob("Note: Data are scraped from Yelp.com.  Each dot represents a CBSA, and the red line is a locally weighted regression fit.",
                                   x = unit(0.02, "npc"), just = "left",
                                   gp = gpar(fontsize = 10, fontfamily="serif")),
                 nrow = 2, heights = c(20, 1))

ggsave("chains_mexican.png", g, dpi = 250)


p <- ggplot(cbsa_data_nochains, aes_string(x = "cbsa_ethnicity_mexican_percent",
                                           y = "mexican_present")) +
  geom_point() + geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Residents Mexican") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Non-Chains' Percent Reviews Mentioning Mexican") + scale_x_log10() +
  theme(text = element_text(family="serif"))

g <- arrangeGrob(p, sub = textGrob("Note: Data are scraped from Yelp.com.  Each dot represents a CBSA, and the red line is a locally weighted regression fit.",
                                   x = unit(0.02, "npc"), just = "left",
                                   gp = gpar(fontsize = 10, fontfamily="serif")),
                 nrow = 2, heights = c(20, 1))
ggsave("nochains_mexican.png", g, dpi=250)


p <- ggplot(cbsa_data_nochains, aes_string(x = "cbsa_origin_mexican_pct_log",
                                           y = "mexican_present")) +
  geom_point() + geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent with Mexican Origin (Log)") + ylab("Percent Reviews Mention Mexican") +
  ggtitle("Non-Chains' Percent Reviews Mentioning Mexican") +
  theme(text = element_text(family="serif"), plot.title=element_text(hjust=0.5))

g <- arrangeGrob(p, sub = textGrob("Note: Data are scraped from Yelp.com.  Each dot represents a CBSA, and the red line is a locally weighted regression fit.",
                                   x = unit(0.02, "npc"), just = "left",
                                   gp = gpar(fontsize = 10, fontfamily="serif")),
                 nrow = 2, heights = c(20, 1))
ggsave("nochains_origin_mex.png", g, dpi=250)


p <- ggplot(cbsa_data_nochains, aes_string(x = "cps_mex_interracial_pct",
                                           y = "mexican_present")) +
  geom_point() + geom_smooth(method = "loess", color = "red", se = F, size = 0.4) +
  theme_bw() + xlab("Percent Couples Interracial (not Mex-Mex)") + ylab("Percent Reviews Mention 'Mexican'") +
  ggtitle("Non-Chains' Percent Reviews Mentioning 'Mexican'") +
  theme(text = element_text(family="serif"), plot.title=element_text(hjust=0.5))

g <- arrangeGrob(p, sub = textGrob("Note: Data are scraped from Yelp.com.  Each dot represents a CBSA, and the red line is a locally weighted regression fit.",
                                   x = unit(0.02, "npc"), just = "left",
                                   gp = gpar(fontsize = 10, fontfamily="serif")),
                 nrow = 2, heights = c(20, 1))
ggsave("nochains_mexican_interracial.png", g, dpi=250)

cor.test(cbsa_data_nochains$cps_mex_interracial_pct, cbsa_data_nochains$cbsa_language_spanish_english_notwell,  method = "pearson", use="pairwise.complete.obs") 
cor.test(cbsa_data_nochains$cps_mex_interracial_pct, cbsa_data_nochains$cbsa_origin_mexican_pct_log,  method = "pearson", use="pairwise.complete.obs") 


p

cbsa_data_chains$cbsa_language_spanish_english_notwell <- as.numeric(cbsa_data_chains$cbsa_language_spanish_english_notwell)
p <- ggplot(cbsa_data_chains, aes_string(x = "cbsa_language_spanish_english_notwell",
                                         y = "mexican_present")) +
  geom_point() +
  theme_bw() + xlab("Percent Speak only Spanish") + ylab("Percent Reviews Mention Mexican") +
  theme(text = element_text(family="serif")) +
  ggtitle("Chains' Percent Reviews Mentioning Mexican") + scale_x_log10()

g <- arrangeGrob(p, sub = textGrob("Note: Data are scraped from Yelp.com.  Each dot represents a CBSA.",
                                   x = unit(0.02, "npc"), just = "left",
                                   gp = gpar(fontsize = 10, fontfamily="serif")),
                 nrow = 2, heights = c(20, 1))

ggsave("chains_spanish_only.png", g, dpi = 250)


cbsa_data_nochains$cbsa_language_spanish_english_notwell <- as.numeric(cbsa_data_nochains$cbsa_language_spanish_english_notwell)
p <- ggplot(cbsa_data_nochains, aes_string(x = "cbsa_language_spanish_english_notwell",
                                         y = "mexican_present")) +
  geom_point() +
  theme_bw() + xlab("Percent Speak only Spanish") + ylab("Percent Reviews Mention Mexican") +
  theme(text = element_text(family="serif")) +
  ggtitle("Chains' Percent Reviews Mentioning Mexican") + scale_x_log10()

g <- arrangeGrob(p, sub = textGrob("Note: Data are scraped from Yelp.com.  Each dot represents a CBSA.",
                                   x = unit(0.02, "npc"), just = "left",
                                   gp = gpar(fontsize = 10, fontfamily="serif")),
                 nrow = 2, heights = c(20, 1))

ggsave("nochains_spanish_only.png", g, dpi = 250)