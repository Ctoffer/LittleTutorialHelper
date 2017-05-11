#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 17:46:19 2017

@author: christopher
"""

#==============================================================================
import os
import shutil

from sys import argv
from sys import exit

from tarfile import open as taropen
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
from rarfile import RarFile

from gmdata_managment import FolderManager as FM
from gmdata_managment import createRow

from moodle import MoodleApi
from moodle import Submission

from student import StudentFilter as StudFil

from syntax import SubmissionSyntaxCorrector as SuSyCo


#==============================================================================

"""
    Utility
    Create directories of the given path.
    If the directory already exists, just return the path
"""
def mkPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
    
    return path

"""
    Utility
    Find the maxium string length of each column in a table.
    A table is an iterateable of dictionary-like objects.
    
    return a list of the maximum string lengths
"""
def findMaxs (keys, table):
    maxs = []
    for i in range(len(keys)):
        maxs.append(len(keys[i]))
        
    for elem in table:
        for i in range(len(maxs)):
            if maxs[i] < len(str(elem[keys[i]])):
                maxs[i] = len(elem[keys[i]])
    return maxs

#==============================================================================
# Structure of one Blatt_\d\d
#==============================================================================
"""
     Structure:
         
     |
     *Blatt_\d\d
     | |
     | *00_Origin
     | | |
     | | +submissions.txt
     | | ~(zip | tar | tar.gz | rar)
     | | ...
     | |
     | *01_Working
     | | |
     | | *00_TUTORIAL1
     | | *01_TUTORIAL2
     | | *02_Imported
     | | *03_Hybrid
     | | *04_Unknown
     | | +GlobalFeedback.txt
     | | +MaxCredits.txt
     | |
"""
#==============================================================================
#==============================================================================
# Original archives

def loadAllArchivesToOrigin (fm, orgPath, tutorLastName, sheetNr):
    oArchives = []

    with MoodleApi( acc = fm.getMoodleAcc()) as moodle:
        sf = StudFil(fm.getAllStudents(status='Local;Imported'))
        subms = moodle.extractSubscriptionRowsFor(sheetNr = sheetNr, studFilter= sf)
    
        maxs = findMaxs(Submission.getKeys(), subms)
    
        subTxtPath = os.path.join(orgPath, 'submissions.txt')
        with open(subTxtPath, 'w') as subTxtF:
            for subm in subms:
                print(createRow([x for x in subm], maxs), file = subTxtF)
    
        print('Found %i filtered submissions. Download will start soon.' % len(subms))
        oArchives = moodle.downloadSubmissions(subms, orgPath)
        print('Download finished')

    
    ssc = SuSyCo(tutorLastName, sheetNr)
    rSyn, wSyn = ssc.filterPaths(oArchives)
    print('Correct Syntax %i' % len(rSyn), 'Wrong Syntax %i' % len(wSyn))
    print('Start autocorrecting...')
    
    for origArchive in wSyn:
        npath, cor = ssc.autocorrect(origArchive, fm)
    
        if cor and npath != origArchive:
            os.rename( os.path.join(orgPath, origArchive), os.path.join(orgPath, npath))
            oArchives.remove(origArchive)
            oArchives.append(npath)
        
    print('... finished.')
    rSyn, wSyn = ssc.filterPaths(oArchives)
    print('Correct Syntax %i' % len(rSyn), 'Wrong Syntax %i' % len(wSyn))
    print('%i files need human interpretation!' % len(wSyn))
    
    for file in wSyn:
        print('=' * 30)
        print('Current name:', os.path.basename(file))
        while True:
            newName = input('Corrected name [.zip if file is not an archive]:')
        
            if ssc.isCorrect(newName) and ssc.isSupportedArchive(file):                
                print('Rename...', end = '')
                newPath =  os.path.join(orgPath, newName)
                os.rename(file, newPath)
                rSyn.append(newPath)
                print('[OK]')
                break
             
            elif ssc.isCorrect(newName) and not ssc.isSupportedArchive(file):
                print('Create Archive...', end = '')
                newPath = os.path.join(orgPath, newName)
                with ZipFile(newPath, 'w', ZIP_DEFLATED) as zFile:
                    zFile.write(file, os.path.basename(file))
                # delete homeless file
                if os.path.isdir(file):
                    shutil.rmtree(file)
                else:
                    os.remove(file)
            
                rSyn.append(newPath)
                print('[OK]')
                break
                
            else:
                print('Wrong Syntax - Try again please')
        print('=' * 30)
    wSyn = []
    return [os.path.join(orgPath, os.path.basename(path)) for path in rSyn]

#==============================================================================
# Unfolded archives

def createMaxCreditFile(workingPath):
    with open(os.path.join(workingPath, 'MaxCredits.txt'), 'w') as fd:
        creds = input('Write max credits per excercise seperated by space: ').split(' ')
        for credit in creds:
            print(credit, file = fd)
        return len(creds)    
    
def loadFromMaxCreditFile(workingPath):
    creds = []
    with open(os.path.join(workingPath, 'MaxCredits.txt'), 'r') as fd:
        for line in fd:
            creds.append(int(line))
            
    return creds
            
def createGlobalFeedback(workingPath):
    with open(os.path.join(workingPath, 'GlobalFeedback.txt'), 'w') as fd:
        print('Hier könnte Ihre Werbung stehen oder ein Feedback.', file = fd)
        
def createCategories (workingpath, tids, dates):
    i = 0
    folders = []
    for tid in tids:
        folders.append(str(i).zfill(2) + '_' + dates[tid])
        i += 1
    for name in ['Imported', 'Hybrid', 'Unknown']:
        folders.append(str(i).zfill(2) + '_' + name)
        i += 1
    
    return [mkPath(path) for path in [os.path.join(workingpath, x) for x in folders]]

def unfoldArchives(workingPath, archives):
    submFolders = []
    opener = {'tar.gz' : lambda tgzFile: taropen(tgzFile, 'r:gz'),
                 'tar' : lambda   tFile: taropen(tFile, 'r:'),
                 'zip' : lambda   zFile: ZipFile(zFile, 'r'),
                 'rar' : lambda   rFile: RarFile(rFile, 'r')
              }
    
    print('Start unfolding...', end = '')
    for archive in archives:
        for k,v in opener.items():
            if archive.endswith(k):
                with v(archive) as locFile:
                    path = os.path.join(workingPath, os.path.basename(archive)[0:-len('.' + k)])
                    locFile.extractall(path)
                    submFolders.append(path)
                    
    print('[OK]')
    
    return submFolders

def createFeedbackFiles (folders, creditCount):
    for folder in folders:
        with open(os.path.join(folder, 'Feedback.txt'), 'w') as fd:
            for i in range(1, creditCount + 1):
                print('#Aufgabe %i' % i, file = fd)
                print('#SUM[-0]', file = fd)
                print(file = fd)
                 
def findCategoryOf (fm, cats, path):
    names = [x.replace('-', ' ') for x in os.path.basename(path).split('_')[2:] if x != '']
    
    cat = None
    
    for name in names:
        if '(' in name:
            name = name.split('(')[0]
        
        possStuds = fm.findStudentByName(name, status = 'Local;Imported')
        if len(possStuds) != 1:
            return cats[-1]
        else:
            stud = possStuds[0]
            if cat == None:
                cat = (stud['TID'], stud['Status'])
            else:
                # same tutor, same tutorial
                if stud['TID'] == cat[0] and stud['Status'] == cat[1]:
                    continue
                
                # same tutor different tutorials
                elif stud['TID'] != cat[0] and stud['Status'] == cat[1]:
                    return cats[-2]
                
                # different tutors
                elif stud['TID'] == cat[0] and stud['Status'] != cat[1]:
                    return cats[-3]
        
    return cats[int(cat[0][-2:])]

def moveToCategory (source, dest):
    if os.path.exists(os.path.join(dest, os.path.basename(source))):
        print('%s was already sorted!' % os.path.basename(source))
    else:
        shutil.move(source, dest)


"""
    Create a folder with the structure
    
    First create additional files (needed for MÜSLI sync and mail responses).
    Then download all archives and store them in origin. There an autocorrection
    for folder syntax is performed and after that a manual correction.
    Unzip the archives from origin into working. Create for each a feedback file.
    Create category folders and sort the submission folders into them.
"""
def createSheetFolder (sheetNr = None, onlyUnpack = False):
    # init stuff
    if sheetNr == None:
        sheetNr = int(input('Insert number of the sheet u want to download: '))
    
    fm = FM()
    tids = fm.getTIDs()
    tutInfos = fm.getTutMetaInfo()
    dates = {}
    for tutInfo in tutInfos:
        dates[tutInfo['ID']] = tutInfo['Day'] + '_' + tutInfo['Time']
    root = fm.root # superFolder
    folder = 'Blatt_%s' % str(sheetNr).zfill(2)
    tutorLastName = fm.getTLastName()
    print('Start sync sheet #%i' %  sheetNr)

    # create important dirs
    sheetFolderPath = mkPath(os.path.join(root, folder))
    orgPath = mkPath(os.path.join(sheetFolderPath, '00_Origin'))
    workingPath = mkPath(os.path.join(sheetFolderPath, '01_Working'))
    
    creditCount = 0
    folders = []
    
    if onlyUnpack:
        creditCount = len(loadFromMaxCreditFile(workingPath))
        cond = lambda x: x.endswith('zip') or x.endswith('rar') or x.endswith('tar') or x.endswith('tar.gz')
        
        archives = [os.path.join(orgPath, x) for x in os.listdir(orgPath) if cond(x)]
        folders = unfoldArchives(workingPath, archives)
    
    else:
        # create additional files
        creditCount = createMaxCreditFile(workingPath)
        createGlobalFeedback(workingPath)
    
        # download and unzip archives
        archives = loadAllArchivesToOrigin(fm, orgPath, tutorLastName, sheetNr)
        folders = unfoldArchives(workingPath, archives)
    
    # create feedback-files and sort them into categories
    createFeedbackFiles(folders, creditCount)
    cats = createCategories(workingPath, tids, dates)
    
    for folder in folders:
        print(os.path.basename(findCategoryOf(fm, cats, folder)), os.path.basename(folder))
        moveToCategory(folder, findCategoryOf(fm, cats, folder))
    

if __name__ == '__main__':
    args = {'--nr':None, '--only-unpack':False}
    
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == '--help':
            # TODO fix this for multi parameter
            print('Call with [--help] or [--nr <int>][--only-unpack]')
            exit(0)
            
        elif arg == '--nr':
            args['--nr'] = int(argv[i + 1])
            i += 1
            
        elif arg == '--only-unpack':
            args['--only-unpack'] = True
            
        else:
            exit('Unknown command \'%s\'. Use --help for more information.' % arg)
        i += 1
    
    createSheetFolder(sheetNr=args['--nr'], onlyUnpack=args['--only-unpack'])
