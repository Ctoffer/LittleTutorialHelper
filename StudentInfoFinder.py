#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 19:44:13 2017

@author: christopher
"""

import sys

from gmdata_managment import FolderManager
from student import ConsoleStudentGetter as CStudGetter

if __name__ == '__main__':  
    includeExt = False
    argvs = sys.argv
    initGuess = ''
    
    for i in range(1, len(argvs)):
        if argvs[i] == '--external' or argvs[i] == '-E':
            includeExt = True
        else:
            initGuess += ' ' + argvs[i] if len(initGuess) > 0 else argvs[i]
    
    fm = FolderManager()
    student = CStudGetter(fm, includeExt = includeExt)  \
                .readStudent(initialGuess = initGuess)
    
    m = len(max(student.getKeys(), key = len))
    divider = '-' * 50
    
    print(divider)
    
    for key in student.getKeys():
        if key == 'TID':
            print(key + ':'.ljust(m + 2 - len(key)), 
                  '_'.join(fm.getDateFor(student[key])))
        else:
            print(key + ':'.ljust(m + 2 - len(key)), 
                  student[key])
        
    print(divider)
    
