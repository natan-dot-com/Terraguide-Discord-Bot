#

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
import requests
import threading
import math

ITEMS_BLOCK_PATH = GLOBAL_JSON_PATH + "items_furnitures.json"
URL = "https://terraria.gamepedia.com/"
BRICKS_IMAGE_PATH = "data_scraping/bricks_img/{}.png"

log = open("log.txt", "w")
itemList = LoadJSONFile(ITEM_FILE_PATH)
furnituresList = []

class myThread (threading.Thread):
   def __init__(self, threadID, init, fin):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.init = init
      self.fin = fin
   def run(self):
      print ("Starting Thread " + str(self.threadID))
      furniture_scraping(self.init, self.fin)
      log.write("Exiting Thread" + str(self.threadID) + "\n")
      print ("Exiting Thread " + str(self.threadID))

def furniture_scraping(init, fin):
    for itemInstance in itemList[init:fin]:
        if itemInstance[SCRAPING_TYPE] == "Furniture":
            newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
            page = requests.get(newURL)
            soup = BeautifulSoup(page.content, "html.parser")
            print("processing {}".format(newURL))

            tableBoxes = soup.find_all("div", class_="infobox item")
            tableBox = tableBoxes[0]
            for tableBoxTmp in tableBoxes:
                if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                    tableBox = tableBoxTmp
            furnituresList.append(get_statistics(tableBox, itemInstance=itemInstance))

    SaveJSONFile(ITEMS_BLOCK_PATH, furnituresList)



first_quarter = math.floor(len(itemList)/4)
second_quarter = math.floor(len(itemList)/2)
third_quarter = 3*math.floor((len(itemList)/4))
fouth_quarter = math.floor(len(itemList))

print("First: {} to {}".format(0, first_quarter))
print("First: {} to {}".format(first_quarter+1, second_quarter))
print("First: {} to {}".format(second_quarter+1, third_quarter))
print("First: {} to {}".format(third_quarter+1, fouth_quarter))

# Create new threads
thread1 = myThread(1, 0, first_quarter)
thread2 = myThread(2, first_quarter, second_quarter)
thread3 = myThread(3, second_quarter, third_quarter)
thread4 = myThread(4, third_quarter, fouth_quarter)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()