import os

def spitAllFiles(files):
  for file in files:
   if os.path.isdir(file):
    filess = os.listdir(file)
    print ('parent directory = ' + file + '***constituent files = ' + str(os.listdir(file)))
    for secondLayer in filess:
     spitAllFiles(secondLayer)
   elif os.path.isfile:
    print(file)
 

def main():
 print('hey!')
 files = os.listdir()
 spitAllFiles(files)

 