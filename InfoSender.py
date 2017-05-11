#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 21:14:55 2017

@author: christopher
"""

from re import compile as rcompile
import sys

from Muesli import MuesliApi as MApi
from Sender import Sender
from TutFolderManager import FolderManager

if __name__ == '__main__':
    argv = sys.argv
    dic = {'Day':None, 'Time':None,
           'Header':None, 'Text':None, 'Att':[],
           'Single':False, 'Multi':False, 'Allowed':False}
    index = -1

    # no args
    if len(argv) == 1:
        print("""
                TAG = Montag | Dienstag | Mittwoch | Donnerstag | Freitag

                -day=<TAG>
                -time=hh:mm
                -header=<string>
                -text=<path>
                -att <all following paths seperated by space>

                -DEBUG
                -DEBUG-MUL

              """)
        sys.exit('')

    for i in range(len(argv)):
        arg = argv[i]

        if rcompile('-day=.*').match(arg):
            dic['Day'] = argv[i][5:]

        elif rcompile('-time=.*').match(arg):
            dic['Time'] = argv[i][6:]

        elif rcompile('-text=.*').match(arg):
            dic['Text'] = argv[i][6:]

        elif '-att' == arg:
            index = i + 1
            print(index)

        elif rcompile('-header=.*').match(arg):
            dic['Header'] = argv[i][8:]

        elif '-DEBUG' == arg:
            print('SINGLE MATCH')
            dic['Single'] = True

        elif rcompile('-DEBUG-MUL').match(arg):
            dic['Multi'] = True

        elif '-ALLOWED' == arg:
            dic['Allowed'] = True

    if index > -1:
        while index < len(argv) and not argv[index].startswith('-'):
            print(argv[i])
            dic['Att'].append(argv[index])
            index += 1

    print(argv)
    FM = FolderManager()
    muesliAcc = FM.getMÜSLIAcc()
    emailAcc = FM.getMailAcc()

    # check important values
    if dic['Header'] == None:
        print('\'Betreff\' wurde nicht definiert - default wurde genommen!')
        dic['Header'] = 'Ich hab Betreff vergessen :/'

    elif dic['Text'] == None:
        sys.exit('Need a message to send pls use -text=<path>')

    elif len(dic['Att']) == 0:
        print('WARNING: No Attachments')

    # send mails
    with Sender(acc = emailAcc) as sender:
        sender.allowed = dic['Allowed']

        if dic['Single']:
            print('Single debug run')
            sender.sendInfoTestMail(FM.getSubject(), dic['Header'], dic['Text'], dic['Att'])

        elif dic['Multi']:
            print('Multiple debug run')
            # use ur different mail adresses as students
            # example:
            #
            # students = [{'Name':'Christopher', 'Mail':'christopher.schuster@stud.uni-heidelberg.de'},
            #            {'Name':'Christopher', 'Mail':'christopher.schuster@t-online.de'},
            #            {'Name':'Christopher', 'Mail':'schustrchr@gmail.com'}]
            
            students = []
            sender.sendInfoMailToAll(students, FM.getSubject(), dic['Header'], dic['Text'], dic['Att'])

        else:
            print('Send to students from', dic['Day'], dic['Time'])

            # TODO load offline email adresses
            students =  None
            with MApi(acc = muesliAcc) as api:
                info = api.getTutorialInfoForDay(dic['Day'], dic['Time'])
                students = api.getStudentsMetaData(info['Link'])

            answer = input('Rly send mails? (Y|n)...')
            if answer == 'Y' or answer == 'y':
                print('...sending')
                sender.sendInfoMailToAll(students, FM.getSubject(), dic['Header'], dic['Text'], dic['Att'])
                sender.sendInfoTestMail(FM.getSubject(), dic['Header'], dic['Text'], dic['Att'])
            else:
                print('... stop')
