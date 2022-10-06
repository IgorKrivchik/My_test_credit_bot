from email.message import Message
import smtplib
import telebot
from telebot import types
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from re import *

 #создаем бота и назначаем токен
bot = telebot.TeleBot("5597293633:AAG4TN0PSvWbI93fvZdMN3enC3WsXre4__s")
 
# Указываем какой текст мы будем ждать от бота, все остальное будет вызывать сообщение 'Данные введены неверно'
status = ["кредит", "рассрочка", "лизинг",
          'кредит на автоприцеп', 'кредит на трактор', 'кредит на мотоблок', 'карты рассрочки', 'рассрочка от магазина',
          'расчитать на 12 месяцев', 'расчитать на 18 месяцев', 'расчитать на 24 месяца', 'расчитать на 36 месяцев','расчитать на 48 месяцев',
          'расчитать на другой срок кредитования']
 
inc_type = []  # Хранит в себе тип заявки
cli_num = []  # Хранит в себе номер телефона заявителя
cli_mail = []  # Хранит в себе почту заявителя
hello_count = []  # Хранит в себе данные о том нужно ли здороваться с пользователем
 
 
# Основной хендлер который реагирует на команду страт
@bot.message_handler(commands=['start'])
def statup(message):  # Здороваемся и просим ввести номер или почту
    key1 = types.ReplyKeyboardMarkup(True, False)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    key1.row(button_phone)
    key1.row('Ввести почту для обратной связи')
    key1.one_time_keyboard = True
    if len(hello_count) == 0:  # Проверяем здоровались ли мы ранее
        bot.send_message(message.chat.id,
                         "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный для подбора кредитных продуктов."
                         " Отправте свой номер телефона или почту, чтоб начать работу ".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=key1)
 
    elif message.text == 'Главное меню':
        pre_main(message)
 
    else:
        bot.send_message(message.chat.id,
                         "Выберете средство для обратной связи, чтоб начать работу ".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=key1)
    hello_count.insert(1, 1)  # Отмечаем факт приветствия
 
 
@bot.message_handler(content_types=['text', 'contact'])  # Основной обработчик
def phone_check(message):  # Уточняем у пользователя чем он с нами поделиться
    if message.text == None:  # Если пользователь нажал кнопку "Поделиться контактом" то текс будет None
        if message.contact.user_id == message.chat.id:  # Проверяем свой ли контакт дал пользователь
            cli_num.append(message.contact.phone_number)
            pre_main(message)
        else:
            bot.send_message(message.chat.id, 'Введите правильный номер телефона!')
            statup(message)
    elif message.text == "Ввести почту для обратной связи":  # Перекидывает на ввод почты
        mail_check(message)
    elif message.text == 'Главное меню':
        pre_main(message)
    else:
        statup(message)
 
 
def mail_check(message):  # Функция ввода почты
    key1 = telebot.types.ReplyKeyboardMarkup(True, False)
    key1.row("Проверить")
    bot.send_message(message.chat.id, 'Введите вашу почту')
    if message.text == 'Ввести почту для обратной связи':
        bot.register_next_step_handler(message, mail_check2)
    elif message.text == 'Главное меню':
        pre_main(message)
 
 
def mail_check2(message):  # Проверка потчы на валидность
    pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')  # Проверяем совпадает ли паттерн
    is_valid = pattern.match(message.text)
    if is_valid:
        cli_mail.append(message.text)  # Записываем полученную почту
        pre_main(message)
    elif message.text == 'Главное меню':
        pre_main(message)
    else:
        bot.send_message(message.chat.id, "Почта введена неверно.")
        statup(message)
 
 
def pre_main(message):  # Основная функция
    inc_type.clear()  # Очищаем словарь с типом заявки
    key = types.ReplyKeyboardMarkup(True, False)
    key.row('кредит')
    key.row('рассрочка')
    key.row('лизинг')
    key.one_time_keyboard = True
    # Спрашиваем что за инцент
    bot.send_message(message.chat.id,
                         "Итак, {0.first_name}!, выберите продукт который Вас заинтересовал.".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=key)
    print('No problem detected. Message send')
    bot.register_next_step_handler(message, main)
 
 
def main(message):  # Определяем тип инцидента и уточняем его подтип
    if message.text == 'кредит':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('кредит на мотоблок')
        keyboard.row('кредит на трактор')
        keyboard.row('кредит на автоприцеп')
        keyboard.row('Главное меню')
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard)
        bot.register_next_step_handler(message, incedent)
    elif message.text == 'рассрочка':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('карты рассрочки') 
        keyboard.row('банковская рассрочка')
        keyboard.row('рассрочка от магазина')
        keyboard.row('Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Выберите интересующую Вас рассрочку, которой вы хотели бы воспользоваться', reply_markup=keyboard)
        bot.register_next_step_handler(message, info)

    elif message.text == 'лизинг':
        task = message.text
        vvod(message)
        bot.send_message(message.chat.id,
        "Итак, {0.first_name}!, поскольку лизинговые уловия подбираются индивидуально для каждого клиента, в ближайшее время с Вами свяжется наш менеджер.".format(
        message.from_user, bot.get_me()),
        parse_mode='html')
      
    elif message.text == ' Главное меню':
        pre_main(message)
 
    else:
        bot.send_message(message.chat.id, 'Данные введены неверно')
        pre_main(message)
 
 
def incedent(message):  # Обрабатываем подтип инцедента
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.add('Главное меню')
 
    if message.text == 'кредит на мотоблок':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('расчитать на 12 месяцев')
        keyboard.row('расчитать на 18 месяцев')
        keyboard.row('расчитать на 24 месяца')
        keyboard.row('расчитать на другой срок кредитования')
        keyboard.add('Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Выберите пожалуйста на какой срок вы бы хотели получить расчет кредита', reply_markup=keyboard)
        bot.register_next_step_handler(message, vvod)
 
    elif message.text == 'кредит на трактор':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('расчитать на 24 месяца')
        keyboard.row('расчитать на 36 месяцев')
        keyboard.row('расчитать на 48 месяцев')
        keyboard.add('Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Выберите пожалуйста на какой срок вы бы хотели получить расчет кредита', reply_markup=keyboard)
        bot.register_next_step_handler(message, vvod)
 
    elif message.text == 'кредит на автоприцеп':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('расчитать на 12 месяцев')
        keyboard.row('расчитать на 18 месяцев')
        keyboard.row('расчитать на 24 месяца')
        keyboard.add('Главное меню')
        keyboard.one_time_keyboard = True
        bot.send_message(message.chat.id, 'Выберите пожалуйста на какой срок вы бы хотели получить расчет кредита', reply_markup=keyboard)
        bot.register_next_step_handler(message, vvod)
 
    elif message.text == 'Главное меню':
        pre_main(message)
 
    else:
        bot.send_message(message.chat.id, 'Данные введены неверно')
        pre_main(message)
 
 
def info(message):  # Обработываем подтип запроса информации
    if message.text == 'Главное меню':
        pre_main(message)
    elif message.text == 'карты рассрочки':
        global task
        task = message.text
        vvod(message)
    elif message.text == 'банковская рассрочка':
        task = message.text
        vvod(message)
    elif message.text == 'рассрочка от магазина':
        task = message.text
        vvod(message)
    else:
        text(message)
        bot.send_message(message.chat.id, 'Данные введены неверно')
        pre_main(message)
 
 
def vvod(message):  # Запрашиваем дополнительную информацию
    inc_type.append(message.text)
    global task
    if message.text in status:
        task = message.text
        bot.send_message(message.chat.id, 'Введите сумму первоначального взноса ЦИФРАМИ, если он будет, если нет то поставьте 0 в строку ввода 😊')
        bot.register_next_step_handler(message, text)
    else:
        bot.send_message(message.chat.id, 'Данные введены неверно')
        pre_main(message)
 
 
def text(message):  # Отправляем письмо
    if message.text == 'Главное меню':
        pre_main(message)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Главное меню')
        bot.send_message(message.chat.id, 'Ваше запрос \"' + message.text +
                         '\" получен. Можете вернуться в главное меню ', reply_markup=keyboard)
        addr_from = "mail@gmail.com"
        addr_to = "mail@gmail.com"
        password = "password"
        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = ("$$$" + message.text)
        body = (f'''
      Автор заявки {message.from_user.first_name},{message.from_user.last_name},
 
      Телефон {cli_num}
 
      Тип заявки: {inc_type},
 
      Текст заявки: {message.text}
      ''')
        msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)  # Создаем объект SMTP
        smtpObj.starttls()  # Начинаем шифрованный обмен по TLS
        smtpObj.login(addr_from, password)  # Получаем доступ
        smtpObj.send_message(msg)  # Отправляем сообщение
        smtpObj.quit()  # Выходим
 
 
while True:  # Запускаем бота
    try:
        bot.polling(none_stop=True)
    except OSError:
        bot.polling(none_stop=True)