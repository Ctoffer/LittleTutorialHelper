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
from gmdata_managment import createMetaDataFile, modifyMetaData
from gmdata_managment import getTutMetaInfo
from gmdata_managment import createTutoriumList
from gmdata_managment import createExternalStudentsList
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
        inp = input('MetaData are already existent: \n\
                     o|O Override \n\
                     m|M Modify   \n\
                     .*  Skip\n\nChoose option: ')
        if  inp.lower() == 'o':
            tutLinks = createMetaDataFile(globalMdataPath)
            onChange = True
            
        elif inp.lower() == 'm':
            tutLinks = modifyMetaData(globalMdataPath)
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


    studentsListPath = pjoin(globalMdataPath, 'StudentList.txt')
    #External
    createExternalStudentsList(globalMdataPath)
    
    # Pre-Init
    if not pexists(studentsListPath):
        createStudentsList(globalMdataPath, ignore = True)

    #Imported/Exported
    print('=' * 30)
    importPath = pjoin(globalMdataPath, 'Imported.txt')
    print('=' * 30)
    exportPath = pjoin(globalMdataPath, 'Exported.txt')

    cif = createImportFile(importPath)
    cef = createExportFile(exportPath)
    onChange = cif or cef or onChange

    if onChange:
        print('Some files have been updated - Updating StudentsList')

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

