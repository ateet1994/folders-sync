#!/usr/bin/env python

import shutil, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--dry-run', action='store_true')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-f', '--folders', type=str, nargs=2, metavar=('folder1', 'folder2'))
args = parser.parse_args()
class Sync:
  def __init__(self, path1, path2, dry_run=False):
     self.path1 = path1
     self.path2 = path2
     self.notinitialdir = False
     self.dry_run = dry_run
     self.walk(self.path1)
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
        if self.dry_run:
          print 'Does not exist', file2
        else:
          print filename, '->', file2
          shutil.copy2(filename, file2)
        continue
      time1 = os.path.getmtime(filename)
      time2 = os.path.getmtime(file2)
      delta = time1 - time2
      if abs(delta) < 2:
        continue
      elif delta > 0:
        if self.dry_run:
          print 'Contents changed', filename
        else:
          print filename, '->', file2
          os.remove(file2)
          shutil.copy2(filename, file2)
      else:
        if self.dry_run:
          print 'Contents changed', file2
        else:
          print file2, '->', filename
          os.remove(filename)
          shutil.copy2(file2, filename)
   
  def walk(self, folder):
    if args.verbose:
      print 'In', folder
    os.chdir(folder)
    files, dirs = self.splitDirsAndFiles(folder)
    folder2 = self.splitAndForm(folder)
    recurse = True
    if (not os.path.exists(folder2)) and self.notinitialdir:
      if self.dry_run:
        print 'Does not exist', folder2
      else:
        print folder, '->', folder2
        shutil.copytree(folder, folder2)
      recurse = False
    self.notinitialdir = True
    if recurse:
     self.fileSync(files)
     for directory in dirs:
      os.chdir(folder)
      self.walk(os.path.abspath(directory))

folders = ['/home/ateet/Documents/codes/', '/grive/codes/']
if args.folders:
  folders = args.folders
Sync(folders[0], folders[1], args.dry_run)
