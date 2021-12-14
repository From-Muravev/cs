import sqlite3
import requests
from bs4 import BeautifulSoup
from steampy.client import SteamClient
from config import *


def decorator_open_data_base(func):
    def open_data_base():
        con = sqlite3.connect("guns.db")
        mouse = con.cursor()
        func(mouse)
        con.close()

    return open_data_base


def market(func):
    def result(*args, **kwargs):
        x = requests.get(func(*args, **kwargs))
        if dict(x.content).get("success"):
            print('Успешно')
        else:
            print(x.content)

    return result


@decorator_open_data_base
def cost_update(mouse, current_cost_of_weapons, current_weapons, current_box):
    for i in current_weapons:
        url = f'https://market.csgo.com/?t=all&search={current_weapons[i]}&sd=desc'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        tags = soup.find_all("a", {"class": "item"})
        item_prices = tags[i].find('a', class_="price").text.strip()
        if item_prices is not None:
            current_cost_of_weapons.append(sorted(item_prices, reverse=False)[0])
            sql = """UPDATE guns SET nickname = %s WHERE id = %s"""
            mouse.execute(sql, (current_weapons[i], current_cost_of_weapons[i]))


@decorator_open_data_base
def find_weapons(mouse, current_box):
    result = mouse.execute("""SELECT * FROM guns
                WHERE box = ?""", ()).fetchall(current_box)
    return result


@market
def sale(id_weapon, price):
    return f'https://market.csgo.com/api/v2/add-to-sale?key=[your_secret_key]&id=[{id_weapon}]&price=[{price}]&cur=[RUB]'


@market
def buy(id_weapon, price):
    return f'https://market.csgo.com/api/v2/buy?key=[your_secret_key]&id=[{id_weapon}]&price=[{price}]'


def accept_contract():
    steam_client = SteamClient(MY_API_KEY)
    steam_client.login(MY_USERNAME, MY_PASSWORD, 'steam_guard.json')
    steam_client.accept_trade_offer(trade_id)

# class weapon:
#     def __init__(self, name, quality):
#         self.quality = quality
#         self.cost = 0
#         self.name = name
#
#     def change(self, cost):
#         self.cost = cost
#
#
# class contract:
#     def __init__(self, weapons):
#         all = [self.gun1 = weapon()
#         self.gun2 = weapon()
#         self.gun3 = weapon()
#         self.gun4 = weapon()
#         self.gun5 = weapon()
#         self.gun6 = weapon()
#         self.gun7 = weapon()
#         self.gun8 = weapon()
#         self.gun9 = weapon()
#         self.gun10 = weapon()]
#
#     def change(self):
#         for i in sorted(weapons, key=lambda x: x[0]):
#             weapon(i[0]).change(i[1])
