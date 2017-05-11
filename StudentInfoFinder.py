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
    fm = FolderManager()
    student = CStudGetter(fm).readStudent(initialGuess = sys.argv[1] if len(sys.argv) > 1 else '')
    
    m = len(max(student.getKeys(), key = len))
    divider = '-' * 50
    
    print(divider)
    
    for key in student.getKeys():
        if key == 'TID':
            print(key + ':'.ljust(m + 2 - len(key)), '_'.join(fm.getDateFor(student[key])))
        else:
            print(key + ':'.ljust(m + 2 - len(key)), student[key])
        
    print(divider)
    
