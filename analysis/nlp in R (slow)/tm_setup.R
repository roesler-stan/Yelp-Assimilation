library(tm)
library(stringr)

cat_data_small <- cat_data[1:100, ]

# Create a dataset where each category has one long blob of text
corpus_data <- NULL
for (category in unique(cat_data$category)) {
  subset <- cat_data[cat_data$category == category, ]
  text <- str_c(subset$review, collapse = " ")
  row <- data.frame(category, text)
  corpus_data <- rbind(corpus_data, row)
}

myReader <- readTabular(mapping = list(content = "text", id = "category"))
corpus <- Corpus(DataframeSource(corpus_data), readerControl = list(reader = myReader))

corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation, preserve_intra_word_dashes = F)
corpus <- tm_map(corpus, stemDocument)
corpus <- tm_map(corpus, stripWhitespace)

# The following line takes a LONG time - so do the later line instead
#corpus <- tm_map(corpus, removeWords, stopwords("english"))  # Remove stopwords

termDocMatrix <- TermDocumentMatrix(corpus)
term_data <- data.frame(inspect(termDocMatrix))
term_data$term <- row.names(term_data)
term_data <- subset(term_data, !(term %in% stopwords()))
