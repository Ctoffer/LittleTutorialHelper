#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 21:12:30 2017

@author: christopher
"""

import os
from os.path import join as pjoin
from re import compile as rcompile

import template_holder as RTH

from moodle import MoodleApi
from muesli import MuesliApi
from student import ConsoleStudentGetter
from student import Student
from student import StudentFilter
from student import isNameIn
from util import getMaximumColumnSizes

"""
    +GlobalMetaData
    |
    |--->MetaData.txt
    |--->Tut00_MuesliData.txt
    |--->Tut01_MuesliData.txt
    |--->StudentsList.txt
    |--->Imported.txt
    |--->Exported.txt
    |--->info_template.html
    |--->return_template.html
"""


#==============================================================================
# create MetaData.txt
#==============================================================================

def createTutoriumId(identification, tutorium):
    return 'Tut' + str(identification).zfill(2)

def createTutoriumMData(i, tut):
    res = '| '
    res += tut['ID'] + ' | '
    res += tut['Day'].rjust(12) + ' | '
    res += tut['Time'] + ' | '
    res += tut['Place'].rjust(20) + ' | '
    res += tut['Subject'] + ' | '
    res += tut['Link'] + ' |'

    return res

def createInfoTemplate(gMDPath):
    path = os.path.join(gMDPath, 'info_template.html')

    with open(path, 'w') as fd:
        print(RTH.getInfoTemplateText(), file = fd)

    return path

def createReturnTemplate(gMDPath):
    path = os.path.join(gMDPath, 'return_template.html')

    with open(path, 'w') as fd:
        print(RTH.getReturnTemplateText(), file = fd)

    return path

def modify(text, reverse = False):
    if reverse:
        return ''.join([chr(int(x)) for x in text[1:].split('|')])
    else:
        return '>' + '|'.join([str(ord(c)) for c in text])


def createAttribute(gMDFile, key, value, secure = True):
    print(key, '=', modify(value) if secure else value, file = gMDFile)


def chooseFromList(li, cdiscr = 'elements', iSent = 'Choose index (type -1 to try again): ', key = None, single = False):
    print('Found %i %s:' % (len(li), cdiscr))
    print(iSent)
    
    for i, v in enumerate(li):
        print(str(i).zfill(2), v if key == None else v[key])
    
    while True:
        index = int(input(iSent))
        if index == -1:
            if single:
                return None
            else:
                continue
        
        print('')
        break
    
    return li[index]

def getAccountFromUser (accName = 'MÜSLI'):
    return (input('Please insert %s-Username: ' % accName), 
            input('Please insert %s-Password: ' % accName))
    
def getLoginDataFromUser (platforms = ['Müsli', 'Moodle', 'Mail']):
    loginData = {}
    
    for platform in platforms:
        acc, passw = getAccountFromUser(accName = platform)
        loginData['%s_USER' % platform.upper()] = acc
        loginData['%s_PASSW' % platform.upper()] = passw
        
    return loginData
            
def getSynchedTutsFromUser (muesliName, muesliPassw):
    synchedTuts = []
    
    with MuesliApi(acc = (muesliName, muesliPassw)) as muesli:
        tutorials = muesli.getCurrentTutorials()
        
        for tut in tutorials:
            print('Do u want to synch data from this tutorial:',
                  tut['Subject'],
                  '(', tut['Day'], tut['Time'], ')',
                  end = '')

            if input('(Y|n)') == 'Y':
                print('Added')
                synchedTuts.append(tut)
            else:
                print('Skipped')
    
    return synchedTuts

def getMoodleDataFromUser (moodleName, moodlePassw):
    seq = 'Choose where ur tutorial is by index \
            (Type -1 to return to previous step): '
    
    data = [None] * 3
    listData = [lambda d1, d2 : [x['Name'] for x in moodle.listFacilities()],
                lambda d1, d2 : [x['Name'] for x in moodle.listSubFacilitiesOf(d1)],
                lambda d1, d2 : moodle.listCoursesOf(d1, d2)
                ]
    cdiscrs = ['facilities', 'subfacilities', 'subfacilities']
    cFL = lambda lvl, d1, d2: chooseFromList(listData[lvl](d1, d2),
                                   cdiscr = cdiscrs[lvl], iSent = seq, single = True)
    
    courseLink = None
    lvl = 0

    with MoodleApi(acc = (moodleName, moodlePassw)) as moodle:
        while True:
            val = ''
            if lvl >= 0 and lvl < 3:
                val = cFL(lvl, data[0], data[1])
            else:
                break
                
            if val == None:
                if lvl > 0:
                    lvl -= 1
            else:
                data[lvl] = val
                lvl += 1
                
        moodle.moveToCourse (courseData = (data[0], data[1], data[2]))
        courseLink = moodle.curURL
        print('Your tutorial is located here: %s' % courseLink)
        
    data.append(courseLink)
    print('')
    return tuple(data)

def getMoodleDataFromFile (gMDataPath):
    return (readAttribute(gMDataPath, 'FACILITY'), 
            readAttribute(gMDataPath, 'SUB_FACILITY'), 
            readAttribute(gMDataPath, 'COURSE'), 
            readAttribute(gMDataPath, 'COURSE_LINK'))
    
def writeToMetaData (gMDPath, subj, loginKData, personalKData, synchedTuts, moodleKData):
    keys, loginData = loginKData
    personalKeys, personalData = personalKData
    moodleKeys, moodleData = moodleKData
    result = []
    
    with open(os.path.join(gMDPath, 'MetaData.txt'), 'w') as f:
        print('THIS_SUBJ', '=', subj, file = f)

        print('Save login data...', end = '')
        for i in range(0, len(keys), 2):
            createAttribute(f, keys[i], loginData[keys[i]])
            createAttribute(f, keys[i + 1], loginData[keys[i + 1]])
            print('', file = f)
        print('[OK]')

        print('Save personal data...', end = '')
        for i in range(len(personalKeys)):
            createAttribute(f, personalKeys[i], personalData[i])
        print('', file = f)
        print('[OK]')

        print('Save synched Tuts...', end = '')
        for i in range(len(synchedTuts)):
            tut = synchedTuts[i]
            tut['ID'] = createTutoriumId(i, tut)
            result.append(tut)
            print(tut['ID'], end='...')
            print(createTutoriumMData(i, tut), file = f)
        print('', file = f)
        print('[OK]')

        print('Save Moodle data...', end = '')
        for i in range(len(moodleKeys)):
            createAttribute(f, moodleKeys[i], moodleData[i], secure = False)
        print('', file = f)
        print('[OK]')

        print('Create Mail-Templates...', end = '')
        print('MAIL_ITEMPLATE', '=', createInfoTemplate(gMDPath), file = f)
        print('MAIL_RTEMPLATE', '=', createReturnTemplate(gMDPath), file = f)
        print('[OK]')
        
    return result

def createMetaDataFile(gMDPath):
    subj = input('Please insert E-Mail-Tag (like "ALDA-17"): ')
    
    #==========================================================================

    loginData = getLoginDataFromUser()
    
    #==========================================================================

    my_fname = input('Please insert ur First Name: ')
    my_lname = input('Please insert ur Last Name: ')
    my_mail = input('Please insert ur E-Mailaddress: ')
    
    personalData = (my_fname, my_lname, my_mail)
    
    #==========================================================================

    print('Configure MÜSLI data')
    print('-' * 30)
    
    synchedTuts = getSynchedTutsFromUser(loginData['MÜSLI_USER'], 
                                         loginData['MÜSLI_PASSW'])
    
    print('')

    #==========================================================================
    print('Configure Moodle data')
    print('-' * 30)

    moodleData = getMoodleDataFromUser(loginData['MOODLE_USER'], 
                                       loginData['MOODLE_PASSW'])
    print('')

    #==========================================================================

    keys = ('MÜSLI_USER', 'MÜSLI_PASSW', 'MOODLE_USER', 'MOODLE_PASSW', 'MAIL_USER', 'MAIL_PASSW')
    personalKeys = ('MY_FNAME', 'MY_LNAME', 'MY_MAIL')
    moodleKeys = ('FACILITY', 'SUB_FACILITY', 'COURSE', 'COURSE_LINK')

    result = writeToMetaData (gMDPath, subj, 
                              (keys, loginData), 
                              (personalKeys, personalData), 
                              synchedTuts, 
                              (moodleKeys, moodleData))

    return result

def modifyMetaData (gMDataPath):
    keys = ('MÜSLI_USER', 'MÜSLI_PASSW', 'MOODLE_USER', 'MOODLE_PASSW', 'MAIL_USER', 'MAIL_PASSW')
    personalKeys = ('MY_FNAME', 'MY_LNAME', 'MY_MAIL')
    moodleKeys = ('FACILITY', 'SUB_FACILITY', 'COURSE', 'COURSE_LINK')
    
    # very slow cuz every readAttribute opens and cloeses fd on its own
    subj = readAttribute(gMDataPath, 'THIS_SUBJ')
    loginData = {x:readAttribute(gMDataPath, x) for x in keys}
    personalData = [readAttribute(gMDataPath, x) for x in personalKeys]
    synchedTuts = getTutMetaInfo(gMDataPath)
    moodleData = [readAttribute(gMDataPath, x) for x in moodleKeys]
    
    while True:
        print()
        print('=' * 30)
        print("""MetaData - Content:
            00 Mail-Tag
            01 MÜSLI-Account
            02 Moodle-Account
            03 Mail-Account
            04 Personal data
            05 Tutorial Infos
            06 Moodle Data
        """)
        
        inp = input("What do u want to modify \n(Type index or A for 'Apply Changes': ")
                
        if inp == 'A':
            return writeToMetaData (gMDataPath, subj, 
                              (keys, loginData), 
                              (personalKeys, personalData), 
                              synchedTuts, 
                              (moodleKeys, moodleData))
          
        inp = int(inp)
            
        if inp == 0:
            subj = input('Please insert E-Mail-Tag (like "ALDA-17"): ')
            
        elif inp == 1:
            loginData = {**loginData, 
                         **getLoginDataFromUser(platforms = ['Müsli'])}
    
        elif inp == 2:
            loginData = {**loginData, 
                         **getLoginDataFromUser(platforms = ['Moodle'])}
    
        elif inp == 3:
            loginData = {**loginData, 
                         **getLoginDataFromUser(platforms = ['Mail'])}
    
        elif inp == 4:
            my_fname = input('Please insert ur First Name: ')
            my_lname = input('Please insert ur Last Name: ')
            my_mail = input('Please insert ur E-Mailaddress: ')
            
            personalData = (my_fname, my_lname, my_mail)
            
        elif inp == 5:
            print('Configure MÜSLI data')
            print('-' * 30)
    
            synchedTuts = getSynchedTutsFromUser(loginData['MÜSLI_USER'], 
                                         loginData['MÜSLI_PASSW'])
    
            print('')
            
        elif inp == 6:
            print('Configure Moodle data')
            print('-' * 30)

            moodleData = getMoodleDataFromUser(loginData['MOODLE_USER'], 
                                       loginData['MOODLE_PASSW'])
            print('')
            
        else:
            print("Input '%s' is not supported!" % inp)
        
                
    
    

#==============================================================================
# load from MetaData.txt
#==============================================================================

def getMetaDataPath(gMDataPath):
    return os.path.join(gMDataPath, 'MetaData.txt')


def readAttribute(gMDataPath, key):
    with open(getMetaDataPath(gMDataPath), 'r') as fd:
        for line in fd:
            if line.startswith(key):
                val = line.split('=')[1].strip()
                if rcompile('>(\d+|)*').match(val):
                    return modify(val, reverse = True)
                else:
                    return val

def getTutIDs(gMDataPath):
    result = []
    with open(getMetaDataPath(gMDataPath), 'r') as file:
         for line in file:
            if line.startswith('|'):
                result.append(line.split('|')[1].strip())

    return result

def getTutLinksFromFile(gMDataPath):
    result = []
    with open(getMetaDataPath(gMDataPath), 'r') as file:
        for line in file:
            if line.startswith('|'):
                cols = line.split('|')[1:-1]
                result.append({'ID':cols[0].strip(), 'Link':cols[5].strip()})

    return result

def getTutMetaInfo(gMDataPath):
    result = []
    columnKeys = ['ID', 'Day', 'Time', 'Place', 'Subject', 'Link']

    with open(getMetaDataPath(gMDataPath), 'r') as file:
        for line in file:
            if line.startswith('|'):
                cols = line.split('|')[1:-1]
                tmp = {}
                for i in range(len(columnKeys)):
                    tmp[columnKeys[i]] = cols[i].strip()
                result.append(tmp)

    return result

def loadSubject(gMDataPath):
    with open(getMetaDataPath(gMDataPath), 'r') as file:
       for line in file:
           if line.startswith('THIS_SUBJ'):
               return line.split('=')[1].strip()

    return 'UNKNOWN'

def loadUserFrom(gMDataPath, accName):
    keys = []

    if accName == 'MÜSLI':
        keys = ['MÜSLI_USER', 'MÜSLI_PASSW']

    elif accName == 'MOODLE':
        keys = ['MOODLE_USER', 'MOODLE_PASSW']

    elif accName == 'MAIL':
        keys = ['MAIL_USER', 'MAIL_PASSW']

    else:
        raise ValueError('Unknown account %s' % accName)

    return (readAttribute(gMDataPath, keys[0]), readAttribute(gMDataPath, keys[1]))

def getEmailTuple(gMDataPath):
    return (readAttribute(gMDataPath, 'MY_FNAME'),
            readAttribute(gMDataPath, 'MY_MAIL'))

def getInfoTemplatePath(gMDataPath):
    with open(getMetaDataPath(gMDataPath), 'r') as file:
       for line in file:
           if line.startswith('MAIL_ITEMPLATE'):
               return line.split('=')[1].strip()

    return None

def getReturnTemplatePath(gMDataPath):
    with open(getMetaDataPath(gMDataPath), 'r') as file:
       for line in file:
           if line.startswith('MAIL_RTEMPLATE'):
               return line.split('=')[1].strip()

    return None

#==============================================================================
# create Tutxx_MuesliData
#==============================================================================

def createTutoriumList(tutpath, tut):
    acc = loadUserFrom(os.path.dirname(tutpath), 'MÜSLI')
    with MuesliApi(acc) as muesli:
        with open(tutpath, 'w') as file:
            muesli.generateMetadataTable(tut, stream = file)

def getStudentFromMUESLI(gMDataPath, tid):
    path = os.path.join(gMDataPath, tid + '_MuesliData.txt')
    valid = lambda x: x.startswith('+-')

    res = []

    with open(path, 'r') as file:
        lastLine = None
        for line in file:
            if valid(line):
                cols = [x.strip() for x in lastLine.split('|')]
                res.append(Student(tid = tid, name = cols[1], mail = cols[2], subject = cols[3], status = 'Local'))
            lastLine = line

    return res


#==============================================================================
# load data from Imported and Exported
#==============================================================================

def getImportedStudents(gMDataPath):
    path = os.path.join(gMDataPath, 'Imported.txt')
    valid = lambda x: x.startswith('+-')
    res = []

    with open(path, 'r') as file:
        lastLine = None
        for line in file:
            if valid(line):
                cols = [x.strip() for x in lastLine.split('|')]
                res.append(Student(tid = cols[1], name = cols[2], 
                                   mail = cols[3], subject = cols[4], status = 'Imported', 
                                   extTut = cols[7]))
            lastLine = line

    return res

def getExportedStudents(gMDataPath):
    path = os.path.join(gMDataPath, 'Exported.txt')
    valid = lambda x: x.startswith('+-')
    res = []

    with open(path, 'r') as file:
        lastLine = None
        for line in file:
            if valid(line):
                cols = [x.strip() for x in lastLine.split('|')]
                res.append(Student(tid = cols[1], name = cols[2], 
                                   mail = '', status = 'Exported'))
            lastLine = line

    return res


#==============================================================================
# create Imported.txt
# create Exported.txt
#==============================================================================

def createDivider(maxs, corner = '+', segment = '-'):
    res = corner

    for i in range(len(maxs)):
        res += segment * (maxs[i] + 2) + corner

    return res

def createRow(columns, maxs, divider = '|', divbuf = ' '):
    res = divider

    for i in range(len(maxs)):
        res += divbuf + columns[i].rjust(maxs[i]) + divbuf + divider

    return res

def getStudentPairFromUser(filename, studRefList):
    students = []
    fm = FolderManager()
    divider = '~' * 35

    while input('Want to add a student to %s? (Y|n)' % filename) == 'Y': 
        csg  = ConsoleStudentGetter(fm, includeExt = False)
        csg2 = ConsoleStudentGetter(fm, includeExt = True)
        
        print(divider)
        print('Insert Pair of students:\n\
              \t+ Name of the partner in ur tutorial \n\
              \t  (press Enter if there is no partner in ur tutorial) \n\
              \t+ Name of the student u want to import ')
              
        print('\nName of the partner in ur tutorial:')
        mStudent = csg.readStudent(allowEmpty = True)
        print(mStudent)
        print('Name of the imported student:')
        eStudent = csg2.readStudent()
        print(eStudent)
        eStudent['TID'] = mStudent['TID'] if mStudent != None else 'Tut_99'
        print(eStudent)
        print('Pair << %s, %s >>' %  ('NONE' 
                                          if mStudent == None 
                                          else mStudent['Name'],
                                      eStudent['Name']))
        print(divider)
        
        students.append(eStudent)
    print(students)
    return students

def nonEmptyInput(msg, value = ''):
    userInput = input(msg)
    return userInput if len(userInput) == 0 else value

def removeImportedStudents(students):
    res = [x for x in students]
    
    while True:
        if len(res) == 0:
            print('There are no imported students!')
            return res
            
        for index, student in enumerate(students):
            print('%s %s' % (str(index).zfill(2), student['Name']))
        
        index = int(input('Type the index of the student u want to remove.'))
        
        if index < 0:
            break
        student = students[index]
        
        # remove student from list
        if input('Do u want to remove %s from the list of imported \
                 students? (Y|n)' % student['Name']) == 'Y':
            res = res[0:index] + res[index + 1:]
            print()
            continue
    
    return res


def writeImportFile(path, students):
    print('writeImportFile (%s, %s)' % (path, students))
    columnNames = Student.getKeys()
    maxs = [len(x) for x in columnNames]
    
    for student in students:
        keys = Student.getKeys()
        print(student)
        for i in range(len(maxs)):
            print(keys[i], student[i], student[keys[i]])    
            if maxs[i] < len(student[i]):
                maxs[i] = len(student[i])
                    
    print('Create %s...' % os.path.basename(path), end = '')
    with open(path, 'w') as imp:
        p = lambda x: print(x, file = imp)
        
        divider = createDivider(maxs)
        headerDiv = createDivider(maxs, segment = '=')

        p(headerDiv)
        p(createRow(columnNames, maxs))
        p(headerDiv)

        for student in students:
            p(createRow(student, maxs))
            p(divider)
            
    print('[OK]')
                    
# Todo change to working path and make second param 'mode' which should replace
# the userinput in this function => more modular
def createImportFile(path):
    filename = os.path.basename(path)
    tids = getTutIDs(os.path.dirname(path))

    # already known students from tutroials
    studRefList = []
    for tid in tids:
        studRefList += getStudentFromMUESLI(os.path.dirname(path), tid)

    if os.path.exists(path):
        # Imported.txt already existing
        userInput = input(
                '''Do u want to modify \'%s\'? Type on of following options:
                o|O for OVERRIDE
                a|A for APPEND
                r|R for REMOVE
                (.*) for NO CHANGES\n\n''' % filename).lower()
            
        if userInput == 'a':
            tup = lambda x : (x['TID'], x['Name'], x['Mail'], x['ExtTut'])
            students = [tup(x) for x in getImportedStudents(os.path.dirname(path))]
            print('Current state:')
            for index, value in enumerate(students):
                print(str(index).zfill(2), value[1])
            
            students += getStudentPairFromUser(filename, studRefList)
            
            print(students)
        
        elif userInput == 'o':
            students = getStudentPairFromUser(filename, studRefList)
            
        elif userInput == 'r':
            students = removeImportedStudents(
                           getImportedStudents(
                                   os.path.dirname(path)))
        else:
            print('Nothing to change - skip')
            return False
        
        writeImportFile(path, students)
            
    else:
        # initial creation
        print("No '%s' found - start creating... " % filename)
        
        students = getStudentPairFromUser(filename, studRefList)
        writeImportFile(path, students)


    return True

def createExportFile(path):
    columnNames = ['TID', 'NAME']
    filename = os.path.basename(path)
    tids = getTutIDs(os.path.dirname(path))

    if os.path.exists(path):
        if input('Override \'%s\'? (Y|n)' % filename) != 'Y':
            print('Skipped')
            return False

    # already known students from tutroials
    studs = []
    for tid in tids:
        studs += getStudentFromMUESLI(os.path.dirname(path), tid)
    filt = StudentFilter(studs)

    print('Create %s' % filename)
    with open(path, 'w') as imp:
        students = []
        maxs = []
        for i in range(len(columnNames)):
            maxs.append(len(columnNames[i]))

        while input('Want to add a student to %s? (Y|n)' % filename) == 'Y':
            vals = []
            student = None

            while True:
                nm = input('Insert name of student which u want to export: ')
                student = filt.findStudentByName(nm)
                if len(student) == 1:
                    student = student[0]
                    break

                elif len(student) > 1:
                    student = chooseFromList(student, cdiscr='students', iSent='Choose student by index: ')
                    break

                else:
                    print("Didn't find name. Please try again.")

            vals.append(student['TID'])
            vals.append(student['Name'])
            students.append(tuple(vals))
            print()

        for student in students:
            for i in range(len(maxs)):
                if maxs[i] < len(student[i]):
                    maxs[i] = len(student[i])

        divider = createDivider(maxs)
        headerDiv = createDivider(maxs, segment = '=')

        p = lambda x: print(x, file = imp)
        p(headerDiv)
        p(createRow(columnNames, maxs))
        p(headerDiv)

        for student in students:
            p(createRow(student, maxs))
            p(divider)

    return True

#==============================================================================
# create ExternalStudents.txt
#==============================================================================

def createExternalStudentsList (gMDataPath):
    with MuesliApi(acc = loadUserFrom(gMDataPath, 'MÜSLI')) as mapi:
        info = mapi.getCurrentTutorials()
        #print(info)
        subject = info[0]['Subject']
        mapi.moveToTutorialMainPage(subject)
        #print(mapi.curURL)
    
        tutInfos = mapi.findExternalTutorialData(info[0]['Subject'], 
                        readAttribute(gMDataPath, 'MY_FNAME')
                        + ' ' 
                        + readAttribute(gMDataPath, 'MY_LNAME'))
    
        keys = ['TID', 'Day', 'Time', 'Place', 'Subject', 'Link', 'Tutor']
        extTutRows = []
    
        for index, tutInfo in enumerate(tutInfos):
            #print(index)
            tid = 'Ext_%s' % str(index).zfill(2)
            tutInfo['TID'] = tid
            tutInfo['Subject'] = subject
            extTutRows.append(tutInfo)
            
            maxs = getMaximumColumnSizes(extTutRows, keys)
    
            tutStud = {x['Tutor']:[] for x in extTutRows}
    
            with open(pjoin(gMDataPath, 'ExternalTutorials.txt'), 'w') as fd:
                studList = []
                for tutInfo in extTutRows:
                    print('|', tutInfo['TID'].rjust(maxs[0]), '|', tutInfo['Day'].rjust(maxs[1]),
                                     '|', tutInfo['Time'].rjust(maxs[2]), '|', tutInfo['Place'].rjust(maxs[3]),
                                     '|', subject.rjust(maxs[4]), '|', tutInfo['Link'].rjust(maxs[5]), '|', 
                                     tutInfo['Tutor'].rjust(maxs[6]), '|', 
                                     file = fd)
        
            
                    studentsData = mapi.getStudentsMetaData(tutInfo['Link'])
        
                    for studentData in studentsData:
                        student = Student(tutInfo['TID'], studentData['Name'], studentData['Mail'])
                        student['ExtTut'] = tutInfo['Tutor']
                        student['Status'] = 'External'
                        student['Subject'] = studentData['Subject']
                
                        studList.append(student)
                        print(student)
                
                    tutStud[tutInfo['Tutor']].append(studList)
                    studList = []
            
        with open(pjoin(gMDataPath, 'ExternalStudentsList.txt'), 'w') as fd:
            listEntries = []
        
            for tutor, groups in tutStud.items():
                print(tutor, len(groups), [len(group) for group in groups])
                for group in groups:
                    print('Groupsize: %s' % str(len(group)))
                    for student in group:
                        listEntries.append(student)
                    
            maxs = getMaximumColumnSizes(listEntries, Student.getKeys())
        
            for student in sorted(listEntries, key = lambda x: x['TID']):
                print('| %s |' % ('|'.join(
                        [' %s ' % str(student[key]).rjust(maxs[index]) 
                        for index, key in enumerate(student.getKeys())])),
                    file = fd)
    
def getETutMetaInfo (gMDataPath):
    result = []
    columnKeys = ['ID', 'Day', 'Time', 'Place', 'Subject', 'Link', 'ExtTut']
    
    with open(pjoin(gMDataPath, 'ExternalTutorials.txt'), 'r') as fd:
        for line in fd:
            #print(line[1:-2].split('|'))
            result.append({columnKeys[index]:x.strip() 
                            for index, x in enumerate(line[1:-2].split('|'))})
            
    return result
    
    
def getETutIDs (gMDataPath):
    return [x['ID'] for x in getETutMetaInfo(gMDataPath)]

def getETutors (gMDataPath):
    return [x['ExtTut'] for x in getETutMetaInfo(gMDataPath)]
            
    
def getExternalStudents (gMDataPath, etid = '*', extTut = '*'):
    splitInParts = lambda x: [p for p in x.split(';') if p]
    
    rows = []
    keys = Student.getKeys()
    
    with open(pjoin(gMDataPath, 'ExternalStudentsList.txt'), 'r') as fd:
        for row in fd:
            rows.append({keys[index]:col.strip() for index, col in enumerate(row[1:-2].split('|'))})
            
    for i in range(len(rows)):
        rows[i] = Student.fromDict(rows[i])
    
    etids = splitInParts(etid) if etid != '*' else getETutIDs(gMDataPath)
    extTuts = splitInParts(extTut) if extTut != '*' else getETutors(gMDataPath)
    
    return [x for x in rows if x['TID'] in etids and isNameIn(x['ExtTut'], extTuts)]


#==============================================================================
# create StudentsList.txt
#==============================================================================

def createStudentsList(gMdataPath, ignore = False):
    # Student (TID, Name, Mail, Subject, Status, Active, Status, ExtTut)
    print('createStudentsList(%s)' % gMdataPath)
    path = os.path.join(gMdataPath, 'StudentsList.txt')
    studs = []
    tmp = []
    
    if not ignore:
        studs = getExportedStudents(gMdataPath)
        tmp = getImportedStudents(gMdataPath)

    for tid in getTutIDs(gMdataPath):
        tmp2 = []
        for stud in getStudentFromMUESLI(gMdataPath, tid):
            for r in studs:
                if r.name == stud.name and r.tid == stud.tid:
                    stud.status = r.status
                    stud.extTut = r.extTut
            tmp2.append(stud)
        tmp += tmp2

    studs = sorted(tmp, key=lambda x: (x['TID'], x['Name']))

    keys = Student.getKeys()
    maxs = []
    for i in range(len(keys)):
        maxs.append(len(keys[i]))

    for student in studs:
        for i in range(len(maxs)):
            if maxs[i] < len(str(student[keys[i]])):
                maxs[i] = len(student[keys[i]])

    divider = createDivider(maxs)
    headerDiv = createDivider(maxs, segment = '=')

    with open(path, 'w') as f:
        p = lambda x: print(x, file = f)

        p(headerDiv)
        p(createRow(keys, maxs))
        p(headerDiv)

        for student in studs:
            p(createRow([str(x) for x in tuple(student)], maxs))
            p(divider)

def getStudents(gMdataPath, tid = '*', status = '*'):
    tids = getTutIDs(gMdataPath)
    stati = ['Exported', 'Local', 'Imported']

    preCheck = lambda x: x[1:] if x.startswith(';') else x
    postCheck = lambda x: x[:-1] if x.endswith(';') else x

    tid = postCheck(preCheck(tid))
    status = postCheck(preCheck(status))

    if tid != '*':
        tids = tid.split(';')

    if status != '*':
        stati = status.split(';')

    path = os.path.join(gMdataPath, 'StudentsList.txt')
    keys = Student.getKeys()
    valid = lambda x: x.startswith('+-')
    students = []

    with open(path, 'r') as file:
        lastLine = None
        for line in file:
            if lastLine == None:
                lastLine = line
                continue

            if valid(line):
                cols = [x.strip() for x in lastLine.split('|')][1:-1] 
                student = Student(cols[0], cols[1], cols[2])
                for i in range(len(keys)):
                    student[keys[i]] = cols[i]

                if student['TID'] in tids and student['Status'] in stati:
                    students.append(student)

            lastLine = line

    return students

#==============================================================================

def isRoot(path):
    return os.path.exists(os.path.join(path, 'GlobalMetaData'))

def findRoot(path):
    if isRoot(path):
        return path

    while True:
        splits = os.path.split(path)
        if isRoot(splits[0]):
            return splits[0]

        elif splits[1] == '':
            return None

        else:
            path = splits[0]


#==============================================================================

class FolderManager(object):

    def __init__(self, path = os.getcwd()):
        self.root = findRoot(path)
        if self.root == None:
            raise ValueError('No valid root could be found in path %s' % path)
        self.__gMDataPath = os.path.join(self.root, 'GlobalMetaData')

    def getSubject(self):
        return loadSubject(self.__gMDataPath)

    def getMÜSLIAcc(self):
        return loadUserFrom(self.__gMDataPath, 'MÜSLI')

    def getMoodleAcc(self):
        return loadUserFrom(self.__gMDataPath, 'MOODLE')

    def getMailAcc(self):
        return loadUserFrom(self.__gMDataPath, 'MAIL')

    def getMyEmailData(self):
        return getEmailTuple(self.__gMDataPath)

    def getInfoTemplatePath(self):
        return getInfoTemplatePath(self.__gMDataPath)

    def getReturnTemplatePath(self):
        return getReturnTemplatePath(self.__gMDataPath)

    def getTFirstName (self):
        return readAttribute(self.__gMDataPath, 'MY_FNAME')

    def getTLastName (self):
        return readAttribute(self.__gMDataPath, 'MY_LNAME')

    #--------------------------------------------------------------------------
    def getTIDs(self):
        return getTutIDs(self.__gMDataPath)
    
    def getETIDs (self):
        return getETutIDs(self.__gMDataPath)
    #--------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------
    def getTutMetaInfo (self):
        return getTutMetaInfo(self.__gMDataPath)
    
    def getETutMetaInfo (self):
        return getETutMetaInfo(self.__gMDataPath)
    
    def getInfoForStudent (self, student):
        tid = student['TID']
        
        infos = None
        if student['Status'] == 'External':
            infos = self.getETutMetaInfo()
        
        else:
            infos = self.getTutMetaInfo()
            
        for info in infos:
            if info['ID'] == tid:
                return info
                
        return None
            
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def getDateFor (self, tid):
        print('getDateFor (%s)' % tid)
        if 'Ext' in tid:
            einfo = [x for x in self.getETutMetaInfo() if x['ID'] == tid][0]
            return (einfo['Day'], einfo['Time'])
        else:    
            info = [x for x in self.getTutMetaInfo() if x['ID'] == tid][0]
            return (info['Day'], info['Time'])
        
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def getStudents (self, tid, status = 'Local'):
        return getStudents(self.__gMDataPath, tid, status)
    
    def getEStudents (self, tutor, etid = '*'):
        return getExternalStudents(self.__gMDataPath, etid, tutor)
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    def getAllStudents(self, status = 'Local'):
        res = []
        print('#1', len(res))
        if 'External' in status or status == '*':
            res += getExternalStudents(self.__gMDataPath)
            print('#2', len(res))
            
        print('#3', len(res + getStudents(self.__gMDataPath, '*', status)))
        return res + getStudents(self.__gMDataPath, '*', status)
    #--------------------------------------------------------------------------
    
    #--------------------------------------------------------------------------
    def findStudentByName(self, name, status = 'Local;Exported'):
        studs = self.getStudents(tid = '*', status = status)
        
        if 'External' in status or status == '*':
            studs += self.getEStudents('*')
        
        #return findStudentInList(name, studs)
        return StudentFilter(studs).findStudentByName(name)
    
    #--------------------------------------------------------------------------

#==============================================================================
