import datetime
import re
import time
import telebot
import requests
from config import TOKEN, headers, orderer, my_chat_id

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start', ])
def check_id(message):
    print(message)


def color(coef):
    if 1 < coef <= 1.2:
        return '🔴', 'R'
    elif 1.2 < coef <= 1.5:
        return '🔵', 'B'
    elif 1.5 < coef <= 2.5:
        return '🟢', 'G'
    elif 2.5 < coef <= 4.5:
        return '🟣', 'P'
    elif 4.5 < coef <= 10:
        return '🔵', 'B'
    else:
        return '🟡', 'Y'


def parse(number_game):
    while True:
        result = requests.get(f'https://api.cs.fail/crash/get-game/{number_game}', headers=headers).text
        if result != '{"error_code":-1,"error_text":"Game not found"}':
            number_game += 1
            coef = re.search(r'crashed_at":\d{0,10}(\.\d{0,2})?', result).group()[12:]
            time_for_mess = re.search(r'start_at":\d{0,20}', result).group()[10:]
            time_for_mess = time_for_mess[:-3] + '.' + time_for_mess[-3:]
            time_for_mess = datetime.datetime.fromtimestamp(float(time_for_mess)).strftime('%H:%M %d.%m.%Y')
            color_for_mess = color(float(coef))
            result_message = color_for_mess[0] + ' K=' + coef.replace('.', '_') + ' ' + time_for_mess
            result_message += f'\n#{color_for_mess[1]} #K{coef.replace(".", "_")} #T{time_for_mess[:time_for_mess.find(" ")].replace(":", "")} #D{time_for_mess[time_for_mess.find(" ") + 1:].replace(".", "_")}'
            bot.send_message(chat_id=my_chat_id, text=result_message, disable_notification=True)
            with open('1.txt', 'w') as f:
                f.write(str(number_game))
        time.sleep(3)


if __name__ == '__main__':
    # bot.infinity_polling()
    with open('1.txt', 'r') as f:
        parse(int(f.read()))
