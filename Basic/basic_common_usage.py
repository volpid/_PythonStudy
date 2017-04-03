#!/usr/bin/python3
# -*- coding: utf8 -*-

import logging
import os
import stat

def GetRelativePath(basePath, destPath) :
	# common_prefix = os.path.commonprefix([basePath, destPath])
	# relative_path = os.path.relpath(destPath, common_prefix)
	relative_path = os.path.relpath(basePath, destPath)
	print( relative_path)
	return relative_path
		
def GetBaseFinename(absfile) :
	(dir, filename) = os.path.split(absfile)
	(basefilename, ext) = os.path.splitext(filename)	
	return basefilename
	
def SetupLoggingFile(loggingFile, loggingLevel) :
    if os.path.exists(loggingFile) :
        os.chmod(loggingFile, stat.S_IWRITE)
        os.remove(loggingFile)

    fileHandler = logging.FileHandler(loggingFile)	
    formatter = logging.Formatter('%(message)s')
    fileHandler.setFormatter(formatter)	
    logging.getLogger().addHandler(fileHandler)
    logging.getLogger().setLevel(loggingLevel)

def CheckDoLogging(level) :	
    # CRITICAL = 50
    # DEBUG = 10
    # ERROR = 40
    # FATAL = 50
    # INFO = 20
    # NOTSET = 0
    # WARN = 30
    # WARNING = 30
	if logging.getLogger().getEffectiveLevel() <= level :
		return True
	return False

def LogWarn(text) :	
	logging.warning(text)
def LogInfo(text) :	
	logging.info(text)
def LogDEBUG(text) :	
	logging.debug(text)
		
#------------------------------------------------------------------
def DoMainTest() :    
    #get relative dir
    path1 = r'.\python_study_vs.pyproj'
    path2 = r'.\_Output\_vs2015_source.vcxproj'
    abspath = os.path.abspath(path2)

    GetRelativePath(path1, path2)
    GetRelativePath(path2, path1)

    ##dir name
    print(os.path.dirname(abspath))

    ##remove ext
    print(GetBaseFinename(abspath))

    ##print list with newline
    lists = ['a', 'a', 'a', 'a', 'a', 'a']
    print("+".join(lists))

    ##print dict with newline
    dicts = {'key1':'value1', 'key2':'value2', 'key3':'value3', 'key4':'value4'}
    print("{\n" + "\n".join('{key}: {value}'.format(key = k, value = v) for k, v in dicts.items()) + "\n}")
    print("{\n" + "\n".join('{}: {}'.format(k, v) for k, v in dicts.items()) + "\n}")
    print("{\n" + "\n".join('{1}: {0}'.format(k, v) for k, v in dicts.items()) + "\n}")

    ##check same type
    print("isinstance", isinstance(dicts, dict))

    ##logging 	
    loggingFile = r'.\_Output\logging.txt'
    SetupLoggingFile(loggingFile, logging.DEBUG)
    if CheckDoLogging(logging.DEBUG) :
        LogDEBUG("LOGGING:DEBUG")
        LogInfo("LOGGING:INFO")
        LogWarn("LOGGING:WARN")

if __name__ == '__main__' :
	DoMainTest()