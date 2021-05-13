#!usr/bin/python
# -*- coding: utf-8 -*-

import os
from threading import Timer,Thread,Event
import requests
import random
import json
from ImageParser import YandexImage

token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # токен администратора

# Токен администратора можно взять тут: 
# https://vkhost.github.io/

group_id = 000000000 # id группы

p_timer_h = 0 # Задержка между публикациями в часах
p_timer_m = 1 # Задержка между публикациями в минутах

publish_img = 5 # картинок публиковать в 1 посте| максимум 10

list_search = [
	"пример 1", 
	"пример 2", 
	"пример 3", 
	"пример 4", 
	"пример 5"] # список запросов для yandex, указывайте в "" через запяту

yandex_or_image = "yandex" # yandex - картинки из инета по запросам; image - картинки из папки img


print("Bot is Start")

parser = YandexImage()

xl = 0

id = str('-'+str(group_id))

p_timer = ((p_timer_h * 60 * 60) + (p_timer_m * 60))

try:
	files = os.listdir("img")
except:
	os.mkdir("img")

class post_timer():

   def __init__(self,t,hFunction):
      self.t = t
      self.hFunction = hFunction
      self.thread = Timer(self.t, self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t, self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def get_link(message, attachments):
  api_url = 'https://api.vk.com/method/wall.post?owner_id='+id+'&from_group=1&access_token='+token+'&message='+message+'&attachments='+attachments+'&v=5.126'
  return api_url

def getWallUploadServer():
  r = requests.get('https://api.vk.com/method/photos.getWallUploadServer?', params = {'access_token':token,
                                      'group_id':group_id,
                                      'v':'5.101'}).json() 																															
  return r['response']['upload_url']

def save_r():
      save_result = requests.get('https://api.vk.com/method/photos.saveWallPhoto?', params ={'access_token':token,
                                            'group_id':group_id,
                                            'photo':upload_response['photo'],
                                            'server':upload_response['server'],
                                            'hash':upload_response['hash'],
                                            'v':'5.101'}).json()
      return ('photo'+str(save_result['response'][0]['owner_id'])+'_'+str(save_result['response'][0]['id']))

def post_yandex_main():
  global xl
  x = 1
  upload_url = getWallUploadServer()
  list_url = []
  list_photo_vk = []
  for item in parser.search(random.choice(list_search)):
  	list_url.append(item.url)

  for iturl in list_url:
  	p = requests.get(iturl)
  	out = open(f"img/img{x}.jpg", "wb")
  	out.write(p.content)
  	out.close()
  	x += 1
  	if x == (publish_img + 1):
  		break
  	
  x = 1
  for i in range(publish_img):
  	file = {'file1': open(f'img/img{x}.jpg', 'rb')}
  	global upload_response
  	upload_response = requests.post(upload_url, files=file).json()
  	save_result = save_r()
  	list_photo_vk.append(save_result + ", ")
  	x += 1

  file = ''
  full_data = ' '.join(list_photo_vk)

  req = requests.get(get_link('', full_data)).json()

  os.remove("img/img1.jpg")
  os.remove("img/img2.jpg")
  os.remove("img/img3.jpg")
  os.remove("img/img4.jpg")
  os.remove("img/img5.jpg")

  xl += 1
  if xl == 20:
  	xl = 0

def post_image_main():
  upload_url = getWallUploadServer()
  list_photo_vk = []
  list_image_vk = []

  x = 0
  for i in range(publish_img):
  	file = {'file1': open(f'img/{files[x]}', 'rb')}
  	global upload_response
  	upload_response = requests.post(upload_url, files=file).json()
  	save_result = save_r()
  	list_photo_vk.append(save_result + ", ")
  	list_image_vk.append(files[x])
  	x += 1
  
  x = 0
  for i in range(publish_img):
  	os.remove(f"img/{list_image_vk[x]}")
  	x += 1

  file = ''
  full_data = ' '.join(list_photo_vk)

  eq = requests.get(get_link('', full_data)).json()


if __name__ == '__main__':
  if yandex_or_image == "yandex":
    timer_for_posts = post_timer(p_timer, post_yandex_main)
    timer_for_posts.start()
  elif yandex_or_image == "image":
    timer_for_posts = post_timer(p_timer, post_image_main)
    timer_for_posts.start()
  else:
    print("Переменая yandex_or_image указана не верно!")