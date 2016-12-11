rm(list = ls())

library(jpeg)
library(grid)
library(ggplot2)
library(gtools)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Code/R")
source("helper/make_title.R")
options(scipen = 999)
setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots/")

# In python, transform words to lower case and only keep adjectives (use nltk)
data <- read.csv("/Users/katharina/Dropbox/Projects/Yelp/Data/academic/adjectives_tfidf.csv")

# Get rank from tfidf (which is actually already sorted)
plot_data <- NULL
for (c in unique(data$cat_state)) {
  d <- subset(data, cat_state == c)
  d <- d[order(-d$tfidf), ]
  d <- d[1:20,]
  row.names(d) <- NULL
  d$rank <- row.names(d)
  d$rank <- as.numeric(d$rank)
  plot_data <- rbind(plot_data, d)
}


# Plot with category flag on top and each state within each category
amer <- readJPEG("../images/american.jpg"); american <- rasterGrob(amer, interpolate=TRUE)
it <- readJPEG("../images/italian.jpg"); italian <- rasterGrob(it, interpolate=TRUE)
mex <- readJPEG("../images/mexican.jpg"); mexican <- rasterGrob(mex, interpolate=TRUE)

ggplot(plot_data, aes(cat_state, ((rank * -1) - 3.5))) +
  geom_label(aes(label = term, fill = cat_state), color = 'white', fontface = 'bold', size = 2) +
  scale_fill_manual(values = c("#C20631", "#673e1e", "#C20631", "#673e1e", "#C20631", "#673e1e")) +
  theme(plot.title = element_text(size = 16)) + theme_classic() + guides(fill = F) +
  labs(title = "Most Characteristic Words") + xlab("") + ylab("TF-IDF Ranking") +
  scale_y_continuous(limits = c(-24, -1), breaks = c(-23.5, -13.5, -4.5),
                     labels = c("#20", "#10", "#1")) +
  annotation_custom(american, xmin=0.75, xmax=2.25, ymin=0, ymax=-3) +
  annotation_custom(italian, xmin=2.75, xmax=4.25, ymin=0, ymax=-3) + 
  annotation_custom(mexican, xmin=4.75, xmax=6.25, ymin=0, ymax=-3) +
  scale_x_discrete(labels = c("AZ", "WI", "AZ", "WI", "AZ", "WI"))

ggsave("tfidf_adjectives_bycat.png", dpi = 300)



# Plot with states on top and categories (e.g. Mexican) within each state
wi <- readJPEG("../images/wisconsin.jpg"); wisconsin <- rasterGrob(wi, interpolate=TRUE)
az <- readJPEG("../images/arizona.jpg"); arizona <- rasterGrob(az, interpolate=TRUE)

# Make an empty category for spacing
empty_row <- data.frame(list("cat_state" = "", "rank" = 20, "term" = ""))
plot_data <- smartbind(plot_data, empty_row)

plot_data$cat_state <- factor(plot_data$cat_state,
                              levels = c("American in AZ", "Italian in AZ", "Mexican in AZ", "",
                                         "American in WI", "Italian in WI", "Mexican in WI" ))

ggplot(plot_data, aes(cat_state, ((rank * -1) - 3.5))) +
  geom_label(aes(label = term, fill = cat_state), color = 'white', fontface = 'bold', size = 2) +
  scale_fill_manual(values = c("#377eb8", "#4daf4a", "#984ea3", "white", "#377eb8", "#4daf4a", "#984ea3")) +
  theme_classic() + guides(fill = F) +
  labs(title = "Most Characteristic Words") + xlab("") + ylab("TF-IDF Ranking") +
  scale_y_continuous(limits = c(-24, -1), breaks = c(-23.5, -13.5, -4.5),
                     labels = c("#20", "#10", "#1")) +
  annotation_custom(wisconsin, xmin=0.25, xmax=3.5, ymin=0, ymax=-3) +
  annotation_custom(arizona, xmin=4.5, xmax=7.5, ymin=0, ymax=-3) +
  scale_x_discrete(labels = c("American", "Italian", "Mexican", "", "American", "Italian", "Mexican")) +
  theme(plot.title = element_text(size = 16))

ggsave("tfidf_adjectives_bystate.png", dpi = 300)
