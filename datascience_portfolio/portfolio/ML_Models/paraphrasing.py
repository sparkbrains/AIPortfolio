import nltk
from django.conf import settings
import os
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize

# if os.path.isdir(settings.DIR_PUNKT) and os.path.isdir(settings.DIR_WORDNET):
#     path1 = os.path.join(settings.BASE_DIR,settings.N_PATH3)
#     path2 = os.path.join(settings.BASE_DIR,settings.N_PATH2)
#     nltk.data.path.append(path1)
#     nltk.data.path.append(path2)
# else:
#     nltk.download('wordnet' , download_dir=settings.BASE_D)

path1 = settings.N_PATH3
path2 = settings.N_PATH2
nltk.data.path.append(path1)
nltk.data.path.append(path2)




def get_synonyms(word, pos):
    synonyms = []
    for syn in wordnet.synsets(word, pos=pos):
        for lemma in syn.lemmas():
            synonym = lemma.name()
            if '_' not in synonym:  
                synonyms.append(synonym)
    return synonyms

def get_paraphrased_sentences(paragraph):

    sentences = sent_tokenize(paragraph)
    paraphrased_paragraph = []

    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged_words = nltk.pos_tag(words)
        paraphrased_sentence = []

        for word, tag in tagged_words:
            if tag.startswith('JJ'):  # Adjective
                synonyms = get_synonyms(word, wordnet.ADJ)
                paraphrased_word = synonyms[0] if synonyms else word
            elif tag.startswith('VB'):  # Verb
                synonyms = get_synonyms(word, wordnet.VERB)
                paraphrased_word = synonyms[1] if len(synonyms) > 1 else synonyms[0] if synonyms else word
            elif tag.startswith('NN'):  # Noun
                synonyms = get_synonyms(word, wordnet.NOUN)
                paraphrased_word = synonyms[0] if synonyms else word
            else:
                paraphrased_word = word  # Keep the word as it is for other POS tags

            paraphrased_sentence.append(paraphrased_word)

        paraphrased_sentence = ' '.join(paraphrased_sentence)
        paraphrased_paragraph.append(paraphrased_sentence)

    paraphrased_paragraph = ' '.join(paraphrased_paragraph)
    paraphrased_paragraph = '. '.join(s.capitalize() for s in paraphrased_paragraph.split('. '))

    return paraphrased_paragraph