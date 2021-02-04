import threading
import math
import sys
import importlib

#log = open("log.txt", "w")

class myThread (threading.Thread):
   def __init__(self, threadID, file_name, function_name, init, fin):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.init = init
      self.fin = fin
      self.import_scraping = importlib.import_module(file_name, function_name)
      self.call_function = "self.import_scraping." + str(function_name) + "(self.init, self.fin, self.threadID)"
   def run(self):
      print ("Starting Thread " + str(self.threadID) + " on indexes " + str(self.init) + " to " + str(self.fin))
      exec(self.call_function)
      #log.write("Exiting Thread" + str(self.threadID) + "\n")
      print ("Exiting Thread " + str(self.threadID))

def start_threads(file_path_name, function_name, size, threads_number):

   #Windows
   if len(file_path_name.split("\\")) > 1:
      file_name = file_path_name.split("\\")[-1].split(".")[0]
      file_path = "\\".join(file_path_name.split("\\")[0:-2])
   #Linux
   else:
      file_name = file_path_name.split("/")[-1].split(".")[0]
      file_path = "/".join(file_path_name.split("/")[0:-2])
   
   sys.path.insert(1, file_path)

   indexes = []
   indexes.append(0)
   threads = []
   #Start Threads
   for i in range(threads_number):
      if i < threads_number-1:
         index = (i+1) * math.floor(size/threads_number)
      else:
         index = size
      indexes.append(index)
      threads.append(myThread((i+1), file_name, function_name, indexes[-2], indexes[-1]))
      threads[-1].start()
   
   #Join Threads
   for i in range(threads_number):
      threads[i].join()
   return