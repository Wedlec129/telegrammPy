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
TOKEN='1####g'

#получить число из сайта
def getChesloForhtml(teg,clas,htmlForChislo):
      # Ссылка на нужную страницу
      html = htmlForChislo
    	# Заголовки для передачи вместе с URL
      headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.#####1.149 Safari/537.36'}

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
     
  # addr_from = "###u"                 # Адресат
  # addr_to   = "#.com"                   # Получатель
  # password  = ####"                                  # Пароль

   addr_from = "#u"                 # Адресат
   addr_to   = komu                   # Получатель
   password  = "#####"                                  # Пароль

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

 
histoty=[]    
  
spamMeseng=[]

fostKomu=[]

@bot.message_handler(commands=['start'])  # если написали команду старт
def messengToStart(message):

   


  #создаём большие кнопки 
  markupBig = types.ReplyKeyboardMarkup(row_width=2)

  
  item2Big=types.InlineKeyboardButton("1) содержание спама")
  item3Big=types.InlineKeyboardButton("2) кому отправить (почта)")
  item1Big=types.InlineKeyboardButton("3) спам")

  markupBig.add(item2Big,item3Big,item1Big)

  #


  
  bot.send_message(message.chat.id,"привет <b>  "+message.from_user.first_name +" "+ message.from_user.last_name+"</b>  это Спам Бот"  ,parse_mode='html',reply_markup=markupBig)
  
  

 

  #тут проверям все сообщения(текст ) от пользователя
@bot.message_handler(content_types=['text'])
def otvet(message):
   if message.text == '3) спам':
            
            #создаём маленькие кнопочки к сообщению
             markup = types.InlineKeyboardMarkup(row_width=2)

             item1=types.InlineKeyboardButton("1", callback_data='spam1')
             item2=types.InlineKeyboardButton("5", callback_data='spam5')
             item3=types.InlineKeyboardButton("10", callback_data='spam10')
             markup.add(item1,item2,item3)

             bot.send_message(message.chat.id,"кому спамить : " +fostKomu[0])
             bot.send_message(message.chat.id,"что спамить : " +spamMeseng[0])

             bot.send_message(message.chat.id,"сколько спамить ?" ,reply_markup=markup)

   if message.text == '1) содержание спама':
        histoty.clear()
        histoty.append("spam")
        bot.send_message(message.chat.id,"введите текст для спама : " )

   if message.text!='1) содержание спама' and message.text!='2) спам'and message.text!='2) кому отправить (почта)' and histoty[0]=="spam" :
       
       spamMeseng.clear()
       spamMeseng.append(message.text)
       bot.send_message(message.chat.id,"замена текста для спама на : "+spamMeseng[0] )
       histoty[0]="w"
   
   if message.text == '2) кому отправить (почта)':
        histoty.clear()
        histoty.append("findPost")
        bot.send_message(message.chat.id,"введите почту для спама : " )  
           
   if message.text!='1) содержание спама' and message.text!='3) спам'and message.text!='2) кому отправить (почта)' and histoty[0]=="findPost" :
       
       fostKomu.clear()
       fostKomu.append(message.text)
       bot.send_message(message.chat.id,"замена почты на : "+fostKomu[0] )
       histoty[0]="w"
       
   
    


#тут проверям нажатия маленьких кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
            if call.data == 'spam1':
                
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=" (отправленно) ")
                #print(spamMeseng[0]+fostKomu[0])
                WriteToEMAIL(spamMeseng[0],fostKomu[0])
               

            if call.data == 'spam5':    
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=" (отправленно) ")
                for i in  range(5):
                   
                   
                    WriteToEMAIL(spamMeseng[0],fostKomu[0])

            if call.data == 'spam10':    
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=" (отправленно) ")
                for i in  range(10):
                    
                     
                     WriteToEMAIL(spamMeseng[0],fostKomu[0])





#run
bot.polling(none_stop=True) #бот активен 




