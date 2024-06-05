import requests
import time
from telebot import TeleBot


# login

login_url = 'https://partner.sbermegamarket.ru/api/merchantUIService/v1/securityService/session/start'
headers_start = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '92',
    'Content-Type': 'application/json',
}

payload_login = {
    "meta":{"from":"mui-router"},
    "data":
    {"login":"LOGIN",
    "password":"PASSWORD"}
}

res_log = requests.post(login_url, headers = headers_start, json=payload_login)
session = res_log.json()['data']['sessionId']


# search orders

search_url = 'https://partner.sbermegamarket.ru/api/merchantUIService/v1/orderService/order/search'
method = 'post'

payload = {
    "meta": {"from":"mui-main"},
        "data":{
            "isDeleteCanceledItems": True,
                "statuses":["NEW"],
                "orderBy":{"confirmationDate":"asc"},
                "deliveryMethods":["PICKUP","COURIER"],
                "fulfillmentMethod":["FULFILLMENT_BY_MERCHANT"],
                "serviceSchemes":["DELIVERY_BY_GOODS"],
                "offset": 0,
                "limit": 30,
                "sessionId": session
                }
}

headers_check = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '321',
    'Content-Type': 'application/json',
}

res = requests.post(search_url, headers=headers_check, json=payload)
data = res.json()


# Sending a message if a new order to the Bot

bot = TeleBot('TOKEN')
while True:
    count_orders = data['data']['total']
    if count_orders > 0:
        for i in range(count_orders):
            shipment_id = str(data['data']['items'][i]['shipmentId'])
            try:
                with open('orders.txt', 'r') as file:
                    order_total = file.readlines()
                    orders = [line.strip() for line in order_total]
            except FileNotFoundError:
                orders = []
                print('Файл не найден')
            if shipment_id not in orders:
                bot.send_message(chat_id='CHATID', text=f'Новый заказ! \nНомер заказа - {shipment_id}')
                orders.append(shipment_id)
                with open('orders.txt', 'w') as file:
                    file.seek(0)
                    file.truncate()
                    file.write('\n'.join(orders))
                print('Заказ отправлен')
            else:
                print('Бот уже оповестил об этом заказе')
    time.sleep(5)