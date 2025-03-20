import os
from fileSpitter import spitAllFiles

def main():
 print('hey!')
 files = os.listdir()
 spitAllFiles(files)

 