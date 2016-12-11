library(tm)
library(stringr)
library(reshape)
library(jpeg)

valid_states <- c("PA", "NV", "AZ", "NC", "WI", "IL")
state_data <- subset(academic_data, state %in% valid_states)



# Create a dataset where each state has one long blob of text
corpus_data_states <- NULL
for (state in unique(state_data$state)) {
  subset <- state_data[state_data$state == state, ]
  text <- str_c(subset$review, collapse = " ")
  row <- data.frame(state, text)
  corpus_data_states <- rbind(corpus_data_states, row)
}

myReader <- readTabular(mapping = list(content = "text", id = "state"))
corpus_states <- Corpus(DataframeSource(corpus_data_states),
                       readerControl = list(reader = myReader))

corpus_states <- tm_map(corpus_states, content_transformer(tolower))
corpus_states <- tm_map(corpus_states, removePunctuation, preserve_intra_word_dashes = F)
corpus_states <- tm_map(corpus_states, stemDocument)
corpus_states <- tm_map(corpus_states, stripWhitespace)

termDocMatrix_states <- TermDocumentMatrix(corpus_states)
term_data_states <- data.frame(inspect(termDocMatrix_states))
term_data_states$term <- row.names(term_data_states)
term_data_states <- subset(term_data_states, !(term %in% stopwords()))



setwd("/Users/katharina/Dropbox/Projects/Yelp/Output/plots")

weightedTermDocMatrix_states <- weightTfIdf(termDocMatrix_states)
weighted_terms_states <- data.frame(inspect(weightedTermDocMatrix_states))
weighted_terms_states$term <- row.names(weighted_terms_states)
row.names(weighted_terms_states) <- NULL

weighted_terms_wide_states <- melt(weighted_terms_states, id.vars = "term", variable_name = "state")

plot_data <- NULL
for (s in valid_states) {
  d <- subset(weighted_terms_wide_states, state == s)
  d <- d[order(-d$value), ]
  d <- d[1:20,]
  row.names(d) <- NULL
  d$rank <- row.names(d)
  d$rank <- as.numeric(d$rank)
  plot_data <- rbind(plot_data, d)
}


pa <- readJPEG("../images/pennsylvania.jpg"); pennsylvania <- rasterGrob(pa, interpolate=TRUE)
il <- readJPEG("../images/illinois.jpg"); illinois <- rasterGrob(il, interpolate=TRUE)
nc <- readJPEG("../images/north carolina.jpg"); north_carolina <- rasterGrob(nc, interpolate=TRUE)
nv <- readJPEG("../images/nevada.jpg"); nevada <- rasterGrob(nv, interpolate=TRUE)
wi <- readJPEG("../images/wisconsin.jpg"); wisconsin <- rasterGrob(wi, interpolate=TRUE)
az <- readJPEG("../images/arizona.jpg"); arizona <- rasterGrob(az, interpolate=TRUE)

ggplot(plot_data, aes(state, ((rank * -1) - 3.5))) + 
  geom_point(color = "white") + 
  geom_label(aes(label = plot_data$term, fill = plot_data$state),
             color = 'white', fontface = 'bold', size = 2) +
  scale_fill_manual(values = c("#C20631", "#673e1e", "#21B726", "#F5871F", "#5BE1C6", "#266E35")) +
  theme_classic() +
  theme(legend.position = 1, plot.title = element_text(size = 16)) +
  labs(title = "Most Characteristic Words") + 
  xlab("") + ylab("Ranking") +
  scale_y_continuous(limits = c(-24, -1), breaks = c(-23.5, -14, -4.5),
                     labels = c("#20", "#10", "#1")) +
  annotation_custom(pennsylvania, xmin=.5, xmax=1.5, ymin=0, ymax=-4) + 
  annotation_custom(illinois, xmin=1.5, xmax=2.5, ymin=0, ymax=-4) + 
  annotation_custom(north_carolina, xmin=2.5, xmax=3.5, ymin=0, ymax=-4) +
  annotation_custom(nevada, xmin=3.5, xmax=4.5, ymin=0, ymax=-4) + 
  annotation_custom(wisconsin, xmin=4.5, xmax=5.5, ymin=0, ymax=-4) + 
  annotation_custom(arizona, xmin=5.5, xmax=6.5, ymin=0, ymax=-4)

ggsave("tfidf_bystate.png", dpi = 300)
