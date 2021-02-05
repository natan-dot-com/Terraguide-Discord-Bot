import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
import requests
from multithreading_starter import *

URL = "https://terraria.gamepedia.com/"
STORAGE_PATH = GLOBAL_JSON_PATH + LIGHT_SOURCE_JSON_NAME_FILE
DATA_TO_BE_SCRAPPED = [SCRAPING_HOUSE, SCRAPING_MECHANISM, SCRAPING_WATERPROOF]
GENERAL_LIGHT_SOURCES = ["Torch", "Candle", "Candelabra", "Lantern", "Chandelier", "Lamps"]
newURL = URL + "Light_sources"
pageLightSources = requests.get(newURL)
soupLightSources = BeautifulSoup(pageLightSources.content, "html.parser")

itemList = LoadJSONFile(ITEM_FILE_PATH)
lightSourcesList = []

@start_threads_decorator(size=len(itemList), threads_number=8)
def lightSourcesScraping(init, fin, threadID):
    for itemInstance in itemList[init:fin]:
        if itemInstance[SCRAPING_TYPE] == "Light source":
            newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
            page = requests.get(newURL)
            soup = BeautifulSoup(page.content, "html.parser")
            print("Thread {}: Processing {} with ID {}".format(threadID, newURL, itemInstance[SCRAPING_ID]))
        
            tableBoxes = soup.find_all("div", class_="infobox item")
            tableBox = tableBoxes[0]
            for tableBoxTmp in tableBoxes:
                if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                    tableBox = tableBoxTmp

            lightSourceDict = get_statistics(tableBox, itemInstance=itemInstance)

            #shit code that doesn't work
            '''lightSourceDict.pop(SCRAPING_SOURCES)
            lightSourcesTables = soupLightSources.find_all("table", class_="terraria")[0:2]

            nowBreak = 0
            for lightSourcesTable in lightSourcesTables:
                lightSourcesRows = lightSourcesTable.find_all("tr")[1:]
                tableHeadColumns = lightSourcesTable.find_all("tr")[0].find_all("th")
                indexes = getTableColumns(tableHeadColumns, DATA_TO_BE_SCRAPPED)
                lightSourcesRowInstance = ""
                for lightSourcesRow in lightSourcesRows:
                    #print("{} == {}".format(lightSourcesRow.find("img")["alt"], itemInstance[SCRAPING_NAME]))
                    if lightSourcesRow.find("img")["alt"] == itemInstance[SCRAPING_NAME]:
                        nowBreak = 1
                        lightSourcesRowInstance = lightSourcesRow
                        break
                        
                if not nowBreak:
                    for lightSourcesRow in lightSourcesRows:
                        if lightSourcesRow.find("img")["alt"] in GENERAL_LIGHT_SOURCES:
                            newURL = URL + lightSourcesRow.find("img")["alt"]
                            pageLightSource = requests.get(newURL)
                            soupLightSource = BeautifulSoup(pageLightSource.content, "html.parser")
                            lightSourceTables = soupLightSource.find_all("table")
                            for lightSourceTable in lightSourceTables:
                                lightSourceRows = lightSourceTable.find_all("tr")
                                if not lightSourceRows:
                                    continue
                                for lightSourceRow in lightSourceRows[1:]:
                                    if lightSourceRow.find("img"):
                                        if lightSourceRow.find("img")["alt"] == itemInstance[SCRAPING_NAME]:
                                            lightSourcesRowInstance = lightSourceRow
                                            nowBreak = 1
                                            break
                                if nowBreak:
                                    break
                            if nowBreak:
                                break

                if nowBreak:
                    lightSourcesColumns = lightSourcesRowInstance.find_all("td")
                    for lightSourcesColumn, index in zip(lightSourcesColumns, range(0, len(lightSourcesColumns))):
                        for i in range(len(indexes)):
                            #print("{} == {}\n".format(tableHeadColumns[index].text.rstrip(), list(indexes.keys())[i]))
                            if tableHeadColumns[index].text.rstrip() == list(indexes.keys())[i]:
                                lightSourceDict[list(indexes.keys())[i]] = lightSourcesColumn.img["alt"]
                if nowBreak:
                    break


            lightSourceDict[SCRAPING_SOURCES] = SOURCE_SOURCES_DICT'''
            lightSourcesList.append(lightSourceDict)
              
SaveJSONFile(STORAGE_PATH, sortListOfDictsByKey(lightSourcesList, SCRAPING_ITEM_ID))