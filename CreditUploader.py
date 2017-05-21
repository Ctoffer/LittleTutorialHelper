#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 02:22:17 2017

@author: christopher
"""

from os.path import basename as pbasename
from os import getcwd
from os import scandir
from sys import argv

from re import compile as rcompile

from muesli import MuesliApi
from gmdata_managment import FolderManager as FM
#from gmdata_managment import findStudentInList as fStudLi

def extractSheetNr(fName):
    return int(pbasename(fName).split('.')[0].split('_')[1])

def getAllStudentNames(eCreditFile):
    res = []
    
    with open(eCreditFile) as fd:
        for line in fd:
            res.append(line.split('|')[1:-1][0].strip())
            
    return res

def uploadCreditFile(creditFile, fm):
    print('Upload %s to MÜSLI.' % creditFile)
    sheetNr = extractSheetNr(creditFile)
    
    with MuesliApi(acc = fm.getMÜSLIAcc()) as mapi:
        tids = fm.getTIDs()
        infos = fm.getTutMetaInfo()
        
        for tid in tids:
            for info in infos:
                if tid == info['ID']:
                    print(info)
                    result, students = mapi.uploadCredits(info, creditFile, sheetNr)
                    
                    print()
        
                    print('Not matched - maybe some of them didn\'t upload sth:')
                    for student in students:
                        print(student)
            
                    print('_____________________')
                    for r,k in result.items():
                        print(r, k)

def uploadExternalCreditFile(eCreditFile, fm):
    print('Upload %s to MÜSLI.' % eCreditFile)
    sheetNr = extractSheetNr(eCreditFile)
    eTut = pbasename(eCreditFile).split('.')[0].split('_')[3].replace('-', ' ')
    print(eTut)
    names = getAllStudentNames(eCreditFile)
    
    with MuesliApi(acc = fm.getMÜSLIAcc()) as mapi:
        tids = fm.getETIDs()
        infos = [info for info in fm.getETutMetaInfo() if info['ExtTut'] == eTut]
        
        for tid in tids:
            for info in infos:
                if len(names) == 0:
                    print('Nothing to match!')
                    return
                
                if tid == info['ID']:
                    print(info)
                    result, students = mapi.uploadCredits(info, eCreditFile, sheetNr)
                    
                    print()
            
                    print('Matched: ')
                    for r,k in result.items():
                        names.remove(r)
                        print(r, k)
                    print('Still need to match:')
                    for name in names:
                        print(name)


if __name__ == '__main__':
    print('Credit Upload')
    if len(argv) == 2:
        uploadCreditFile(argv[1])
        
    else:
        folder = getcwd()
        fm = FM()
        
        for entry in scandir(folder):
            if entry.is_file():
                print()
                extPatternStr = 'AllCredits_\d\d_%s_.*\.txt' % fm.getTFirstName()
                
                if rcompile('AllCredits_\d\d\.txt').match(entry.name):
                    uploadCreditFile(entry.path, fm)
                
                elif rcompile(extPatternStr).match(entry.name):
                    uploadExternalCreditFile(entry.path, fm)
