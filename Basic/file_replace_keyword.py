#!/usr/bin/python3
# -*- coding: utf8 -*-

import os
import shutil
import stat

from tempfile import mkstemp

def replace(file_path, patterns) :
    #create temp file.
    (fh, abs_path) = mkstemp()
    try :
        with open(abs_path, 'w', encoding = 'utf-8') as newFile:
            with open(file_path, "r", encoding = 'utf-8') as oldFile:
                for line in oldFile :
                    newline = line
                    for pattern in patterns :
                        newline = newline.replace(pattern[0], pattern[1])
                    newFile.write(newline)
    except IOError :
        print("IOError")
    
    os.close(fh)
    os.remove(file_path)
    shutil.move(abs_path, file_path)

if __name__ == '__main__' :
    
    originfile = r'./_Output/vs2015_source.vcxproj'
    replacefile = r'./_Output/replace_source.vcxproj'

    if os.path.exists(replacefile) :
        os.chmod(replacefile, stat.S_IWRITE)
        os.unlink(replacefile)

    shutil.copyfile(originfile, replacefile)

    replacePair = [('</', '['), ('/>', ']'), ('<', '['), ('>', ']')]
    replace(replacefile, replacePair)