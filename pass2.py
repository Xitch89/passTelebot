import telebot
import random
import string

bot = telebot.TeleBot('6227538798:AAFfukZtOuhEP9LeRp5qmR3LUXSsiJjKznc')

# Змінна для зберігання поточного етапу генерації паролю
stage = 0
foundation1 = ""

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт Забувака )) Я згенерую пароль який ти 'напевно' не забудеш введи перший набір символів(це може бути адреса сайту,але без знаків ( , / . = ) ) : ")

# Команда /stop
@bot.message_handler(commands=['stop'])
def send_stop(message):
    bot.reply_to(message, "Бот зупинено")
    bot.stop_polling()

# Команда /restart
@bot.message_handler(commands=['restart'])
def send_restart(message):
    bot.reply_to(message, "Перезавантаження бота")
    bot.stop_polling()
    bot.polling()

# Обробник повідомлень
@bot.message_handler(func=lambda message: True)
def generate_password(message):
    global stage, foundation1, foundation2
    if stage == 0:
        # Отримання введення першого набору символів
        foundation1 = message.text
        # Перехід на наступний етап генерації паролю
        stage += 1
        # Очікування введення другого набору символів
        bot.reply_to(message, "Введіть другий набір символів(краще коли це буде слово пароль яке ви не забудете та матиме великі літери,малі,цифри та символ):")
    elif stage == 1:
        # Отримання введення другого набору символів
        foundation2 = message.text
        # Перехід на наступний етап генерації паролю
        stage += 1
        # Очікування введення довжини паролю
        bot.reply_to(message, "Введіть довжину паролю яку б ви хотіли отримати :")
    elif stage == 2:
        # Отримання введення довжини паролю
        pass_len = int(message.text)
        # Генерація паролю
        random.seed(0)
        password_list = []
        for i in range(pass_len):
            if i == 0:  # перший символ - велика літера
                password_list.append(random.choice(foundation1).upper())
            elif i == pass_len - 2:  # передостанній символ - цифра
                password_list.append(random.choice(string.digits))
            elif i == pass_len - 1:  # останній символ - символ
                password_list.append(random.choice(string.punctuation))
            elif i % 2 == 0:
                password_list.append(random.choice(foundation1))
            else:
                password_list.append(random.choice(foundation2))
        password = ''.join(password_list)
        bot.reply_to(message, "Your password is: {}".format(password))
        # Повернення до початкового етапу генерації паролю
        stage = 0
        foundation1 = ""
        foundation2 = ""

bot.polling()