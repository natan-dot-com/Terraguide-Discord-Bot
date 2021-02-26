# Load 3-level parent directories
from importlib import import_module
import path_manager
if __name__ == '__main__' and __package__ == None:
    __package__ = path_manager.importParents(level=3)
    import_module(__package__)

# Setting the root directory as working directory for Linux systems
from platform import system
from pathlib import Path
import os
executionOS = system()
if executionOS == "Linux":
    os.chdir("../../")

from ...utility_tools.scraping_tools import *
from ...utility_tools.json_manager import *
from ...utility_tools.multithreading_starter import *
from bs4 import BeautifulSoup
import requests

VANITY_PATH = GLOBAL_JSON_PATH + VANITY_NAME_FILE + JSON_EXT
URL = "https://terraria.gamepedia.com/"

itemList = LoadJSONFile(GLOBAL_JSON_PATH + MAIN_NAME_FILE + JSON_EXT)
vanitiesList = []

@start_threads_decorator(size=len(itemList), threads_number=8)
def vanityScraping(init, fin, threadID):
    for itemInstance in itemList[init:fin]:
        if itemInstance[SCRAPING_TYPE] == "Vanity":
            newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
            page = requests.get(newURL)
            soup = BeautifulSoup(page.content, "html.parser")
            print("Thread {}: Processing {} with ID {}".format(threadID, newURL, itemInstance[SCRAPING_ID]))

            tableBoxes = soup.find_all("div", class_="infobox item")
            tableBox = tableBoxes[0]
            for tableBoxTmp in tableBoxes:
                if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                    tableBox = tableBoxTmp

            vanitiesList.append(get_statistics(tableBox, itemInstance=itemInstance))

SaveJSONFile(VANITY_PATH, sortListOfDictsByKey(vanitiesList, SCRAPING_ITEM_ID))
