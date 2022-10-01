from __future__ import print_function

import os
import os.path
import telebot
import time

from telebot import types
from aiogram import Bot, executor, Dispatcher

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

Flag = False

TOKENBOT = '5734355729:AAFHRCEwQvtRyk8lviwh3iUN13G7-ktaoBQ'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
bot = telebot.TeleBot(TOKENBOT)

SAMPLE_SPREADSHEET_ID = '1HNt7XVWEGwLrmAum8PrkdxD5NIvNUeTY0uw1Yq7CVog'

SAMPLE_RANGE_NAME_VIDIO = 'List1!A2:A100'
SAMPLE_RANGE_NAME_ADIIT = 'List1!B2:B100'
bote = Bot(TOKENBOT)


def main():
    creds = None
    list_vidio = []
    list_addit = []

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()

        result1 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range = SAMPLE_RANGE_NAME_VIDIO).execute()
        result2 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range = SAMPLE_RANGE_NAME_ADIIT).execute()

        values1 = result1.get('values', [])
        values2 = result2.get('values', [])

        for row in values1:
            list_vidio.append(row[0])

        for row in values2:
            list_addit.append(row[0])

    except HttpError as err:
        print(err)
    return(list_vidio, list_addit)


if __name__ == '__main__':
    main()


list_vidio, list_addit = main()


@bot.message_handler(commands=['start'])
def startbot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Видеоматериалы")
    button2 = types.KeyboardButton("Доп.Материалы")

    markup.add(button1, button2)

    bot.send_message(message.chat.id, "Приветствую, что вам нужно?",reply_markup=markup)


@bot.message_handler(content_types=['text'])
def info(message):
    if message.chat.type == 'private':
        if message.text == "Видеоматериалы":
            j = 'Видеометериалы' + '\n'
            for i in range(len(list_vidio)):
                j += str(i+1) + ') ' + str(list_vidio[i]) + '\n'
            bot.send_message(message.chat.id, j)

        elif message.text == 'Доп.Материалы':
            d = 'Доп.Материалы' + '\n'
            for g in range(len(list_addit)):
                d += str(g + 1) + ') ' + str(list_addit[g]) + '\n'
            bot.send_message(message.chat.id, d)
    timer_set(message)


def timer_set(message):
    global Flag

    if Flag == False:

        bot.send_message(message.chat.id, "Установите таймер отправки напоминаний в секундах")
        numb = message.text

        if numb == int:
            tim = int(numb)
            Flag = True
            timer(tim, message)


def timer(tim, message):
    time.sleep(tim)
    bot.send_message(message.chat.id, "Не хотите продолжить обучение?")
    timer(tim, message)


bot.polling(non_stop=True)