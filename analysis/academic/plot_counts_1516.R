library(plyr)
library(reshape2)
library(ggplot2)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots")
source("/Users/katharina/Dropbox/Projects/Yelp/Code/analysis/helper/make_title.R")

# Remove restaurants in other categories
categories <- c("Mexican", "Italian", "American")
plot_data <- subset(academic_data, category %in% categories)
plot_data <- subset(plot_data, year %in% c(2015, 2016))

# Clean data, make numeric
present_vars <- grep('_present', names(plot_data), value = T)
for (var in present_vars) {
  plot_data[[var]] <- as.numeric(plot_data[[var]])
}

cat_means <- ddply(plot_data, .(category), numcolwise(mean, na.rm = T))
write.csv(cat_means, "cat_means_1516.csv", row.names = F)


present_vars <- present_vars[! present_vars %in% c("italian_present", "mexican_present", "american_present")]
present_data <- melt(cat_means, id.vars = 'category', measure.vars = present_vars)
present_data$variable <- sapply(present_data$variable, make_title)
present_data$variable <- sapply(present_data$variable, function(x) gsub(' Present', '', x))


ggplot(present_data, aes(x = reorder(variable, value), y = value * 100, fill = category)) +
  geom_bar(position = "dodge", stat = "identity") +
  ggtitle("Percentage of Reviews with each Theme, 2015-16") +
  xlab("Theme") + ylab("Percentage of Reviews") +
  scale_fill_brewer(palette = "Accent", name = "Category") +
  theme_bw() + theme(axis.text.x = element_text(angle = 60, vjust = 0.5)) + ylim(0, 50)

ggsave("present_1516.png", dpi = 300, width = 12, height = 10)
