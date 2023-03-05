import telebot
import random
import string

bot = telebot.TeleBot('6227538798:AAFfukZtOuhEP9LeRp5qmR3LUXSsiJjKznc')

# Variable to store the current stage of password generation
stage = 0
foundation1 = ""

# Command /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт Забувака )) Я згенерую пароль який ти 'напевно' не забудеш, введи перший набір символів(це може бути адреса сайту,але без знаків ( , / . = ) наприклад: wwwgooglecom ")

# Message handler
@bot.message_handler(func=lambda message: True)
def generate_password(message):
    global stage, foundation1, foundation2
    if stage == 0:
        # Get the first set of characters
        if len(message.text) > 100:
            bot.reply_to(message, "Набір символів не може бути довшим за 100 символів. Будь ласка, спробуйте ще раз.")
            return
        foundation1 = message.text
        # Move to the next stage of password generation
        stage += 1
        # Wait for the second set of characters
        bot.reply_to(message, "Введіть другий набір символів(краще коли це буде слово пароль яке ви не забудете та матиме великі літери,малі,цифри та символ) : ")
    elif stage == 1:
        # Get the second set of characters
        if len(message.text) > 100:
            bot.reply_to(message, "Набір символів не може бути довшим за 100 символів. Будь ласка, спробуйте ще раз.")
            return
        foundation2 = message.text
        # Move to the next stage of password generation
        stage += 1
        # Wait for the length of the password
        bot.reply_to(message, "Введіть довжину паролю яку б ви хотіли отримати :")
    elif stage == 2:
        # Get the length of the password
        try:
            pass_len = int(message.text) 
        except ValueError:
            bot.reply_to(message, "Це має бути ціле число. Повторіть спробу")
            return
        if pass_len > 100:
            bot.reply_to(message, "Довжина паролю не може бути більше 100 символів. Будь ласка, спробуйте ще раз.")
            return
        # Generate the password
        random.seed(0)
        password_list = []
        punctuation_chars = "/\@!#$%^&()}{><][?" #перелік знаків пунктуації
        for i in range(pass_len):
            if i == 0:  # first character - uppercase letter
                password_list.append(random.choice(foundation1).upper())
            elif i == pass_len - 2:  # second to last character - number
                password_list.append(random.choice(string.digits))
            elif i == pass_len - 1:  # last character - symbol
                password_list.append(random.choice(punctuation_chars))
            elif i % 2 == 0:
                password_list.append(random.choice(foundation1))
            else:
                password_list.append(random.choice(foundation2))
        password = ''.join(password_list)
        bot.reply_to(message, "Задля безпеки видаліть історію чату.Ви завжди зможете знайти свій пароль, повторно ввівши Ваші набори символів. Ваш пароль: ")
        bot.reply_to(message, "{}".format(password))
        # Повернення до початкового етапу генерації паролю
        stage = 0
        foundation1 = ""
        foundation2 = ""
        bot.reply_to(message, "Можемо продовжити генерувати наступний пароль за потреби чи повернути вже згенерований. Ви знаєте що робити 😉 ")

bot.polling()