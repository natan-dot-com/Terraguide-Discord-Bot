import json
import os
from bs4 import BeautifulSoup
import bs4
import requests 
import threading
import math

sucessful = 200
src_prefix = "img/"

url = "https://terraria.gamepedia.com/"

log_file = 'img_log.txt'

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, item_list, init, fin):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.item_list = item_list
      self.init = init
      self.fin = fin
   def run(self):
      print ("Starting Thread " + str(self.threadID))
      img_search(self.item_list, self.init, self.fin)
      print ("Exiting Thread " + str(self.threadID))

def img_search(item_list, init, fin):
    print("entrou")
    for item in item_list[init:fin]:

        new_url = url + item['name'].replace(" ", "_")

        page = requests.get(new_url)
        if page.status_code == sucessful:
            
            soup = BeautifulSoup(page.content, 'html.parser')
            item_img = soup.find("div", class_="section images")
            
            if type(item_img) is bs4.element.Tag:
                #find tag
                img = item_img.find("img")

                #get the src link
                img_src = img['src']
                print(img_src)

                #img path
                img_path = src_prefix + item['name'].replace(" ", "_") + ".png"

                #get the image
                img_output = requests.get(img_src, stream=True)
                #print(type(img_output))
                if img_output.ok:
                    with open(img_path, 'wb') as handler:
                        for block in img_output.iter_content(1024):
                            if not block:
                                break
                            handler.write(block)
                else:
                    with open(log_file, "a") as log:
                        log.write("Image not found with ID " + str(item['id']) + "\n")
                #exit(0)
            else:
                with open(log_file, "a") as log:
                    log.write("Image not found with link " + new_url + " and ID " + str(item['id']) + "\n")

    
with open('json/items2.json') as items:
    item_list = json.load(items)

if os.path.exists(log_file):
  os.remove(log_file)

first_quarter = math.floor(len(item_list)/4)
second_quarter = math.floor(len(item_list)/2)
third_quarter = 3*math.floor((len(item_list)/4))
fouth_quarter = math.floor(len(item_list)/4)

# Create new threads
thread1 = myThread(1, item_list, 0, first_quarter)
thread2 = myThread(2, item_list, first_quarter + 1, second_quarter)
thread3 = myThread(3, item_list, second_quarter + 1, third_quarter)
thread4 = myThread(4, item_list, third_quarter + 1, fouth_quarter)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()