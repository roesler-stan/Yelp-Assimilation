library(tm)
library(reshape)
library(jpeg)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots")

weightedTermDocMatrix <- weightTfIdf(termDocMatrix)
weighted_terms <- data.frame(inspect(weightedTermDocMatrix))
weighted_terms$term <- row.names(weighted_terms)
row.names(weighted_terms) <- NULL


weighted_terms_wide <- melt(weighted_terms, id.vars = "term", variable_name = "category")


weighted_american <- subset(weighted_terms_wide, category == "American")
weighted_american <- weighted_american[order(-weighted_american$value), ]
weighted_american <- weighted_american[1:20,]
row.names(weighted_american) <- NULL
weighted_american$rank <- row.names(weighted_american)
weighted_american$rank <- as.numeric(weighted_american$rank)

weighted_italian <- subset(weighted_terms_wide, category == "Italian")
weighted_italian <- weighted_italian[order(-weighted_italian$value), ]
weighted_italian <- weighted_italian[1:20,]
row.names(weighted_italian) <- NULL
weighted_italian$rank <- row.names(weighted_italian)
weighted_italian$rank <- as.numeric(weighted_italian$rank)

weighted_mexican <- subset(weighted_terms_wide, category == "Mexican")
weighted_mexican <- weighted_mexican[order(-weighted_mexican$value), ]
weighted_mexican <- weighted_mexican[1:20,]
row.names(weighted_mexican) <- NULL
weighted_mexican$rank <- row.names(weighted_mexican)
weighted_mexican$rank <- as.numeric(weighted_mexican$rank)

plot_data <- rbind(weighted_american, weighted_italian, weighted_mexican)


amer <- readJPEG("../images/american.jpg"); american <- rasterGrob(amer, interpolate=TRUE)
it <- readJPEG("../images/italian.jpg"); italian <- rasterGrob(it, interpolate=TRUE)
mex <- readJPEG("../images/mexican.jpg"); mexican <- rasterGrob(mex, interpolate=TRUE)

ggplot(plot_data, aes(category, ((rank * -1) - 3.5))) + 
  geom_point(color = "white") + 
  geom_label(aes(label = plot_data$term, fill = plot_data$category),
             color = 'white', fontface = 'bold', size = 2) +
  scale_fill_manual(values = c("#C20631", "#673e1e", "#21B726")) + theme_classic() +
  theme(legend.position = 1, plot.title = element_text(size = 16)) + 
#   axis.title.y = element_text(margin = margin(0,10,0,0))
  labs(title = "Most Characteristic Words") + 
  xlab("") + ylab("Ranking") +
  scale_y_continuous(limits = c(-24,-1), breaks = c(-23.5, -13.5, -4.5),
                     labels = c("#20", "#10", "#1")) +
  annotation_custom(american, xmin=.75, xmax=1.25, ymin=0, ymax=-4) + 
  annotation_custom(italian, xmin=1.75, xmax=2.25, ymin=0, ymax=-4) + 
  annotation_custom(mexican, xmin=2.75, xmax=3.25, ymin=0, ymax=-4)

ggsave("tfidf_bycat.png", dpi = 300)
