from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import pymorphy2
import collections
import math

# необходимые методы

def get_tokens():
    tokens_file = open("tokens.txt", "r")
    tokens = []
    for line in tokens_file:
        tokens.append(line.replace('\n', ''))
    return tokens


def get_lemmas():
    lemmas_file = open("lemmas.txt", "r")
    lemmas = []
    for line in lemmas_file:
        lemmas.append(line.split(':')[0])
    return lemmas


def count_tf(text):
    words_frequency = collections.Counter(text)
    tf = dict()
    for t in text:
        tf[t] = words_frequency[t] / float(len(text))
    return tf


def count_idf(texts, words):
    idf = dict()
    for word in words:
        idf[word] = math.log10(len(texts) / sum([1.0 for i in texts if word in i]))
    return idf


def count_tf_idf(tf, idf):
    tf_idf = dict()
    for word in tf:
        tf_idf[word] = tf[word] * idf[word]
    return tf_idf


# считываем все токены и леммы
tokens = get_tokens()
lemmas = get_lemmas()

# считываем все тексты из файлов 1 задания
texts = []
for i in range(1, 218):
    f = open("Выкачка/страница " + str(i) + ".txt", "r")
    texts.append(f.read())

# из каждого текста получаем список токенов (не уникальных)
texts_tokens = []
for text in texts:
    text_tokens = word_tokenize(text.replace('.', ' '))
    stop_words = stopwords.words("russian")
    filtered_tokens = []
    r = re.compile("[а-я]")
    for token in text_tokens:
        if token not in stop_words and r.match(token) and len(token) > 1:
            filtered_tokens.append(token)
    texts_tokens.append(filtered_tokens)

# подсчитываем idf всех токенов
tokens_idf = count_idf(texts_tokens, tokens)

# подсчитываем tf и tf-idf токенов и записываем результаты в файл
i = 1
for text_tokens in texts_tokens:
    tokens_tf = count_tf(text_tokens)
    tokens_tf_idf = count_tf_idf(tokens_tf, tokens_idf)
    tokens_result_file = open("tokens/страница " + str(i) + ".txt", "a")
    for token in tokens_tf:
        tokens_result_file.write(f'{token} {tokens_idf[token]} {tokens_tf_idf[token]}\n')
    tokens_result_file.close()
    i += 1

# имеющиеся токены переводим в леммы
texts_lemmas = []
morph = pymorphy2.MorphAnalyzer()
for text_tokens in texts_tokens:
    text_lemmas = []
    for token in text_tokens:
        text_lemmas.append(morph.parse(token)[0].normal_form)
    texts_lemmas.append(text_lemmas)

# подсчитываем idf всех лемм
lemmas_idf = count_idf(texts_lemmas, lemmas)

# подсчитываем tf и tf-idf лемм и записываем результаты в файл
i = 1
for text_lemmas in texts_lemmas:
    lemmas_tf = count_tf(text_lemmas)
    lemmas_tf_idf = count_tf_idf(lemmas_tf, lemmas_idf)
    lemmas_result_file = open("lemmas/страница " + str(i) + ".txt", "a")
    for lemma in lemmas_tf:
        lemmas_result_file.write(f'{lemma} {lemmas_idf[lemma]} {lemmas_tf_idf[lemma]}\n')
    lemmas_result_file.close()
    i += 1

lemmas_idf_file = open("lemmas_idf.txt", "a")
for lemma in lemmas_idf:
    lemmas_idf_file.write(f'{lemma} {lemmas_idf[lemma]}\n')
lemmas_idf_file.close()
