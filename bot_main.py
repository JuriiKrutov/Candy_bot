import telebot
from telebot import types
import random

bot = telebot.TeleBot('5821547541:AAHdRwFbRlGlffSPnrbATJLOY4sQSR0qoFg')

candy = 221
max_candy = 28
take_us = 0
take_b = 0
flag = ''


@bot.message_handler(commands=['start'])
def start(message):
    global flag
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Начать игру')
    btn2 = types.KeyboardButton('Правила')
    murkup.add(btn1, btn2)
    bot.send_message(message.chat.id, f'Приветствую вас в игре {message.from_user.first_name}', reply_markup=murkup)

@bot.message_handler(content_types=['text'])
def new_game(message):
    global candy
    if message.text == 'Начать игру':
        candy = 221
        bot.send_message(message.chat.id, f'в ирге всего {candy} конфет')
        flag = random.choice(['user', 'bot'])
        if flag == 'user':
            bot.send_message(message.chat.id, 'Первым ходите вы')
            controller(message)
        else:
            bot.send_message(message.chat.id, 'Первым ходит бот')
            controller(message)
    elif message.text == 'Правила':
        bot.send_message(message.chat.id, "Вы играете против бота. На столе лежит 221 конфета, каждый игрок поочередно"
                                          "берет не менее 1 и не более 28 конфет, выигрывает тот кто забрал последние "
                                          "конфеты со стола. Первый игрок выбирается рандомно")
        start(message)


def controller(message):
    global flag
    if candy > 0:
        if flag == 'user':
            bot.send_message(message.chat.id, 'Ваш ход, возьмите не меньше 1 и не больше 28 конфет')
            bot.register_next_step_handler(message, take_user)
        else:
            bot.send_message(message.chat.id, 'Ход бота')
            take_bot(message)
    else:
        if flag == 'user':
            bot.send_message(message.chat.id, 'В этот раз победил бот, попробуйте еще раз)')
        else:
            bot.send_message(message.chat.id, f'Поздравляю {message.from_user.first_name} Вы победили эту бездушную машину')


def take_bot(message):
    global candy, take_b, flag
    if candy <= max_candy:
        take_b = candy
    elif candy % max_candy == 0:
        take_b = max_candy - 1
    else:
        take_b = candy % max_candy - 1
        if take_b == 0:
            take_b = 1
    candy -= take_b
    bot.send_message(message.chat.id, f'бот взял {take_b} конфет, на столе осталось {candy} конфет')
    flag = 'user'
    controller(message)


def take_user(message):
    global flag, take_us, candy
    take_us = int(message.text)
    if 0 < take_us < 29 and take_us <= candy:
        candy -= take_us
        bot.send_message(message.chat.id, f'осталось {candy} конфет')
        flag = 'bot'
    else:
        bot.send_message(message.chat.id, 'Вы ввели неверное количество, попробуйте снова')
    controller(message)


bot.infinity_polling()
