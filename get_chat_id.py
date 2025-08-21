import requests

BOT_TOKEN = '8158133901:AAE-jkP2Pq0KVhR8KiIUYwtw0vR-E1brYw0'

url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
response = requests.get(url)
data = response.json()

for result in data['result']:
    try:
        chat = result['message']['chat']
        print(f"Chat title: {chat.get('title')}")
        print(f"Chat ID: {chat['id']}")
    except KeyError:
        continue
