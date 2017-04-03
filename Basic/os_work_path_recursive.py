#!/usr/bin/python3
# -*- coding: utf8 -*-

import os

if __name__ == '__main__' :

    findext = '.py'
    targetpaht = "./"
    stop = None

    for (root, dirs, files) in os.walk(targetpaht) :
        print("root: " + root)
        print("sub folder", len(dirs))
        print("files", len(files))
    
        for file in files :
            (dir, filename) = os.path.split(file)
            (basefilename, ext) = os.path.splitext(filename)	

            if findext == ext :
                path = os.path.join(root, file)
                abspath = os.path.abspath(path)
                        
                print("find file: " + path)
                print("abs: " + abspath)

                print("\r\nfile contens\r\n")
                with open(abspath, "rt") as f:
                    for line in f.readlines() :
                        print(line.strip())

                stop = True
                break

        if stop :
            # break early for easy check output
            break