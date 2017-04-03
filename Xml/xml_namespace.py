
import os
import re
import shutil
import stat
import xml.etree.ElementTree as ET

def SetDefaultXMLNamespace(namespace) :
	ET.register_namespace('', namespace)
	
def GetDefaultXMLNamespace(xmlfile) :	
	xmlns = ''
	xmlnsMatch = re.compile('\{(.*)\}')	
	try :
		xmlTree = ET.parse(xmlfile)	
		rootTag = xmlTree.getroot().tag
		matchGroups = xmlnsMatch.match(rootTag)	
		if len(matchGroups.groups()) > 0 :
			xmlns = str(matchGroups.groups(0)[0])
	except : 
		pass
	return xmlns

#------------------------------------------------------------------

def DoMainTest(xmlfile) :
    namespace = GetDefaultXMLNamespace(xmlfile)
    print(namespace)
    xmlns = {'vcns' : namespace}	
    SetDefaultXMLNamespace(namespace)

if __name__ == '__main__' :
    originfile = r'./_Output/_vs2015_source.vcxproj'
    xmlfile = r'./_Output/namespace_source.vcxproj'

    if os.path.exists(xmlfile) :
        os.chmod(xmlfile, stat.S_IWRITE)
        os.unlink(xmlfile)

    shutil.copyfile(originfile, xmlfile)
    DoMainTest(xmlfile)