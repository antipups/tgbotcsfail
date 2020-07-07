import datetime
import re
import time
import telebot
import requests
from config import TOKEN, headers, orderer

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start', ])
def check_id(message):
    """
        Для того, чтоб узнать chat_id
    :param message:
    :return:
    """
    print(message)


def color(coef):
    """
        Какой кружок и букву выводим
    :param coef: сам коэфициент
    :return: котреж, первое это сам кружочек, второе, это буква
    """
    if 1 <= coef < 1.2:
        return '🔴', 'R'
    elif 1.2 <= coef < 2:
        return '🔵', 'B'
    elif 2 <= coef < 3:
        return '🟢', 'G'
    elif 3 <= coef < 5:
        return '🟣', 'P'
    elif 5 <= coef < 10:
        return '🟠', 'O'
    else:
        return '🟡', 'Y'


def parse(number_game):
    """
        Бесконечный цикл на проверку новых данных, с проверкой интернета, чтоб не было краша
    :param number_game:
    :return:
    """
    while True:
        try:
            result = requests.get(f'https://api.cs.fail/crash/get-game/{number_game}', headers=headers).text
        except:
            time.sleep(5)
            continue
        if result != '{"error_code":-1,"error_text":"Game not found"}':
            number_game += 1
            coef = round(float(re.search(r'crashed_at":\d{0,10}(\.[^,]*)?', result).group()[12:]), 2)
            time_for_mess = re.search(r'start_at":\d{0,20}', result).group()[10:]
            time_for_mess = time_for_mess[:-3] + '.' + time_for_mess[-3:]
            time_for_mess = (datetime.datetime.fromtimestamp(float(time_for_mess)) + datetime.timedelta(hours=3)).strftime('%H:%M %d.%m.%Y')
            color_for_mess = color(coef)
            result_message = color_for_mess[0] + ' K=' + str(coef).replace('.', '_') + ' ' + time_for_mess
            result_message += f'\n#{color_for_mess[1]} #K{str(coef).replace(".", "_")} #T{time_for_mess[:time_for_mess.find(" ")].replace(":", "")} #D{time_for_mess[time_for_mess.find(" ") + 1:].replace(".", "_")}'
            bot.send_message(chat_id=orderer, text=result_message, disable_notification=True)
            with open('1.txt', 'w') as f:
                f.write(str(number_game))
        time.sleep(3)


if __name__ == '__main__':
    # bot.infinity_polling()
    with open('1.txt', 'r') as f:
        parse(int(f.read()))
