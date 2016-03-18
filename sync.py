#!/usr/bin/env python

import shutil, os, sys

class Sync:
  def __init__(self, path1, path2):
     self.path1 = path1
     self.path2 = path2
     self.notinitialdir = False
  def splitAndForm(self, path):
    return os.path.join(self.path2,path.replace(self.path1, '', 1))

  def splitDirsAndFiles(self, path):
    files = []
    dirs = []
    for entity in os.listdir(path):
      if os.path.isfile(entity): files.append(entity)
      else: dirs.append(entity)
    return (files, dirs)

  def fileSync(self, files):
   for filename in files:
      filename = os.path.abspath(filename)
      file2 = self.splitAndForm(filename)
      if not os.path.exists(file2):
        print 'Copying', file2
        shutil.copy(filename, file2)
        continue
      time1 = os.path.getmtime(filename)
      time2 = os.path.getmtime(file2)
      if time1 < time2:
#        print time1, '->', time2
        print file2, '->', filename
        os.remove(filename)
        shutil.copy(file2, filename)
      elif time1 > time2:
#        print time1, '->', time2
        print filename, '->', file2
        os.remove(file2)
        shutil.copy(filename, file2)
   
  def walk(self, folder):
    print 'In', folder
    os.chdir(folder)
    files, dirs = self.splitDirsAndFiles(folder)
    folder2 = self.splitAndForm(folder)
    recurse = True
    if (not os.path.exists(folder2)) and self.notinitialdir:
      print 'Copying', folder2
      shutil.copytree(folder, folder2)
      recurse = False
    self.notinitialdir = True
    if recurse:
     self.fileSync(files)
     for directory in dirs:
      os.chdir(folder)
      self.walk(os.path.abspath(directory))

if __name__ == '__main__':
  if len(sys.argv) > 2:
    path1 = sys.argv[1]
    path2 = sys.argv[2]
  else:
    path1 = '/home/ateet/Documents/codes/temp/syn1/'
    path2 = '/home/ateet/Documents/codes/temp/syn2/'
  sync_obj = Sync(path1, path2)
  sync_obj.walk(path1)
