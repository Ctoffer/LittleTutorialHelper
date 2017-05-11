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

def uploadCreditFile(creditFile, sheetNr = None):
    print('Upload %s to MÜSLI.' % creditFile)
    fm = FM()
    if sheetNr == None:
        sheetNr = int(pbasename(creditFile).split('.')[0].split('_')[1])
    
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
        

if __name__ == '__main__':
    if len(argv) == 2:
        uploadCreditFile(argv[1])
    else:
        folder = getcwd()
        for entry in scandir(folder):
            if entry.is_file() and rcompile('AllCredits_\d\d\.txt').match(entry.name):
                uploadCreditFile(entry.path)
