#!usr/bin/python3
#-*- coding=utf8 -*-

import glob
import os.path

ndir = 0
nfile = 0

def Traverse(dir, depth) :
	global ndir
	global nfile

	for obj in glob.glob(dir + '/*') :
		if depth == 0 :
			prefix = '|--'
		else :
			prefix = '|' + ' ' * depth + '|--'

		if os.path.isdir(obj) :
			ndir += 1
			print(prefix + os.path.basename(obj))
			Traverse(obj, depth + 1)
		elif os.path.isfile(obj) :
			nfile += 1
			print(prefix + os.path.basename(obj))
		else :
			print(prefix + "unkown object", obj)

if __name__ == '__main__' :
	path = "." 
	print('path : ', os.path.abspath(path))

	Traverse(path, 0)
	print("\n", ndir, "directories,", nfile, "files")
			
