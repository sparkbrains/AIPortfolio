import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize

def get_synonyms(word, pos):
    synonyms = []
    for syn in wordnet.synsets(word, pos=pos):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

def get_paraphrased_sentences(paragraph):
    sentences = sent_tokenize(paragraph)
    paraphrased_paragraph = []

    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
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
