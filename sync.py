#!/usr/bin/env python

import shutil, os

class Sync:
  def __init__(self, path1, path2):
     self.path1 = path1
     self.path2 = path2
     self.notinitialdir = False
  def splitAndForm(self, path):
    return self.path2 + path.replace(self.path1, '', 1)

  def splitDirsAndFiles(self, path):
    files = []
    dirs = []
    for entity in os.listdir(path):
      if os.path.isfile(entity): files.append(entity)
      else: dirs.append(entity)
    return (files, dirs)

  def fileSync(self, files):
   for filename in files:
      file2 = self.splitAndForm(os.path.abspath(filename))
      if not os.path.exists(file2):
        shutil.copy(filename, file2)
        continue
      time1 = os.path.getmtime(filename)
      time2 = os.path.getmtime(file2)
      if time1 < time2:
        shutil.copy(file2, filename)
      elif time1 > time2:
        shutil.copy(filename, file2)
   
  def walk(self, folder):
    os.chdir(folder)
    print folder
    files, dirs = self.splitDirsAndFiles(folder)
    folder2 = self.splitAndForm(folder)
    recurse = True
    if (not os.path.exists(folder2)) and self.notinitialdir:
      shutil.copytree(folder, folder2)
      recurse = False
    self.notinitialdir = True
    self.fileSync(files)
    if recurse:
     for folder in dirs:
      self.walk(os.path.abspath(folder))

if __name__ == '__main__':
  path1 = '/home/ateet/Documents/codes/temp/syn1'
  path2 = '/home/ateet/Documents/codes/temp/syn2'
  sync_obj = Sync(path1, path2)
  sync_obj.walk(path1)
