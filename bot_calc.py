import telebot
from telebot import types
import datetime

bot = telebot.TeleBot('5821547541:AAHdRwFbRlGlffSPnrbATJLOY4sQSR0qoFg')


def log(message):
    file = open('data.csv', 'a')
    file.write(f'{message.from_user.first_name}, {datetime.datetime.now()}, {message.text}\n')
    file.close()
@bot.message_handler(commands= ['start'])
def start(message):
    mrk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Целые')
    btn2 = types.KeyboardButton('Комплексные')
    mrk.add(btn1, btn2)
    bot.send_message(message.chat.id, f'Здравствуй {message.from_user.first_name}. Я бот калькулятор. Выбери'
                                      f' ниже с какими числами ты хочешь работать', reply_markup=mrk)

@bot.message_handler(content_types=['text'])
def controller(message):
    log(message)
    del_mrk = types.ReplyKeyboardRemove()
    if message.text == 'Целые':
        bot.send_message(message.chat.id, 'Целые числа поддерживают следующие операции:\nсложение "+"\nвычитаеие "-"\n'
                                          'умножение "*"\nделение "/"\nпроцентный остаток от деления "%"\nцелочисленное деление "//"', reply_markup=del_mrk)
        bot.send_message(message.chat.id, 'Введите свой пример, расставляя пробел между знаками')
        bot.register_next_step_handler(message, get_integer)

    elif message.text == 'Комплексные':
        bot.send_message(message.chat.id, 'Комплексные числа поддерживают следующие операции:\nсложение "+"\nвычитаеие "-"\n'
                                          'умножение "*"\nделение "/"', reply_markup=del_mrk)
        bot.send_message(message.chat.id, 'Введите свой пример, расставляя пробел между знаками')
        bot.register_next_step_handler(message, get_complex)



def get_integer(message):
    log(message)
    example = message.text.split()
    decision = 0
    if example[0].isdigit and example[2].isdigit:
        if example[1] in '+-/*//%':
            if example[1] == '+':
                decision = int(example[0]) + int(example[2])
            elif example[1] == '-':
                decision = int(example[0]) - int(example[2])
            elif example[1] == '/':
                if example[2] != '0':
                    decision = int(example[0]) / int(example[2])
                else:
                    bot.send_message(message.chat.id, 'На ноль делить нельзя')
                    controller(message)
            elif example[1] == '*':
                decision = int(example[0]) * int(example[2])
            elif example[1] == '//':
                decision = int(example[0]) // int(example[2])
            elif example[1] == '%':
                decision = int(example[0]) % int(example[2])
            bot.send_message(message.chat.id, f'{message.text} = {decision}')
        else:
            bot.send_message(message.chat.id, 'Вы ввели неверную операцию')
            controller(message)
    else:
        bot.send_message(message.chat.id, 'Вы ввели неверные значения')
        controller(message)

def get_complex(message):
    log(message)
    example = message.text.split()
    decision = 0
    if example[0].isdigit and example[2].isdigit:
        if example[1] in '+-/*':
            if example[1] == '+':
                decision = complex(example[0]) + complex(example[2])
            elif example[1] == '-':
                decision = complex(example[0]) - complex(example[2])
            elif example[1] == '/':
                if example[2] != '0':
                    decision = complex(example[0]) / complex(example[2])
                else:
                    bot.send_message(message.chat.id, 'На ноль делить нельзя')
                    controller(message)
            elif example[1] == '*':
                decision = complex(example[0]) * complex(example[2])
            bot.send_message(message.chat.id, f'{message.text} = {decision}')
        else:
            bot.send_message(message.chat.id, 'Вы ввели неверную операцию')
            controller(message)
    else:
        bot.send_message(message.chat.id, 'Вы ввели неверные значения')
        controller(message)


bot.infinity_polling()