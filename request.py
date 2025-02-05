import requests

# # тут мы просто добоавляем гриб в БД с грибами
# url = "http://57.129.138.22:1001/mushrooms"
# payload = {
#     "id": 1,
#     "name": "Белый гриб",
#     "edible": True,
#     "weight": 250.5,
#     "freshness": "свежий"
# }

# response = requests.post(url, json=payload)
# print("Создание гриба:", response.json())


# # изменим информацию о грибе по его id
# url = "http://57.129.138.22:1001/mushrooms/1"
# payload = {
#     "id": 1,
#     "name": "Белый гриб",
#     "edible": True,
#     "weight": 155.0,
#     "freshness": "застарелый"
# }

# response = requests.put(url, json=payload)
# print("Обновление гриба:", response.json())


# # информация о грибе по его id
# url = "http://57.129.138.22:1001/get_mushrooms/3"

# response = requests.get(url,)
# print("Инфа про гриб:", response.json())



# # Создаем корзинку
# url = "http://57.129.138.22:1001/baskets"
# payload = {
#     "id": 1,
#     "owner": 'admin',
#     "capacity": 1000.1,
# }

# response = requests.post(url, json=payload)
# print("Созданная корзинка:", response.json())



# # Добовляем гриб в корзинку
# url = "http://57.129.138.22:1001/baskets/1/mushrooms"
# payload = {
#     "mushroom_id": 1,
# }

# response = requests.post(url, json=payload)
# print("Добовляем гриб в корзинку", response.json())




# # Получаем инфо по корзине
# url = "http://57.129.138.22:1001/baskets/1"

# response = requests.get(url,)
# print("Инфо по корзине", response.json())



# Добовляем гриб в корзинку
url = "http://57.129.138.22:1001//baskets/1/mushrooms/1"

response = requests.delete(url,)
print("Удаляем гриб из корзинки", response.json())

