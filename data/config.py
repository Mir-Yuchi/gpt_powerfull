from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
image = "https://forbes.ua/static/storage/thumbs/1200x630/a/cc/88089e70-b688f05166dd810e8c285ba777ed8cca.jpg?v=4505_5"

f = open('tokens.txt', 'r')
tokens = f.read().split("\n")
f.close()
