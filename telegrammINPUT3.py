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
TOKEN='#########'

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
def PcSay(watSay):
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
def WriteToEMAIL(text,komu):
     
  # addr_from = "s#######u"                 # Адресат
  # addr_to   = "######com"                   # Получатель
  # password  = "h###"                                  # Пароль

   addr_from = "#3###"                 # Адресат
   addr_to   = komu                   # Получатель
   password  = "####"                                  # Пароль

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




#kurs=getChesloForhtml("div","currency-table__large-text","https://www.banki.ru/products/currency/eur/");  
#writeToFile(kurs)
#say("курс евро :"+kurs)



bot=telebot.TeleBot(TOKEN) # создаём бота и привязываем ключ

class WeShisloForTelegramm:
    a=[0]
    history=["0"]

    def addInHistoty(self,tipHistory):
        #запоминаем в историю
      
      self.history.append(tipHistory)

    def input(self,sms,tipHistory):

      return self.history[len(self.history)-1]==tipHistory and sms != tipHistory
      
        

    def set(self,sms):
        self.a.append(sms)
        self.history.append("0")

    def get(self):
        return self.a[len(self.a)-1]

    def clearHistory(self):
       self.history.clear()
       self.history.append("0")


@bot.message_handler(commands=['start'])  # если написали команду старт
def messengToStart(message):

   


  #создаём большие кнопки 
  markupBig = types.ReplyKeyboardMarkup(row_width=2)

  
  item2Big=types.InlineKeyboardButton("set a")
  item3Big=types.InlineKeyboardButton("get a")
 

  markupBig.add(item2Big,item3Big)

  #


  
  bot.send_message(message.chat.id,"привет <b>  "+message.from_user.first_name +" "+ message.from_user.last_name+"</b>  это Спам Бот"  ,parse_mode='html',reply_markup=markupBig)

  # создаём число для ввода
a=WeShisloForTelegramm()
 

  #тут проверям все сообщения(текст ) от пользователя
@bot.message_handler(content_types=['text'])
def otvet(message):

    #если сбрасываем a
   if message.text == 'set a':
      bot.send_message(message.chat.id,"set a ")

      # добавляем в историю с конкретным именим
      a.addInHistoty('set a')
     
      #вводим а через сообщение  если история ==set a
   if a.input(message.text,'set a'):

       a.set(message.text)

       bot.send_message(message.chat.id,"a = "+a.get())

   if message.text == 'get a':
             bot.send_message(message.chat.id,"get a : "+str(a.get()))
             a.clearHistory() #очищаем историю




bot.polling(none_stop=True) #бот активен 
