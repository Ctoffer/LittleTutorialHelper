#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 22:34:45 2017

@author: christopher
"""

from syntax import extractStudentNamesFromPath

from os.path import basename as pbasename
from os.path import dirname as pdirname
from os.path import join as pjoin
from os import scandir as oscandir
from os import getcwd

from os import remove
from shutil import move

from re import compile as rcompile

from gmdata_managment import FolderManager

#path = '/home/christopher/Dokumente/Uni/SS17/IAD/MailingScripts/Blatt_01/01_Working'

def getMaxCredits(path):
    with open(pjoin(path, 'MaxCredits.txt'), 'r') as fd:
        return [int(x) for x in fd]

def findAllSubmissionFolders(path):
    submissions, imported = [], []
    
    for entry in oscandir(path):
        if entry.is_dir():
            if 'Imported' in entry.name:
                imported = [x.path for x in oscandir(entry.path)]
            else:
                submissions += [x.path for x in oscandir(entry.path)]                
    return (submissions, imported)

def getFeedbackFile(subpath):
    return pjoin(subpath, 'Feedback.txt')


def interpretFeedbackFile(subpath):
    creds = []
    curSum = 0
    collect = False
    
    toPath = getFeedbackFile(subpath)
    fromPath = pjoin(subpath, 'tmp.txt')
    
    
    with open(toPath, 'r') as original:
        with open(fromPath, 'w') as tmp:
            for line in original:
                if line.startswith('#Aufgabe'):
                    collect = True
                    print(line, file = tmp, end = '')
                    continue
                
                elif rcompile('#\[(\+|-)?\d+(\.\d+)?\]$').match(line):
                    print(line, file = tmp, end = '')
                    num = line[2:-2]
                    if '+' in num:
                        curSum += float(num)
                    else:
                        curSum -= abs(float(num))
                
                elif line.startswith('#SUM['):
                    if collect:
                        creds.append(curSum)
                        print('#SUM[' + str(curSum) + ']', file = tmp)
                        curSum = 0
                
                else:
                    print(line, file = tmp, end = '')
                    continue
    
    #remove(toPath)
    move(fromPath, toPath)
    
    return creds

def createCreditsText(subpath):
    res = []
    
    creds = interpretFeedbackFile(subpath)
    for name in extractStudentNamesFromPath(subpath):
        res.append((name, creds))
        
    with open(pjoin(subpath, 'credits.txt'), 'w') as fd:
        for tup in res:
            print(tup[0], '|', '|'.join([str(x).zfill(2) for x in tup[1]]), file = fd)
        
    return res

def writeNameCreditLists(path, fname, vals):
    maxCredits = getMaxCredits(path)
    # sort after first name
    vals = sorted(vals, key = lambda x : x[0].split(' ')[0])
    maxs = [0 for x in range(len(vals[0][1]) + 1)]
    
    for val in vals:
        for i in range(len(maxs)):
            if i == 0 and maxs[i] < len(str(val[0])):
                maxs[i] = len(str(val[0]))
                
            elif i > 0 and maxs[i] < len(str(val[1][i - 1])):
                maxs[i] = len(str(val[1][i - 1]))
                            
    with open(pjoin(path, fname), 'w') as fd:
        for val in vals:
           # print name first in line
           print('| ', val[0].ljust(maxs[0]), end = '', file = fd)
           
           # print credits per excercise seperated by |
           for i in range(len(val[1])):
               creds = maxCredits[i] + float(val[1][i])
               # catch negative credits
               if creds < 0:
                   creds = 0
               print(' |', str(creds).ljust(maxs[i + 1]), end = '', file = fd)
               
           print(' |', file = fd)

def createAllCredits(path):
    fm = FolderManager()
    subs, imp = findAllSubmissionFolders(path)
    total = []
    extra = []
    
    curParent = path
    sheetNr = ''
    while True:
        tmp = pdirname(curParent)
        if tmp == curParent:
            raise ValueError("U can't use this script here!")
        curParent = tmp
        if rcompile('Blatt_\d\d').match(pbasename(curParent)):
            sheetNr = pbasename(curParent).split('_')[1]
            break
    
    for subpath in subs:
        for tup in createCreditsText(subpath):
            total.append((tup[0], [('%.2f' % x).zfill(5) for x in tup[1]]))
            
    for subpath in imp:
        for tup in createCreditsText(subpath):
            searchRes = fm.findStudentByName(tup[0], status = 'Imported')
            if len(searchRes) == 1:
                extra.append((searchRes[0], [('%.2f' % x).zfill(5) for x in tup[1]]))
            else:
                total.append((tup[0], [('%.2f' % x).zfill(5) for x in tup[1]]))
           
    print('Create %s ...' % ('AllCredits_%s.txt' % sheetNr), end = '', flush = True)
    writeNameCreditLists(path, 'AllCredits_%s.txt' % sheetNr, total)
    print('[OK]')
    
    extTutDict = {}
    for elem in extra:
        eTutor = elem[0]['ExtTut']
        if eTutor in extTutDict:
            extTutDict[eTutor].append((elem[0]['Name'], elem[1]))
        else:
            extTutDict[eTutor] = [(elem[0]['Name'], elem[1])]
            
    for k,v in extTutDict.items():
        fname = 'AllCredits_%s_%s_%s.txt' % (sheetNr, fm.getTFirstName(), k.replace(' ', '-'))
        print('Create %s ...' % fname, end = '', flush = True)
        writeNameCreditLists(path, fname, v)
        print('[OK]')
    
if __name__ == '__main__':
    createAllCredits(getcwd())
