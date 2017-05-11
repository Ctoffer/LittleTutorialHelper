#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 18:38:07 2017

@author: christopher
"""
from sys import argv

from gmdata_managment import FolderManager
from muesli import MuesliApi
from student import ConsoleStudentGetter as CStudGetter

if __name__ == '__main__':
    fm = FolderManager()

    student = CStudGetter(fm).readStudent(initialGuess = argv[1] if len(argv) > 1 else '')
    print(student['Name'], fm.getDateFor(student['TID']))

    with MuesliApi(acc = fm.getMÜSLIAcc()) as mapi:
        date = fm.getDateFor(student['TID'])
        pres = input('Set state for "%s" (0 = not presented, else = presented): ' % student['Name']) != '0'
        print('MÜSLI-Entry was set to %s' % ('"1.0" (TRUE)' if pres else '"" (FALSE)'))
        mapi.setPresentedState(student, date = date, presented = pres)

