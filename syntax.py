#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 20:06:07 2017

@author: christopher
"""

from os.path import basename
from os.path import splitext
from re import compile as rcompile

def checkParenExpr(path):
    collect = False
    exprs = []
    expr = ''
        
    i = 0
    while i < len(path):
        c = path[i]
        
        if c == '(':
            collect = True
            i += 1
            continue
                    
        elif c == ')':
            collect = False
            exprs.append(expr)
            expr = ''
                        
        if collect:
            expr += c
        i += 1
                
    for e in exprs:
        path = path.replace(e, e.replace('_', '-'))
    return path

def extractStudentNamesFromPath (path):
        return [x.split('(')[0].replace('-', ' ') for x in basename(path).split('.')[0].split('_')[2:]]

class SubmissionSyntaxCorrector(object):
    
    def __init__ (self, tutLastname, sheetNr):
        self.__tutLastname = tutLastname
        self.__sheetNr = sheetNr
        self.__exts = ['zip', 'tar', 'tar.gz', 'rar']
        
        pat = self.__tutLastname.upper()\
                + '_Blatt' + str(sheetNr).zfill(2)\
                + '_(.+-.+(\(.+-.+\))*)+'\
                + '\.(zip|tar\.gz|tar|rar)'
        
        self.__pattern = rcompile(pat)
        
    def isCorrect (self, path):
        if self.__pattern.match(basename(path)):
            return True
        else:
            return False
        
    def isSupportedArchive (self, path):
        return splitext(path)[1][1:] in self.__exts
        
    def filterPaths (self, paths):
        return ([x for x in paths if self.isCorrect(x)], [x for x in paths if not self.isCorrect(x)])
    
    def autocorrect (self, path, foldManager):
        path = basename(path)
        if self.isCorrect(path):
            return (path, True)
        
        # if extension is not supported there is no hope for auto-correct
        extension = splitext(path)[1]
        if extension[1:] not in self.__exts:
            return (path, False)
        
        # remove spaces
        if ' ' in path:
            path = path.replace(' ', '_').replace(',', '_')
            
        parts = checkParenExpr(path[:-len(extension)]).split('_')
        students = []
        namepat = rcompile('(.+-.+(\(.+-.+\))*)+')
        
        for part in parts:
            # a part containing a number -> skip
            if any(char.isdigit() for char in part):
                continue
            
            # caps segment will be ignored
            elif part.isupper():
                continue
            
            # correct name part
            elif namepat.match(part):
                students.append(part)
                
            # part in CamelCase
            elif len([i for i, c in enumerate(part) if c.isupper()]) > 1:
                indi = [i for i, c in enumerate(part) if c.isupper()][1:]
                tmp = []
                for ind in indi:
                    l = part[:ind]
                    r = part[ind:]
                    if l not in tmp:
                        tmp.append(l)
                    if r not in tmp:
                        tmp.append(r)
                        
                name = ' '.join(tmp)
                res = foldManager.findStudentByName(name, status = 'Local;Imported')
                
                if len(res) == 1:
                    students.append(res[0]['Name'].replace(' ', '-'))
                    
                elif len(res) > 1:
                    continue
                
                elif len(res) == 0 and len(name) > 6:
                    return (path, False)
                    
            # try to check if its a known name part
            else:
                res = foldManager.findStudentByName(part.capitalize(), status = 'Local;Imported')
                
                if len(res) == 1:
                    tmp = res[0]['Name'].replace(' ', '-')
                    if tmp not in students:
                        students.append(tmp)
                    
                elif len(res) > 1: # name part thats not unambiguously
                    return (path, False)
                
        # no students 
        if len(students) == 0:
            return (path, False)
                
        students = sorted(students, key = lambda x: x.split('-')[0])
        npath = self.__tutLastname.upper() + '_Blatt' + str(self.__sheetNr).zfill(2)
        
        for student in students:
            npath += '_' + student
            
        npath += extension
        
        return (npath, True)
        
        
