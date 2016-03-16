#!/usr/bin/env python

import shutil, os

path1 = '/home/ateet/Documents/codes/temp/syn1'
path2 = '/home/ateet/Documents/codes/temp/syn2'
flag = False
def splitAndForm(path):
  return path2 + path.replace(path1, '', 1)

for folderName, subfolders, filenames in os.walk(path1):
  os.chdir(folderName)
  if flag:
    destFolder = splitAndForm(os.path.abspath(folderName))
    if not os.path.exists(destFolder):
      shutil.copytree(folderName, destFolder)
      continue
  flag = True
  for filename in filenames:
      file2 = splitAndForm(os.path.abspath(filename))
      if not os.path.exists(file2):
        shutil.copy(filename, file2)
        continue
      time1 = os.path.getmtime(filename)
      time2 = os.path.getmtime(file2)
      if time1 < time2:
        shutil.copy(file2, filename)
      elif time1 > time2:
        shutil.copy(filename, file2)
      
