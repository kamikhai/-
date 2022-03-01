from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import pymorphy2

text = ''
for i in range(1, 218):
    # считываем текст из исходного файла
    f = open("Выкачка/страница " + str(i) + ".txt", "r")
    text += f.read()

# разбиваем текст на токены
tokens = word_tokenize(text.replace('.', ' '))

# избавляемся от стоп-слов, знаков препинания и цифр
stop_words = stopwords.words("russian")
filtered_tokens = []
r = re.compile("[а-я]")
for token in tokens:
    if token not in stop_words and r.match(token) and len(token) > 1:
        filtered_tokens.append(token)
# получаем только уникальные слова
filtered_tokens = set(filtered_tokens)

# записываем токены в файл и создаем словарь лемм
tokens_file = open("tokens.txt", "a")
morph = pymorphy2.MorphAnalyzer()
lemmas = {}
for token in filtered_tokens:
    tokens_file.write(token + "\n")
    normal_form = morph.parse(token)[0].normal_form
    if normal_form in lemmas:
        lemmas[normal_form].append(token)
    else:
        lemmas[normal_form] = [token]
tokens_file.close()

# записываем леммы в файл
lemmas_file = open("lemmas.txt", "a")
for lemma in lemmas:
    lemmas_file.write(lemma + ":")
    for word in lemmas[lemma]:
        lemmas_file.write(" " + word)
    lemmas_file.write("\n")
lemmas_file.close()
