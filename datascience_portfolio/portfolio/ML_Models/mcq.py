import warnings
warnings.filterwarnings("ignore")
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import numpy as np
import random
import re
import requests
from flashtext import KeywordProcessor
from django.conf import settings
import os
# if os.path.isdir(settings.DIR_WORDNET):
#     path1 = os.path.join(settings.BASE_DIR,settings.N_PATH3)
#     nltk.data.path.append(path1)

path1 = settings.N_PATH3
nltk.data.path.append(path1)
from nltk.corpus import wordnet as wn


def generate_questions_with_answers(paragraph, limit=10):
    def get_stopwords():
        return set(stopwords.words('english'))

    def tokenize_text(text):
        return word_tokenize(text)

    def filter_tokens(tokens, stopwords):
        return [word for word in tokens if word.lower() not in stopwords and word.isalpha()]

    def split_text_to_sentences(text):
        sentences = nltk.sent_tokenize(text)
        return [sent.strip() for sent in sentences if len(sent) > 15]

    def map_sentences_to_keywords(filtered_tokens, sentences):
        keyword_processor = KeywordProcessor()
        keyword_sentences = {}

        for token in filtered_tokens:
            keyword_sentences[token] = []
            keyword_processor.add_keyword(token)

        for sent in sentences:
            found_keywords = keyword_processor.extract_keywords(sent)
            for keyword in found_keywords:
                keyword_sentences[keyword].append(sent)

        for keyword in keyword_sentences.keys():
            keyword_sentences[keyword] = sorted(keyword_sentences[keyword], key=len, reverse=True)
        filtered_dict = {key: value for key, value in keyword_sentences.items() if value}

        return filtered_dict


    def get_word_sense(sentence, word):
        word = word.lower()
        if len(word.split()) > 0:
            word = word.replace(" ", "_")
        synsets = wn.synsets(word, 'n')
        if synsets:
            # Modify this section to use the desired word sense disambiguation method
            word_sense = synsets[0]  # Defaulting to the first synset
            return word_sense
        else:
            return None
    def get_wordnet_distractors(syn, word):
        distractors = []
        word = word.lower()
        act_word = word

        if len(word.split()) > 0:
            word.replace(" ", "_")

        hypernyms = syn.hypernyms()
        if len(hypernyms) == 0:
            return distractors

        for each in hypernyms[0].hyponyms():
            name = each.lemmas()[0].name()
            if name == act_word:
                continue
            name = name.replace("_", " ")
            name = " ".join(w.capitalize() for w in name.split())
            if name is not None and name not in distractors:
                distractors.append(name)

        return distractors

    def get_conceptnet_distractors(word):
        word = word.lower()
        act_word = word

        if len(word.split()) > 0:
            word = word.replace(" ", "_")

        distractors = []
        url = "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5" % (word, word)
        obj = requests.get(url).json()

        for edge in obj['edges']:
            link = edge['end']['term']
            url2 = "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10" % (link, link)
            obj2 = requests.get(url2).json()
            for edge in obj2['edges']:
                word2 = edge['start']['label']
                if word2 not in distractors and act_word.lower() not in word2.lower():
                    distractors.append(word2)

        return distractors

    def generate_questions(paragraph):
        stopwords = get_stopwords()
        tokens = tokenize_text(paragraph)
        filtered_tokens = filter_tokens(tokens, stopwords)
        filtered_list = np.unique(filtered_tokens)
        sentences = split_text_to_sentences(paragraph)
        mapped_sentences = map_sentences_to_keywords(filtered_list, sentences)
        mapped_answers = {}

        try:
            for keyword in mapped_sentences:
                word_sense = get_word_sense(mapped_sentences[keyword][0], keyword)
                if word_sense:
                    distractors = get_wordnet_distractors(word_sense, keyword)
                    if len(distractors) == 0:
                        distractors = get_conceptnet_distractors(keyword)

                    if len(distractors) != 0:
                        mapped_answers[keyword] = {
                            'answer': keyword.capitalize(),
                            'distractors': distractors
                        }
                else:
                    distractors = get_conceptnet_distractors(keyword)
                    if len(distractors) > 0:
                        mapped_answers[keyword] = {
                            'answer': keyword.capitalize(),
                            'distractors': distractors
                        }
            
        except:
            pass

        questions = []
        iterator = 1

        for keyword in mapped_answers:
            sentence = mapped_sentences[keyword][0]
            p = re.compile(keyword, re.IGNORECASE)
            question = p.sub("________", sentence)

            options = [keyword.capitalize()] + mapped_answers[keyword]['distractors']
            options = options[:4]
            random.shuffle(options)

            question_data = {
                'question_number': iterator,
                'question_text': question,
                'options': options,
                'answer': mapped_answers[keyword]['answer']
            }

            questions.append(question_data)
            iterator += 1

        return questions

    def generate_questions_limit(paragraph, limit):
        questions = generate_questions(paragraph)
        if limit > len(questions):
            limit = len(questions)
        return questions[:limit]

    return generate_questions_limit(paragraph, limit)



