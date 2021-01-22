NOT_FOUND = -1

class hashTable:
    def __init__(self, tableSize, stringDictIndex):
        self.size = tableSize
        self.dictIndex = stringDictIndex
        self.data = [None] * self.size
        
    def hashFunction(self, stringData):
        hashValue = 0
        counter = 1
        for charInstance in stringData:
            hashValue += counter * ord(charInstance)
            counter += 1
            
        return hashValue % self.size
        
    def rehashFunction(self, oldValue, rehashCounter):
        return (oldValue + rehashCounter ** 2) % self.size
        
    def hashString(self, stringData, stringDict):
        hashIndex = self.hashFunction(stringData)
        
        if self.data[hashIndex] == None:
            self.data[hashIndex] = stringDict
            return
        else:
            rehashCounter = 1
            nextIndex = self.rehashFunction(hashIndex, rehashCounter)
            while self.data[nextIndex] != None:
                rehashCounter += 1
                nextIndex = self.rehashFunction(hashIndex, rehashCounter)
            if self.data[nextIndex] == None:
                self.data[nextIndex] = stringDict
                return
        
    def dehashString(self, stringData, dictIndexToReturn):
        hashIndex = self.hashFunction(stringData)
        
        if (self.data[hashIndex] != None):
            if self.data[hashIndex][self.dictIndex] == stringData:
                return self.data[hashIndex][dictIndexToReturn] 
            else:
                rehashCounter = 1
                nextIndex = self.rehashFunction(hashIndex, rehashCounter)
                while (self.data[nextIndex] != None) and (self.data[nextIndex][self.dictIndex] != stringData):
                    rehashCounter += 1
                    nextIndex = self.rehashFunction(hashIndex, rehashCounter)
                if self.data[nextIndex] == None:
                    return NOT_FOUND
                elif self.data[nextIndex][self.dictIndex] == stringData:
                    return self.data[nextIndex][dictIndexToReturn]
        else:
            return NOT_FOUND
