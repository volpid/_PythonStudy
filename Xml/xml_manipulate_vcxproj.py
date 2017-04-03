
import logging
import os
import re
import shutil
import stat
import xml.etree.ElementTree as ET

from xml_namespace import *

#------------------------------------------------------------------
# setup logging

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
    # NOTSET = 0
    # WARN = 30
    # WARNING = 30
    if logging.getLogger().getEffectiveLevel() <= level :
        return True
    return False

def LogWarn(text) :	
    logging.warning(text)
def LogInfo(text) :	
    print(text)
    logging.info(text)
def LogDebug(text) :	
    logging.debug(text)	
def LogError(text) :	
    logging.error(text)
   
#------------------------------------------------------------------
# xml mnipulate

encoding = 'utf-8'

def PrintXmlProjectIncludeFiles(xmlfile) :
    LogInfo('PrintXmlProjectIncludeFiles')

    abspath = os.path.dirname(xmlfile);
    if os.path.exists(xmlfile) : 	
        incluidefiles = [];			
        pathMatch = re.compile('(ClInclude Include=|ClCompile Include=)"(.*)"');
        with open(xmlfile, 'r', encoding = encoding) as projfile :
            for line in projfile.readlines() :
                groups = pathMatch.findall(line);
                if len(groups) > 0 :		
                    includefile = groups[0][1]
                    (filename, ext) = os.path.splitext(includefile);
                    if ext.lower() in ['.h', '.hpp', '.cpp', '.c'] :								
                        curpath = abspath + '\\' + includefile;
                        absorigin = os.path.abspath(curpath);
                        incluidefiles.append(absorigin.lower());
                        LogDebug('\t -> origin files : {}'.format(absorigin));
                    else :
                        LogDebug('\t -> skipped files : {}'.format(filename + ext));

def ParseConfigurationCondition(text) :
    quationSpliter = re.compile('[\'\']')
    splitList = quationSpliter.split(text)
    return splitList[3]

def GetConfigurationType(text) :
    configurationTypes = {
        'DynamicLibrary' : 'dll',
        'Application' : 'exe',
        'StaticLibrary' : 'lib'
    }

    if text in configurationTypes.keys() :
        return configurationTypes[text]

    raise Exception('Unkown ConfigurationType - ' + text)

def SetupVcxprojAttrib(absfile, xmlns):	
    LogInfo('\n#SetupVcxprojAttrib')

    xmltree = ET.parse(absfile)
    xmlroot = xmltree.getroot()	
    vcxprojAttribs = {}

    # 'AbsPath'
    # 'Filename'
    # 'RootNamespace'
    # 'Configurations'
    #	+ Configuration + ConfigurationType + Condition

    #AbsPath
    vcxprojAttribs['AbsPath'] = os.path.dirname(absfile)
    #Filename
    (baseFilename, ext) = os.path.splitext(os.path.basename(absfile))
    vcxprojAttribs['Filename'] = baseFilename

    #RootNamespace
    propertyGroupRootNamespaces = xmlroot.findall('vcns:PropertyGroup/vcns:RootNamespace', xmlns)
    try :
        if len(propertyGroupRootNamespaces) > 1 :
            raise Exception('more than one rootnamespace !!')

        vcxprojAttribs['RootNamespace'] = propertyGroupRootNamespaces[0].text
    except Exception as e:
        LogError('RootNamespace :' + e.message)
        vcxprojAttribs['RootNamespace'] = ''

    #Configurations
    configurations = []

    itemGroupProjectConfigurations = xmlroot.findall('vcns:ItemGroup/vcns:ProjectConfiguration', xmlns)
    for itemProjectConfig in itemGroupProjectConfigurations :
        configurationTag = itemProjectConfig.find('vcns:Configuration', xmlns).text
        condition = itemProjectConfig.get('Include')
        configurationType = ''
        configurationTargetName = ''

        propertyGroups = xmlroot.findall('vcns:PropertyGroup', xmlns)		
        for property in propertyGroups :
            conditionText = property.get('Condition')
            if not conditionText : 
                continue

            propertyCondition = ParseConfigurationCondition(conditionText)
            if propertyCondition == condition :		
                cfgType = property.findtext('vcns:ConfigurationType', namespaces = xmlns)
                if cfgType:
                    configurationType = GetConfigurationType(cfgType)

        configurations.append((configurationTag, 
            condition, 
            configurationType))

    vcxprojAttribs['Configurations'] = configurations

    if CheckDoLogging(logging.DEBUG) :		
        LogInfo('##VcxprojAttrib')
        msg = '\n\t'.join('{key} : {value}'.format(key = k, value = v) for (k, v) in vcxprojAttribs.items())
        msg = '\t' + msg + '\n'
        LogInfo(msg)

    return vcxprojAttribs

def RemoveItemDefinitionGroup(xmlAttrib, xmlTree, xmlns) :
    LogInfo('\n#RemoveItemDefinitionGroup')

    xmlRoot = xmlTree.getroot()
    for itemDefinitionGroup in xmlRoot.findall('vcns:ItemDefinitionGroup', xmlns) :
        isChildRemoved = False
        for SccProjectName in itemDefinitionGroup.findall('vcns:PreBuildEvent', xmlns) :
            isChildRemoved = True
            itemDefinitionGroup.remove(SccProjectName)
        for SccLocalPath in itemDefinitionGroup.findall('vcns:PreLinkEvent', xmlns) :
            itemDefinitionGroup.remove(SccLocalPath)
        for SccProvider in itemDefinitionGroup.findall('vcns:PostBuildEvent', xmlns) :
            itemDefinitionGroup.remove(SccProvider)

        if isChildRemoved :
            LogInfo('#Remove Event : ' + str(itemDefinitionGroup))	


def ModifyPropertyGroup(xmlAttrib, xmlTree, xmlns) :
    LogInfo('\n#ModifyPropertyGroup')

    xmlRoot = xmlTree.getroot()
    for PropertyGroup in xmlRoot.findall("vcns:PropertyGroup", xmlns) :
        isChildChanged = False

        for CharacterSet in PropertyGroup.findall("vcns:CharacterSet", xmlns) :			
            CharacterSet.text = 'Unicode'
            isChildChanged = True

        for PlatformToolset in PropertyGroup.findall("vcns:PlatformToolset", xmlns) :
            PlatformToolset.text = 'vs100'
            isChildChanged = True

        if isChildChanged :
            LogInfo('#Modify : ' + str(PropertyGroup.get('Condition')))

def InjectPropertyProp(xmlAttrib, xmlTree, xmlns) :
    LogInfo('\n#InjectPropertyProp')

    injectProperty = 'InjectProperty.props'
    injectProject = xmlAttrib['AbsPath'] + '/' + injectProperty;
    injectLabel = 'LocalAppDataPlatform'

    conditionIndex = 0;
    xmlRoot = xmlTree.getroot()
    for ImportGroup in xmlRoot.findall("vcns:ImportGroup", xmlns) :		
        if ImportGroup.get('Label') == 'PropertySheets' :		
            needToInject = True			

            for Import in ImportGroup.findall("vcns:Import", xmlns) :					
                if Import.get('Project').find(injectProperty) > 0 :
                    needToInject = False
                    break

            if needToInject :
                injectCondition = xmlAttrib['Configurations'][conditionIndex]
                conditionIndex += 1

                LogInfo("## InjectProperty.props -> {} ".format(injectProject))
                Import = ET.SubElement(ImportGroup, 'Import')
                Import.set('Condition', injectCondition)
                Import.set('Project', injectProject)
                Import.set('Label', injectLabel)
                Import.tail = '\n  '

#------------------------------------------------------------------

def ModifyVcprojXmlFile(vcxprojXmlfile) :
    LogInfo('\n#ModifyVcprojXmlFile {} '.format(vcxprojXmlfile))
    xmlns = {'vcns' : GetDefaultXMLNamespace(vcxprojXmlfile)}	
    SetDefaultXMLNamespace(xmlns['vcns'])

    xmlTree = ET.parse(vcxprojXmlfile)
    xmlRoot = xmlTree.getroot()

    vcxPrjAttrib = SetupVcxprojAttrib(vcxprojXmlfile, xmlns)

    #remove field
    RemoveItemDefinitionGroup(vcxPrjAttrib, xmlTree, xmlns)
    #modify field
    ModifyPropertyGroup(vcxPrjAttrib, xmlTree, xmlns)
    #inject field
    InjectPropertyProp(vcxPrjAttrib, xmlTree, xmlns)

    try :
        os.chmod(vcxprojXmlfile, stat.S_IWRITE)
        os.remove(vcxprojXmlfile);
        xmlTree.write(vcxprojXmlfile, encoding = encoding, xml_declaration = True);
    except Exception() as e:
        LogError('XmlFile write fail :' + e.message)

#------------------------------------------------------------------
# main test 

def DoMainTest(xmlfile) :
    PrintXmlProjectIncludeFiles(xmlfile)
    ModifyVcprojXmlFile(xmlfile)

    #namespace = getDefaultXMLNamespace(xmlfile)    
    #xmlns = {'vcns' : namespace}	
    #setDefaultXMLNamespace(namespace)
    
if __name__ == '__main__' :
    originfile = r'./_Output/_vs2015_source.vcxproj'
    xmlfile = r'./_Output/manipulate_source.vcxproj'

    if os.path.exists(xmlfile) :
        os.chmod(xmlfile, stat.S_IWRITE)
        os.unlink(xmlfile)

    shutil.copyfile(originfile, xmlfile)

    loggingFile = r'./_Output/xml_logging.log'
    #SetupLoggingFile(loggingFile, logging.INFO)
    SetupLoggingFile(loggingFile, logging.DEBUG)
    DoMainTest(xmlfile)