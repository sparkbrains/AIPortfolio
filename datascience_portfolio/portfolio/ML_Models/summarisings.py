import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# Initialize NLTK modules
# nltk.download('punkt')
# nltk.download('stopwords')

def summarizer(raw_text):

    # Tokenize the paragraph into sentences
    sentences = sent_tokenize(raw_text)
    
    # Initialize stop words and stemmer
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()
    
    # Compute the word frequencies in the paragraph
    word_frequencies = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence):
            word = word.lower()
            if word not in stop_words:
                stem_word = stemmer.stem(word)
                if stem_word in word_frequencies:
                    word_frequencies[stem_word] += 1
                else:
                    word_frequencies[stem_word] = 1
    # Calculate the sentence scores based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence):
            word = word.lower()
            if word not in stop_words:
                stem_word = stemmer.stem(word)
                if stem_word in word_frequencies:
                    if sentence in sentence_scores:
                        sentence_scores[sentence] += word_frequencies[stem_word]
                    else:
                        sentence_scores[sentence] = word_frequencies[stem_word]
    
    # Determine the average sentence score
    total_score = 1
    total_score = sum(sentence_scores.values())
    sentence_scores.setdefault(' ', 1)
    average_score = total_score / len(sentence_scores)
    
    # Generate the summary by selecting sentences with scores above the average
    summary = [sentence for sentence, score in sentence_scores.items() if score > average_score]
    summary = ' '.join(summary)
    return summary,raw_text,len(raw_text.split(' ')) ,len(summary.split(' '))



