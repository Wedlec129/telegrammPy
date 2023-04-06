#телеграмм
import telebot
from telebot import types

#для звука
import pyttsx3
import speech_recognition as sr

#для парчинга
import requests 
from bs4 import BeautifulSoup as BS

import time
import sys
import os

import smtplib
from configparser import ConfigParser
# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML
from email.mime.image import MIMEImage              # Изображения


#ключ для бота
TOKEN='###'

#получить число из сайта
def getChesloForhtml(teg,clas,htmlForChislo):
      # Ссылка на нужную страницу
      html = htmlForChislo
    	# Заголовки для передачи вместе с URL
      headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.####.149 Safari/537.36'}

      full_page = requests.get(html, headers=headers)

      soup = BS(full_page.content, 'html.parser')

      convert = soup.findAll(teg, {"class": clas}) #тег классы и какие то значения 

      return( convert[0].text)

#произнисти голосом компа
def say(watSay):
    #можно говорить
    PC= pyttsx3.init()

    print(watSay)

    PC.say(watSay)


    PC.runAndWait() #начать говорить

#записать число в файл
def writeToFile(watWrite):
    putyToFail="C:/Users/Борис/Desktop/qw1.txt"
    with open(putyToFail,"w") as file:
       file.write(watWrite)

       print("текст в файле изменён")

#написать сообщение на почту
def WriteToEMAIL(text):
     
   addr_from = "###u"                 # Адресат
   addr_to   = "###om"                   # Получатель
   password  = "p####word"                                  # Пароль

   msg = MIMEMultipart()                               # Создаем сообщение
   msg['From']    = addr_from                          # Адресат
   msg['To']      = addr_to                            # Получатель
   msg['Subject'] = ''                   # Тема сообщения

   body = text
   msg.attach(MIMEText(body, 'plain'))                 # Добавляем в сообщение текст

   
   server = smtplib.SMTP_SSL('smtp.mail.ru', 465)           # Создаем объект SMTP
  
   try:
    server.login(addr_from, password)                   # Получаем доступ

    server.send_message(msg)                            # Отправляем сообщение
    server.quit()                                       # Выходим

    print("письмо отправленно")
   except:
       print("Ошибка ПОЧТЫ : неверный логин или пароль")





kurs=getChesloForhtml("div","currency-table__large-text","https://www.banki.ru/products/currency/eur/");  
#writeToFile(kurs)
#say("курс евро :"+kurs)
#WriteToEMAIL("привет "+kurs)



bot=telebot.TeleBot(TOKEN) # создаём бота и привязываем ключ

@bot.message_handler(commands=['start'])  # если написали команду старт
def messengToStart(message):

    #создаём маленькие кнопочки к сообщению
  markup = types.InlineKeyboardMarkup(row_width=2)

  item1=types.InlineKeyboardButton("ютуб", url="https://www.youtube.com/?gl=RU&hl=ru")
  item2=types.InlineKeyboardButton("что то", url="https://metanit.com/cpp/tutorial/5.14.php")
  item3=types.InlineKeyboardButton("кнопка good", callback_data='good')
  item4=types.InlineKeyboardButton("уведомление", callback_data='sms')

  markup.add(item1,item2,item3,item4)
  #


  #создаём большие кнопки 
  markupBig = types.ReplyKeyboardMarkup(row_width=2)

  item1Big=types.InlineKeyboardButton("евро")
  
  markupBig.add(item1Big)

  #


  #сообщение привет + маленькие кнопкм(к сообщениям)
  bot.send_message(message.chat.id,"привет <b>  "+message.from_user.first_name +" "+ message.from_user.last_name+"</b>  это WedlecBot. его <a href='https://vk.com/wedlec129'> автор </a>"  ,parse_mode='html',reply_markup=markup)
  
  #сообщение + клавиаутрные кнопки

  photo='https://sun1-87.userapi.com/zB8ter8zhVnPiBeRykJOEeijF1S-KmylvpQHMw/561VegVaA8Q.jpg'
  bot.send_photo(message.chat.id, photo)

  bot.send_message(message.chat.id,"igel",reply_markup=markupBig)
  

       
  
  #тут проверям все сообщения(текст ) от пользователя
@bot.message_handler(content_types=['text'])
def otvet(message):
   if message.text == 'евро':
            bot.send_message(message.chat.id,"евро : "+kurs )
   
    


#тут проверям нажатия маленьких кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
                

            if call.data == 'sms':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
               



#run
bot.polling(none_stop=True) #бот активен 


