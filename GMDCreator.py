#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 19:25:34 2017

@author: christopher
"""

from importlib.util import find_spec

from os import makedirs as omakedirs
from os import getcwd
from os.path import join as pjoin
from os.path import exists as pexists
from os.path import basename as pbasename

from pip import main as pip_main

from gmdata_managment import getMetaDataPath
from gmdata_managment import createMetaDataFile
from gmdata_managment import getTutMetaInfo
from gmdata_managment import createTutoriumList
from gmdata_managment import createImportFile
from gmdata_managment import createExportFile
from gmdata_managment import createStudentsList


def install (module):
    spam_spec = find_spec(module)
    found = spam_spec is not None
    if not found:
        pip_main(['install', module])


# create GlobalMetaData - Folder
#==============================================================================

def createGlobalMetaData(root = getcwd()):
    globalMdataPath = pjoin(root, 'GlobalMetaData')
    onChange = False

    if not pexists(globalMdataPath):
        print('GlobalMetaData', globalMdataPath)
        omakedirs(globalMdataPath)
    else:
        print('[WARNING] GlobalMetaData folder already exists!')
        if input('Wanna override and recreate files (step by step)? (Y|n)') != 'Y':
            print('Execution terminated...')
            return globalMdataPath

    tutLinks = None

    #MetaData.txt
    #--------------------------------------------------------------------------
    metaDataFile = getMetaDataPath(globalMdataPath)
    if pexists(metaDataFile):
        if input('Do u want to override MetaData? (Y|n)') == 'Y':
            tutLinks = createMetaDataFile(globalMdataPath)
            onChange = True
        else:
            print('MetaData.txt will not be changed.')

    else:
        print('Create %s' % pbasename(metaDataFile))
        tutLinks = createMetaDataFile(globalMdataPath)

    if tutLinks == None:
        tutLinks = getTutMetaInfo(globalMdataPath)

    #<ID>_MuesliData.txt
    #--------------------------------------------------------------------------
    for tut in tutLinks:
        tutpath = pjoin(globalMdataPath, tut['ID'] + '_MuesliData.txt')

        if not pexists(tutpath):
            createTutoriumList(tutpath, tut)
        else:
            if input('Do u want to sync and override data for (%s %s)? (Y|n)' % (tut['Day'], tut['Time'])) == 'Y':
                print('Synced')
                print(tutpath, tut)
                createTutoriumList(tutpath, tut)
                onChange = True
            else:
                print('Skipped')

    #Imported/Exported
    importPath = pjoin(globalMdataPath, 'Imported.txt')
    exportPath = pjoin(globalMdataPath, 'Exported.txt')

    cif = createImportFile(importPath)
    cef = createExportFile(exportPath)
    onChange = cif or cef or onChange

    if onChange:
        print('Some files have been updated - Updating StudentsList')

    studentsListPath = pjoin(globalMdataPath, 'StudentList.txt')

    if not pexists(studentsListPath) or onChange:
        createStudentsList(globalMdataPath)
    else:
        print('There were no changes on student data.')
        if input('Do u want to update \'%s\' anyways? (Y|n)' % pbasename(studentsListPath)) == 'Y':
            createStudentsList(globalMdataPath)
        else:
            print('Skipped')

    print('GlobalMetaData created and ready to be used')
    return globalMdataPath

#==============================================================================



if __name__ == '__main__':
    install('bs4')
    install('requests')
    install('zipfile')
    install('rarfile')
    install('tarfile')
    install('smtplib')

    createGlobalMetaData()
