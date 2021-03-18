from .json_labels import *

SUCCESS = 0
NOT_FOUND = -1
FULL_TABLE = -2
EMPTY_TABLE = -3

ITEMS_HASH_SIZE = 8192
TABLES_HASH_SIZE = 128
NPC_HASH_SIZE = 1024
SET_HASH_SIZE = 256

class hashTable:
    def __init__(self, tableSize, stringDictIndex, caseSensitive="no"):
        self.sensitive = caseSensitive
        self.dictIndex = stringDictIndex
        self.size = tableSize
        self.inserted = 0
        self.data = [None] * self.size

    # Private functions to hash/rehash (if needed) each string
    def __hashFunction(self, stringData):
        hashValue = 0
        counter = 1
        lowerString = stringData.lower()

        for charInstance in lowerString:
            hashValue += counter * ord(charInstance)
            counter += 1

        return hashValue % self.size

    def __rehashFunction(self, oldValue, rehashCounter):
        return (oldValue + (rehashCounter ** 2)) % self.size

    # Public function to add a dictionary in data list
    def add(self, stringData, stringDict):
        if self.inserted == self.size:
            print("Hash table is already full. Aborted.")
            return FULL_TABLE

        lowerString = stringData.casefold()
        hashIndex = self.__hashFunction(lowerString)

        if self.data[hashIndex] == None:
            self.data[hashIndex] = stringDict
            self.inserted += 1
            return SUCCESS
        else:
            rehashCounter = 1
            nextIndex = self.__rehashFunction(hashIndex, rehashCounter)
            while self.data[nextIndex] != None:
                rehashCounter += 1
                nextIndex = self.__rehashFunction(hashIndex, rehashCounter)
            if self.data[nextIndex] == None:
                self.data[nextIndex] = stringDict
                self.inserted += 1
                return SUCCESS

    # Public function to search a dictionary from a string
    def search(self, stringData, dictIndexToReturn):
        if self.inserted == 0:
            print("Hash table is empty. Aborted.")
            return EMPTY_TABLE

        lowerString = stringData.lower()
        hashIndex = self.__hashFunction(lowerString)

        if self.data[hashIndex] != None:
            if self.data[hashIndex][self.dictIndex].lower() == lowerString:
                return self.data[hashIndex][dictIndexToReturn]
            else:
                rehashCounter = 1
                nextIndex = self.__rehashFunction(hashIndex, rehashCounter)
                while (self.data[nextIndex] != None) and (self.data[nextIndex][self.dictIndex].lower() != lowerString):
                    rehashCounter += 1
                    nextIndex = self.__rehashFunction(hashIndex, rehashCounter)
                if self.data[nextIndex] == None:
                    return NOT_FOUND
                elif self.data[nextIndex][self.dictIndex].lower() == lowerString:
                    return self.data[nextIndex][dictIndexToReturn]
        else:
            return NOT_FOUND

def initializeHashTable(hashTableStructure, infoList):
    if isinstance(hashTableStructure, hashTable):
        for infoInstance in infoList:
            hashTableStructure.add(infoInstance[hashTableStructure.dictIndex], infoInstance)

        if hashTableStructure.inserted == 0:
            print("Empty list was detected. Hash table will be also empty.")

        return hashTableStructure

