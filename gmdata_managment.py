#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 21:12:30 2017

@author: christopher
"""

import os
from re import compile as rcompile

import template_holder as RTH

from moodle import MoodleApi
from muesli import MuesliApi
from student import Student

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
    res += createTutoriumId(i, tut) + ' | '
    res += tut['Tag'].rjust(12) + ' | '
    res += tut['Zeit'] + ' | '
    res += tut['Ort'].rjust(20) + ' | '
    res += tut['Vorlesung'] + ' | '
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


def chooseFromList(li, cdiscr = 'elements', iSent = 'Choose index (type -1 to try again): ', key = None):
    print('Found %i %s:' % (len(li), cdiscr))
    print(iSent)
    
    for i, v in enumerate(li):
        print(str(i).zfill(2), v if key == None else v[key])
    
    while True:
        index = int(input(iSent))
        if index == -1:
            continue
        print('')
        break
    
    return li[index]

def findStudentInList (name, studs):
    matchValue = {x:0 for x in studs}

    perfectMatch = False

    for student in studs:
        for namePart in name.split(' '):
            if namePart in student['Name']:
                matchValue[student] += 1
                perfectMatch = True

    if not perfectMatch:
        for student in studs:
            for namePart in name.split(' '):
               r, w = 0,0
               for i in range(len(namePart)):
                   if namePart[:-i] in student['Name']:
                       r += 1
                   else:
                       w += 1

                   if namePart[len(namePart) - i:] in student['Name']:
                       r += 1
                   else:
                       w += 1

               if r/w > 1:
                   matchValue[student] += 1


    matchValue = sorted([(k, v) for k,v in matchValue.items()],
                        key = lambda x: -x[1])
    maxCount = matchValue[0][1]

    return [x[0] for x in matchValue if (x[1] == maxCount and x[1] > 0) or name == '']

def createMetaDataFile(gMDPath):
    subj = input('Please insert E-Mail-Tag (like "ALDA-17"): ')

    muesli_u = input('Please insert MÜSLI-Username: ')
    muesli_p = input('Please insert MÜSLI-Password: ')

    moodle_u = input('Please insert Moodle-Username: ')
    moodle_p = input('Please insert Moodle-Password: ')

    mail_u   = input('Please insert Mail-Username: ')
    mail_p   = input('Please insert Mail-Password: ')

    my_fname = input('Please insert ur First Name: ')
    my_lname = input('Please insert ur Last Name: ')
    my_mail = input('Please insert ur E-Mailaddress: ')

    keys = ('MÜSLI_USER', 'MÜSLI_PASSW', 'MOODLE_USER', 'MOODLE_PASSW', 'EMAIL_USER', 'EMAIL_PASSW')
    logins = (muesli_u, muesli_p, moodle_u, moodle_p, mail_u, mail_p)

    personalKeys = ('MY_FNAME', 'MY_LNAME', 'MY_MAIL')
    personalData = (my_fname, my_lname, my_mail)

    synchedTuts = []

    print('Configure MÜSLI data')
    print('-' * 30)
    with MuesliApi(acc = (muesli_u, muesli_p)) as muesli:
        tutorials = muesli.getCurrentTutorials()
        for tut in tutorials:
            print('Do u want to synch data from this tutorial:',
                  tut['Vorlesung'],
                  '(', tut['Tag'], tut['Zeit'], ')',
                  end = '')

            if input('(Y|n)') == 'Y':
                print('Added')
                synchedTuts.append(tut)
            else:
                print('Skipped')
    print('')

    #==========================================================================
    print('Configure Moodle data')
    print('-' * 30)

    moodleKeys = ('FACILITY', 'SUB_FACILITY', 'COURSE', 'COURSE_LINK')
    moodleFac = None
    moodleSubFac = None
    moodleCourse = None
    courseLink = None

    with MoodleApi(acc = (moodle_u, moodle_p)) as moodle:
        seq = 'Choose where ur tutorial is by index: '
        moodleFac = chooseFromList([x['Name'] for x in moodle.listFacilities()],
                                   cdiscr = 'facilities',
                                   iSent = seq)
        moodleSubFac = chooseFromList([x['Name'] for x in moodle.listSubFacilitiesOf(moodleFac)],
                                      cdiscr = 'subfacilities',
                                      iSent = seq)
        moodleCourse = chooseFromList(moodle.listCoursesOf(moodleFac, moodleSubFac),
                                      cdiscr = 'subfacilities',
                                      iSent = seq)
        moodle.moveToCourse (courseData = (moodleFac, moodleSubFac, moodleCourse))
        courseLink = moodle.curURL
        print('Your tutorial is located here: %s' % courseLink)
    print('')
    moodleData = (moodleFac, moodleSubFac, moodleCourse, courseLink)

    result = []

    with open(os.path.join(gMDPath, 'MetaData.txt'), 'w') as f:
        print('THIS_SUBJ', '=', subj, file = f)

        print('Save login data...', end = '')
        for i in range(0, len(keys), 2):
            createAttribute(f, keys[i], logins[i])
            createAttribute(f, keys[i + 1], logins[i + 1])
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
            result.append(tut)
            print(createTutoriumId(i, tut), end='...')
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
                if rcompile('>(\d+|)*'):
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

    elif accName == 'EMAIL':
        keys = ['EMAIL_USER', 'EMAIL_PASSW']

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
                                   mail = cols[3], status = 'Imported', 
                                   extTut = cols[4]))
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

def getStudentsFromUser(filename, studRefList):
    students = []

    while input('Want to add a student to %s? (Y|n)' % filename) == 'Y':
        vals = []
        student = None
        
        while True:
            nm = input('Insert name of partner which is in ur tutorial: ')
            student = findStudentInList(nm, studRefList)
        
            if len(student) == 1:
                student = student[0]
                
            elif len(student) > 1:
                student = chooseFromList(student,
                                         cdiscr='students', 
                                         iSent='Choose student by index: ',
                                         key = 'Name')
                
            else:
                print("Didn't find name. Please try again.")
                continue

            
            vals.append(student['TID'])
            vals.append(input('Insert name of the imported student: '))  
            vals.append(input('Insert e-Mail of the imported student: '))
            vals.append(input('Insert name of tutor of the imported student: '))

            students.append(tuple(vals))
            print()
            break
        
    return students

def nonEmptyInput(msg, value = ''):
    userInput = input(msg)
    return userInput if len(userInput) == 0 else value

def modifyImportedStudents(students):
    res = [x for x in students]
    
    while True:
        if len(res) == 0:
            print('There are no imported students!')
            return []
            
        for index, student in enumerate(students):
            print('%s %s' % (str(index).zfill(2), student['Name']))
        
        index = int(input('Type the index of the student u want to modify. '
                          'Type -1 if u completed modification.\n'))
        
        if index < 0:
            break
        student = students[index]
        
        # remove student from list
        if input('Want to remove this student from the list of imported students? (Y|n)') == 'Y':
            res.remove(student)
            print()
            continue
            
        else:
            # otherwise modify
            print('If u want to skip one of the following steps,'
                  'just press enter to continue.')
            tid = student['TID']
            name = nonEmptyInput('Enter name (%s): ' % student['Name'], student['Name'])
            mail = nonEmptyInput('Enter mail (%s): ' % student['Mail'], student['Mail']) 
            extTut = nonEmptyInput('Enter extTutor (%s): ' % student['ExtTut'], student['ExtTut']) 
            res.remove(student)
            res.append(Student(tid, name, mail, extTut = extTut))
        print()
    
    return res


def writeImportFile(path, students):
    columnNames = ['TID', 'NAME', 'MAIL', 'FROM-TUTOR']
    maxs = [len(x) for x in columnNames]
    
    for student in students:
            for i in range(len(maxs)):
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
                m|M for MODIFY (REMOVE)
                (.*) for NO CHANGES\n\n''' % filename).lower()
            
        if userInput == 'a':
            tup = lambda x : (x['TID'], x['Name'], x['Mail'], x['ExtTut'])
            students = [tup(x) for x in getImportedStudents(os.path.dirname(path))]
            print('Current state:')
            for index, value in enumerate(students):
                print(str(index).zfill(2), value[1])
            
            students += getStudentsFromUser(filename, studRefList)
            
            print(students)
            
            writeImportFile(path, students)
        
        elif userInput == 'o':
            students = getStudentsFromUser(filename, studRefList)
            writeImportFile(path, students)
            
        elif userInput == 'm':
            students = modifyImportedStudents(
                           getImportedStudents(
                                   os.path.dirname(path)))
        else:
            print('Nothing to change - skip')
            return False
            
    else:
        # initial creation
        
        students = getStudentsFromUser(filename, studRefList)
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
                student = findStudentInList(nm, studs)
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
# create StudentsList.txt
#==============================================================================

def createStudentsList(gMdataPath):
    # Student (TID, Name, Mail, Subject, Status, Active, Status, ExtTut)
    print('createStudentsList(%s)' % gMdataPath)
    path = os.path.join(gMdataPath, 'StudentsList.txt')
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
        return loadUserFrom(self.__gMDataPath, 'EMAIL')

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

    def getTIDs(self):
        return getTutIDs(self.__gMDataPath)

    def getTutMetaInfo (self):
        return getTutMetaInfo(self.__gMDataPath)

    def getDateFor (self, tid):
        info = [x for x in self.getTutMetaInfo() if x['ID'] == tid][0]
        return (info['Day'], info['Time'])

    def getStudents(self, tid, status = 'Local'):
        return getStudents(self.__gMDataPath, tid, status)

    def getAllStudents(self, status = 'Local'):
        return getStudents(self.__gMDataPath, '*', status)

    def findStudentByName(self, name, status = 'Local;Exported'):
        studs = self.getStudents(tid = ';'.join(self.getTIDs()), status = status)
        return findStudentInList(name, studs)


#==============================================================================
