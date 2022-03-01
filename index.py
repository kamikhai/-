from nltk.tokenize import word_tokenize
import pymorphy2


def create_index():

    # считываем леммы, полученные в прошлой домашней работе
    lemmas_file = open("lemmas.txt", "r")
    index = {}
    for line in lemmas_file:
        lemma = line.split(':')[0]
        index[lemma] = []

    # проходимся по всем текстам и записываем для каждой леммы страницы, на которых она присутствует
    morph = pymorphy2.MorphAnalyzer()
    for i in range(1, 218):
        f = open("Выкачка/страница " + str(i) + ".txt", "r")
        text = f.read()
        tokens = word_tokenize(text)
        for token in tokens:
            normal_form = morph.parse(token)[0].normal_form
            if normal_form in index:
                index[normal_form].append(i)
    return index

# записываем индекс в файл
def write_to_file(index):
    # записываем леммы в файл
    inverted_index_file = open("inverted_index.txt", "a")
    for i in index:
        inverted_index_file.write(i + ":")
        for num in index[i]:
            inverted_index_file.write(" " + str(num))
        inverted_index_file.write("\n")
    inverted_index_file.close()

def bool_search(text):
    # считываем индекс из файла
    inverted_index_file = open("inverted_index.txt", "r")
    index = {}
    for line in inverted_index_file:
        lemma = line.split(':')[0]
        index[lemma] = []
        for num in line.split(": ")[1].split(" "):
            index[lemma].append(int(num))

    parts = text.split(" ")
    for i in range(1, len(parts), 2):
        if parts[i].lower() != 'or' and parts[i].lower() != 'and':
            print('Введите корректный запрос')
            return {}

    if len(parts) % 2 == 0:
        print('Введите корректный запрос')
        return {}

    morph = pymorphy2.MorphAnalyzer()
    normal_form = morph.parse(parts[0])[0].normal_form

    if normal_form in index:
        print(index[normal_form])
        result = set(index[normal_form])
    else:
        result = set

    for i in range(2, len(parts), 2):
        normal_form = morph.parse(parts[i])[0].normal_form
        if normal_form in index:
            print(index[normal_form])
            if parts[i-1] == 'and':
                result = result.intersection(index[normal_form])
            else:
                result = result.union(index[normal_form])

    return result

# index = create_index()
# write_to_file(index)
print(bool_search("надёжный and совершенный"))
