import sqlite3
import requests
from bs4 import BeautifulSoup

url = 'https://csgohub.ru/cases.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
tags = soup.find_all('div', class_="skins-tab-case-section center-block")

case_names = {}

for i in range(len(tags)):
    itemName = tags[i].find('h3', class_="case_section_name").text.strip()
    cur_res = []
    cur_url = 'https://csgohub.ru/' + soup.find('a', href=True, title=itemName)['href']
    cur_response = requests.get(cur_url)
    cur_soup = BeautifulSoup(cur_response.text, 'lxml')
    cur_tags = cur_soup.find_all('div', class_="skins-tab center-block")
    for j in cur_tags:
        item = str(getattr(j.find('h3'), 'text', None))
        qual = str(getattr(j.find('p', class_='nomargin'), 'text', None))
        cost = str(getattr(j.find('span', attrs={'data-toggle': 'tooltip'}), 'text', None))
        cur_res.append([item, qual, cost])
    case_names[itemName] = cur_res

try:
    sqlite_connection = sqlite3.connect('guns.db')
    cursor = sqlite_connection.cursor()

    for i in range(len(case_names)):
        box = [n for n in case_names.keys()][i]
        guns = [k for k in case_names.get(box)]
        for j in range(len(guns)):
            cost = guns[j][2].split('\n- ')[0][1:]
            quality = guns[j][1].split('\xa0')[0][1:]
            if '★' not in guns[j][0] and guns[j][0] != 'None' and 'Неизвестно' not in guns[j][0]:
                sqlite_insert_query = f"""INSERT INTO guns
                                          (name, quality, box, cost)
                                          VALUES
                                          (?, ?, ?, ?);"""
                print([guns[j][0]])
                name_1 = guns[j][0].replace(' ', '%20')
                name_2 = name_1.replace('|', '%7C')
                name_3 = name_2.replace('\n', '')
                print([name_3])
                count = cursor.execute(sqlite_insert_query, [name_3, quality, box, cost])
    sqlite_connection.commit()
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
