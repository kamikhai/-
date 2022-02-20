import requests as req
from bs4 import BeautifulSoup

host = "https://petsi.net"

# Считываем страницу со всеми породами собак
articles = req.get(host + "/dog-breeds")
soup = BeautifulSoup(articles.text, 'lxml')

# Находим все блоки div, в которых содержатся ссылки на статьи о собаках
all_div = soup.findAll('div', {'class': 'page-dog-breeds__list-item-wrapper'})
index = open("index.txt", "a")
for i in range(0, len(all_div)):
    # Получаем ссылку на статью
    a = all_div[i].find('a')
    # Записываем ссылку в файл index.txt
    index.write(str(i + 1) + " " + host + a['href'] + "\n")

    # Открываем страницу со статьей о конкретной породе
    article = req.get(host + a['href'])
    soup = BeautifulSoup(article.text, 'lxml')
    post = soup.findAll('div', {'class': 'breed-view__content-item-text typography'})
    out = open("страница " + str(i + 1) + ".txt", "a")

    # Записываем все абзацы в выходной файл
    for div in post:
        out.write(div.text + "\n")
    out.close()
index.close()
