import requests
from bs4 import BeautifulSoup
import json
import csv

url = "https://ctv7.ru/news"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text
# print(src)

# with open("index.html", "w") as file:
#     file.write(src)

soup = BeautifulSoup(src, "lxml")
all_pages_href = soup.find_all(class_="generic-page generic-button")
all_numbers_of_pages = {}
all_numbers_of_pages['1'] = "https://ctv7.ru/news/"
for item in all_pages_href:
    item_text = item.text
    item_href = "https://ctv7.ru" + item.get("href")
    if item.text == str(3043):
        break
    all_numbers_of_pages[item_text] = item_href

with open("all_numbers_of_pages.json", "w") as file:
    json.dump(all_numbers_of_pages, file, indent=4, ensure_ascii=False)

with open("all_numbers_of_pages.json") as file:
    all_pages = json.load(file)

for news_name, pages_href in all_pages.items():
    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in news_name:
            news_name = news_name.replace(item, "_")
    req = requests.get(url=pages_href, headers=headers)
    src = req.text

    with open(f"data/news_{news_name}.html", "w") as file:
        file.write(src)
    with open(f"data/news_{news_name}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    table_head = ["Новость", "Краткое описание", "Дата и время", "Кол-во просмотров"]
    with open(f"data/news_{news_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                table_head[0],
                table_head[1],
                table_head[2],
                table_head[3]
            )
        )
    # собираем новости
    news_data = soup.find(class_="plitka")
    news_info = []
    news_info_table = []
    for item in news_data:
        if item.find("div class") == -1:
            continue
        news_info = item.find_all("div")
        title_news = news_info[0].find("a").text
        # print(title_news)
        time_news = news_info[0].find("p").text
        # print(time_news)
        short_description = news_info[3].find(class_="news-item-desc").text
        # print(short_description)
        views = news_info[4].find_all(class_="d-inline-block mr-2")[1].text
        # print(views)

        news_info_table.append({
            "Tittle": title_news,
            "Short description": short_description,
            "Time and Date": time_news,
            "Views": views
        })
        with open(f"data/news_{news_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title_news,
                    short_description,
                    time_news,
                    views
                )
            )