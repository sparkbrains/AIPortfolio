import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from django.conf import settings
import os

# if os.path.isdir(settings.DIR_PUNKT) and os.path.isdir(settings.DIR_CORPORA):
#     path1 = os.path.join(settings.BASE_DIR,settings.N_PATH1)
#     path2 = os.path.join(settings.BASE_DIR,settings.N_PATH2)
#     nltk.data.path.append(path1)
#     nltk.data.path.append(path2)
# else:
#     nltk.download('punkt' , download_dir=settings.DIR_PUNKT)
#     nltk.download('stopwords' , download_dir=settings.DIR_CORPORA)

path1 = settings.N_PATH1
path2 = settings.N_PATH2
nltk.data.path.append(path1)
nltk.data.path.append(path2)





def summarizer(paragraph):
    # Tokenize the paragraph into sentences
    sentences = sent_tokenize(paragraph)
    
    # Check if the original paragraph is longer than 500 words
    if len(paragraph.split()) > 500:
        # Sort the sentences based on their lengths
        sentences.sort(key=len)
        # Concatenate the shortest sentences until the total word count reaches 250
        summary = ""
        word_count = 0
        for sentence in sentences:
            word_count += len(sentence.split())
            if word_count <= 250:
                summary += sentence + " "
            else:
                break
    else:
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
        total_score = sum(sentence_scores.values())
        average_score = total_score / len(sentence_scores)
        
        # Sort the sentences based on their lengths
        sentences.sort(key=len)
        
        # Generate the summary by selecting the shortest sentences with scores above the average
        summary = ""
        word_count = 0
        for sentence in sentences:
            if sentence in sentence_scores and sentence_scores[sentence] > average_score:
                word_count += len(sentence.split())
                if word_count <= 250:
                    summary += sentence + " "
                else:
                    break
    summary = summary.strip()
    summary_len = len(summary.split(' '))
    raw_text = paragraph
    raw_text_len = len(paragraph.split(' '))

    # if summary_len <= 5:
    #     return "PLease enter a valid paragraph"
    
    return raw_text,raw_text_len,summary,summary_len
