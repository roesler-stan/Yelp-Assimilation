library(plyr)
library(reshape2)
library(ggplot2)
library(grid)
library(gridExtra)
library(RColorBrewer)

setwd("/Users/katharina/Dropbox/Projects/Yelp/Code/analysis/academic")
source("grid_arrange_legend.R")
setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots")
source("/Users/katharina/Dropbox/Projects/Yelp/Code/analysis/helper/make_title.R")

# Remove restaurants in other categories
categories <- c("Mexican", "Italian", "American")
academic_data <- subset(academic_data, category %in% categories)

# Clean data, make numeric
present_vars <- grep('_present', names(academic_data), value = T)
for (var in present_vars) {
  academic_data[[var]] <- as.numeric(academic_data[[var]])
}

cat_means <- ddply(academic_data, .(category), numcolwise(mean, na.rm = T))
cat_std <- ddply(academic_data, .(category), numcolwise(sd, na.rm = T))
cat_N <- ddply(academic_data, .(category), numcolwise(function(x) sum(!is.na(x))))
# Reviews per restaurant type
cat_N[, c("category", "mexican_present", "authentic_present")]

present_vars <- present_vars[! present_vars %in% c("italian_present", "mexican_present", "american_present")]
present_means <- melt(cat_means, id.vars = 'category', measure.vars = present_vars, value.name="mean")
present_std <- melt(cat_std, id.vars = 'category', measure.vars = present_vars, value.name="std")
present_N <- melt(cat_N, id.vars = 'category', measure.vars = present_vars, value.name="N")

present_data <- merge(present_means, present_std, by = c('category', "variable"))
present_data <- merge(present_data, present_N, by = c('category', "variable"))
present_data$mean <- present_data$mean * 100
present_data$std <- present_data$std * 100
# SE = SD / sqrt(N)
present_data$se <- present_data$std / sqrt(present_data$N)

present_data$variable <- sapply(present_data$variable, make_title)
present_data$variable <- sapply(present_data$variable, function(x) gsub(' Present', '', x))


ggplot(present_data, aes(x = reorder(variable, mean), y = mean, fill = category)) +
  geom_bar(position = "dodge", stat = "identity") +
  ggtitle("Percentage of Reviews with each Theme") +
  xlab("Theme") + ylab("Percentage of Reviews") +
  scale_fill_brewer(palette = "Accent", name = "Category") +
  theme_bw() + theme(axis.text.x = element_text(angle = 60, vjust = 0.5)) + ylim(0, 50)
ggsave("themes_all.png", dpi = 300)


# Only mexican and authentic
plot_data <- subset(present_data, variable %in% c("Authentic", "Ethnicity"))
p <- ggplot(plot_data, aes(x = variable, y = mean, fill = category)) +
  geom_bar(position = "dodge", stat = "identity") +
  ggtitle("Percentage of Reviews with each Theme") +
  xlab("Theme") + ylab("Percentage of Reviews") +
  scale_fill_brewer(palette = "Accent", name = "Category") + theme_bw() +
  theme(text = element_text(family="serif")) +
  geom_errorbar(aes(ymax = mean + se, ymin = mean - se), width=0.8,
                position = position_dodge(width=0.9))

g <- arrangeGrob(p, sub = textGrob("Note: Data are from Yelp Academic Challenge, Round 8.  Black lines represent standard errors.",
                                   x = unit(0.02, "npc"), just = "left",
                                   gp = gpar(fontsize = 10, fontfamily="serif")),
                 nrow = 2, heights = c(20, 1))

ggsave("themes.png", g, dpi = 300)



# Only mexican for Phoenix vs. Urbana-Champaign
academic_data$ethnicity_present <- as.numeric(academic_data$ethnicity_present)
academic_data$authentic_present <- as.numeric(academic_data$authentic_present)
means <- ddply(academic_data, .(state, category), summarise,
                  ethnicity_present = mean(ethnicity_present, na.rm=T) * 100,
                  authentic_present = mean(authentic_present, na.rm=T) * 100)
sd <- ddply(academic_data, .(state, category), summarise,
               ethnicity_present = sd(ethnicity_present, na.rm=T) * 100,
               authentic_present = sd(authentic_present, na.rm=T) * 100)
N <- ddply(academic_data, .(state, category), summarise,
           N = sum(!is.na(ethnicity_present)))

means <- melt(means, id.vars=c('state', 'category'), value.name="mean")
sd <- melt(sd, id.vars=c('state', 'category'), value.name="sd")
sd <- merge(sd, N, by=c('state', 'category'))
plot_data <- merge(means, sd, by=c("state", "category", "variable"))
# SE = SD / sqrt(N)
plot_data$se <- plot_data$sd / sqrt(plot_data$N)
plot_data$variable <- sapply(plot_data$variable, make_title)
plot_data$variable <- sapply(plot_data$variable, function(x) gsub(' Present', '', x))
plot_data <- subset(plot_data, state %in% c("IL", "AZ") & category %in% c("Mexican", "Italian"))


my.cols <- brewer.pal(8, "Accent")[2:8]
p1 <- ggplot(subset(plot_data, state=="AZ"),
              aes(x = variable, y = mean, fill = category)) +
    geom_bar(position = "dodge", stat = "identity") +
    ggtitle("Phoenix, AZ") + xlab("") + ylab("% Reviews") +
    geom_errorbar(aes(ymax = mean + se, ymin = mean - se), width=0.8,
                  position = position_dodge(width=0.9)) +
  scale_fill_manual(values = my.cols, name = "Category") + theme_bw() +
  theme(text = element_text(family="serif"), legend.position="none") + ylim(0, 45)

p2 <- ggplot(subset(plot_data, state=="IL"),
             aes(x = variable, y = mean, fill = category)) +
  geom_bar(position = "dodge", stat = "identity") +
  ggtitle("Urbana-Champaign, IL") + xlab("") + ylab("% Reviews") +
  geom_errorbar(aes(ymax = mean + se, ymin = mean - se), width=0.8,
                position = position_dodge(width=0.9)) +
  scale_fill_manual(values = my.cols, name = "Category") + theme_bw() +
  theme(text = element_text(family="serif"), legend.position="none") + ylim(0, 45)
  
p1.leg <- ggplot(subset(plot_data, state=="AZ"),
                 aes(x = variable, y = mean, fill = category)) +
  geom_bar(position = "dodge", stat = "identity") +
  theme(text = element_text(family="serif")) +
  scale_fill_manual(values = my.cols, name = "Category")
  
g_legend <- function(a.gplot){
  tmp <- ggplot_gtable(ggplot_build(a.gplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)}
legend <- g_legend(p1.leg)

g <- grid.arrange(arrangeGrob(p1, p2, legend, ncol=3, widths=c(3/7,3/7,1/7)))
g2 <- arrangeGrob(g, sub = textGrob("Note: Data are from Yelp Academic Challenge, Round 8.  Black lines represent standard errors.",
                                    x = unit(0.02, "npc"), just = "left",
                                    gp = gpar(fontsize = 8, fontfamily="serif")),
                  nrow = 2, heights = c(20, 1))
ggsave("themes_Phoenix_Urbana.png", g2, dpi = 300)
