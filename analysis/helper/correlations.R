## Plot correlations and distributions of patient health and county health features


library(Hmisc)
library(corrplot)
library(plyr)
library(reshape2)

setwd("C:/Users/kroesler/Google Drive/ARW/Output/medad cost")


# Only include numeric columns
cor_cols <- names(medad_data)[sapply(medad_data, function(x) class(x) == "numeric")]

# Make county average data
county_data <- ddply(medad_data[, c("fips_county_cd", cor_cols)], .(fips_county_cd), numcolwise(mean))

# Reverse order of columns
cols <- rev(names(county_data))
county_data <- county_data[, cols]


# Rename columns to look nice
make_title <- function(col) {
  col <- gsub("_", " ", col)
  s <- strsplit(col, " ")[[1]]
  col <- paste(toupper(substring(s, 1, 1)), substring(s, 2), sep = "", collapse = " ")
  return(col)  
}

names(county_data) <- sapply(names(county_data), make_title)

# Reorder columns to group similar variables together
col_names <- names(county_data)
cost_cols <- c("Potential Risk Score", "Total Cost", "Caregap", "Predicted Cost")
col_names <- col_names[! col_names %in% cost_cols]
col_names <- c(col_names, cost_cols)
county_data <- county_data[, col_names]

cor_cols <- names(county_data)[! names(county_data) %in% c("Fips County Cd", "Risk Score")]
vars <- county_data[, cor_cols]
M <- cor(vars, use = "pairwise.complete.obs")

# Find columns missing any correlation data
cor_data <- data.frame(M)
bad_cols <- names(cor_data)[sapply(cor_data, function(x)all(is.na(x)))]
remove_period <- function(x) {
  return(gsub(".", " ", x, fixed = T))
}
bad_cols <- lapply(bad_cols, remove_period)


# Now get a correlation matrix without the missing data
cor_cols <- cor_cols[! cor_cols %in% bad_cols]
vars <- county_data[, cor_cols]
M <- cor(vars, use = "pairwise.complete.obs")



## To check p-values
cor.mtest <- function(mat, conf.level = 0.95) {
  mat <- as.matrix(mat)
  n <- ncol(mat)
  p.mat <- lowCI.mat <- uppCI.mat <- matrix(NA, n, n)
  diag(p.mat) <- 0
  diag(lowCI.mat) <- diag(uppCI.mat) <- 1
  for(i in 1:(n-1)){
    for(j in (i+1):n){
      tmp <- cor.test(mat[,i], mat[,j], conf.level = conf.level)
      p.mat[i,j] <- p.mat[j,i] <- tmp$p.value
      lowCI.mat[i,j] <- lowCI.mat[j,i] <- tmp$conf.int[1]
      uppCI.mat[i,j] <- uppCI.mat[j,i] <- tmp$conf.int[2]
    }
  }
  return(list(p.mat, lowCI.mat, uppCI.mat))
}

res1 <- cor.mtest(vars, 0.95)
res2 <- cor.mtest(vars, 0.99)

# Squares' size and color for correlation strength, variables on left and top
# Leave insignificant correlations blank
diag(M) <- NA

png('medad_health_rcorr.png', height = 4000, width = 4000)
# order = "hclust"
corrplot(M, method = 'square', type = "lower", na.label = " ",
         tl.srt = 60, tl.cex = 2.5, cl.cex = 2, p.mat = res1[[1]], insig= "blank")
title(main = "County-Level Features' Correlations for Medicare Advantage Patients, 2015",
      cex.main = 6, line = -5)
dev.off()



# Table of correlations and their p-values
corr_table <- rcorr(as.matrix(vars), type = "pearson")



## Plot distribution of many health vars by payer
## Jitter plot of predicted cost / actual total cost and county health measures by payer
medad_data_complete <- subset(medad_data, !is.na(total_div_pred_cost))

cost_plot <- ggplot(medad_data_complete, aes(x = payer_name, y = total_div_pred_cost, colour = payer_name)) +
  geom_jitter(alpha = 0.9, size = 0.2)  + scale_color_brewer(palette = "Paired") + scale_y_log10(labels = comma) +
  guides(color = F) + ylab("Total / Predicted Cost") + xlab("Payer") + theme_bw() +
  stat_summary(fun.y = mean, colour = "black", geom = "point", shape = 18, size = 3, show.legend = FALSE) +
  stat_summary(fun.y = median, colour = "black", geom = "point", shape = 5, size = 3, show.legend = FALSE) +
  geom_hline(yintercept = 1, linetype = "dashed")

mean_value <- mean(medad_data_complete$diabetic_screening, na.rm = T) * 100
plot_county1 <- ggplot(medad_data_complete, aes(x = payer_name, y = diabetic_screening * 100, colour = payer_name)) +
  geom_jitter()  + scale_color_brewer(palette = "Paired") +
  guides(color = F) + ylab("Diabetic Screening") + xlab("Payer") + theme_bw() +
  stat_summary(fun.y = mean, colour = "black", geom = "point", shape = 18, size = 3, show.legend = FALSE) +
  stat_summary(fun.y = median, colour = "black", geom = "point", shape = 5, size = 3, show.legend = FALSE) +
  geom_hline(yintercept = mean_value, linetype = "dashed")

legend_plot <- ggplot(medad_data_complete, aes(x = payer_name, y = total_div_pred_cost, colour = payer_name)) +
  geom_point() + scale_colour_brewer(name = "Payer", palette = "Paired") + theme(legend.position = "bottom")

g <- ggplotGrob(legend_plot)$grobs
legend <- g[[which(sapply(g, function(x) x$name) == "guide-box")]]
lheight <- sum(legend$height)

cost_plot <- ggplot_gtable(ggplot_build(cost_plot))
plot_county1 <- ggplot_gtable(ggplot_build(plot_county1))


# Find the maximum width of the bottom and top left plots to give them both the same width
maxWidth = unit.pmax(cost_plot$widths[2:3], cost_plot$widths[2:3])
cost_plot$widths[2:3] <- maxWidth
plot_county1$widths[2:3] <- maxWidth

plots_grid <- grid.arrange(cost_plot, plot_county1, legend, nrow = 3, ncol = 1, heights = c(8, 8, 1))

g <- arrangeGrob(plots_grid, top = textGrob("Medicare Advantage Patients' Predicted vs. Total Cost and County Diabetic Screenings by Payer, 2015"))

g2 <- arrangeGrob(g, sub = textGrob("Payers' means across patients are represented by filled diamonds, medians are shown by hollow diamonds, and the dashed line shows county mean.  Total cost is on a log-10 scale.",
                                    x = unit(0.02, "npc"), just = "left", gp = gpar(fontsize = 10)), nrow = 2, heights = c(20, 1))

ggsave('medad_pred_total_cost_diabscr_payer_jitter.png', g2, dpi = 300, width = 12, height = 10)




## Barplot of mean values for several county measures by payer
county_health_cols <- names(medad_data)[28: 108]
# Also look at cost data
county_health_cols <- c(county_health_cols, "total_cost", "predicted_cost")

payer_means <- ddply(medad_data[, c("payer_name", county_health_cols)], .(payer_name), numcolwise(mean, na.rm = T))

# Constrain each mean to be between 0 and 1
payer_means[, county_health_cols] <- sapply(payer_means[, county_health_cols], min_max)


# Divide each value by the overall mean to normalize
# payer_means[, county_health_cols] <- payer_means[, county_health_cols] / colMeans(payer_means[, county_health_cols], na.rm = T)

# Remove columns that are only NA
Filter(function(x)!all(is.na(x)), payer_means)

payer_means.m <- melt(payer_means, id.vars = "payer_name")

# Sort by values for HMSA
hmsa_data <- subset(payer_means.m, payer_name == "HMSA")
variables <- hmsa_data[order(hmsa_data$value), ]$variable
payer_means.m$variable <- factor(payer_means.m$variable, levels = variables)
payer_means.m <- payer_means.m[order(payer_means.m$variable),]


p <- ggplot(payer_means.m, aes(x = payer_name, y = value, color = variable)) +
  #  geom_bar(position = "dodge", stat = "identity") +
  geom_point() +
  ggtitle("Medicare Advantage Patients' Counties' Mean Values by Payer, 2015") +
    xlab("County Measure Measure") + ylab("Mean Value (0-1)") + theme_bw() + guides(color = F) +
  stat_summary(fun.y = mean, colour = "black", geom = "point", shape = 18, size = 3, show.legend = FALSE) +
  stat_summary(fun.y = median, colour = "black", geom = "point", shape = 5, size = 3, show.legend = FALSE)

ggsave("county_means_payer.png", p, dpi = 300, width = 12, height = 10)


