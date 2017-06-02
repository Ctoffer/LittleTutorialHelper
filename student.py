#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 01:33:09 2017

@author: christopher
"""

from sys import exit as sexit

class Student(object):

    def __init__(self, tid, name, mail, subject = '', status = 'Local', active = True, extTut = ''):
        self.tid = tid
        self.name = name
        self.mail = mail
        self.subject = subject
        self.status = status # Imported, Exported, Local
        self.active = active # important for feedback mails
        self.extTut = extTut


    def __getitem__(self, key):
        if key == 'TID' or key == 0:
            return self.tid

        if key == 'Name' or key == 1:
            return self.name

        elif key == 'Mail' or key == 2:
            return self.mail

        elif key == 'Subject' or key == 3:
            return self.subject

        elif key == 'Active' or key == 4:
            return self.active

        elif key == 'Status' or key == 5:
            return self.status

        elif key == 'ExtTut' or key == 6:
            return self.extTut

    # TODO yeah i fucked it up with the __hash__ 
    def __setitem__(self, key, value):
        if key == 'TID':
            self.tid = value

        if key == 'Name':
            self.name = value

        elif key == 'Mail':
            self.mail = value

        elif key == 'Subject':
            self.subject = value

        elif key == 'Active':
            self.active = value

        elif key == 'Status':
            self.status = value

        elif key == 'ExtTut':
            self.extTut = value


    @staticmethod
    def getKeys():
        return ['TID', 'Name', 'Mail', 'Subject', 'Active', 'Status', 'ExtTut']

    def __iter__(self):
        keys = self.getKeys()
        for i in range(len(keys)):
            yield self[keys[i]]

    def __str__(self):
        return '<TID: %s, Name: %s, Mail: %s, Subject: %s, Active: %s, Status: %s, ExtTut: %s>' % tuple(self)

    def __hash__(self):
        return hash(tuple(self))

    def __eq__(self, other):
        if other == None:
            return False
        
        return tuple(self) == tuple(other)

    def __ne__(self, other):
        return not(self == other)
    
    @staticmethod
    def fromDict(d):
        stud = Student(d['TID'], d['Name'], d['Mail'])
        for key in Student.getKeys()[3:]:
            if key in d:
                stud[key] = d[key]
        return stud


class ConsoleStudentGetter(object):
    def __init__(self, folderManager, includeExt = False):
        self.__fm = folderManager
        self.__iExt = includeExt

    def readStudent(self, initialGuess = '', allowEmpty = False):
        students = []
        state = 'Local;Exported;External' if self.__iExt else 'Local;Exported'

        while True:
            students = []
            if initialGuess != '':
                students = self.__fm.findStudentByName(initialGuess, status = state)
            else:
                guess = input('Name(part) of student: ')
                if guess == '' :
                    if allowEmpty:
                        return None
                    else:
                        print('You need to insert at least one letter!')
                        continue
                students = self.__fm.findStudentByName(guess, status = state)
                
            if len(students) > 1:
                print('Too much matches. Choose one result by index (Type -1 for retry): ')
                students = sorted(students, key = lambda x: x['Name'])
                for i in range(len(students)):
                    print(str(i).zfill(2), students[i]['Name'], end = '  ')
                    
                    if students[i]['ExtTut'] != '':
                        print('(%s)'  % students[i]['ExtTut'])
                    else:
                        print()

                index = int(input('Index: '))
                if index == -1:
                    initialGuess = ''
                    continue

                return students[index]

            elif len(students) == 1:
                return students[0]

            elif len(students) < 1:
                if input('No match found. Try again? (Y|n)') != 'Y':
                    sexit('Program terminated by User')
                else:
                    initialGuess = ''
                    
"""
    Compare two lists of nameparts.
    If an element of the left list is found in the right list, then a counter
    will be increased by one. If the counter is 2 or bigger than at least
    two name parts did match - mostly the first and last name.
"""
def cmpNameParts(left, right):
    #print('cmpNameParts (%s, %s)' % (left, right))
    if len(left) > len(right):
        return cmpNameParts(right, left)
    
    #print(left, right)
    count = 0
    
    for l in left:
        for r in right:
            if l == '' or r == '':
                continue
            if l in r or r in l:
                count += 1
            
    #print('count %s' % str(count))
    return len(left) == count # minimum match first and last name

"""
    If a list of nameparts contains german letters like äöü escape them
"""
def escapeName(name):
    escape = lambda x: x.replace('Ö', 'Oe').replace('Ä', 'Ae') \
                        .replace('Ü', 'Ue').replace('ö', 'oe') \
                        .replace('ä', 'ae').replace('ü', 'ue') \
                        .replace('ß', 'ss').capitalize()
    return escape(name)

def compareNames(name1, name2):
    #print('compareNames (%s, %s)' % (name1, name2))
    mod = lambda x : x.strip().split(' ')
    return compareNameParts(mod(name1), mod(name2))

def compareNameParts(nameParts1, nameParts2):
    #print('compareNameParts (%s, %s)' % (nameParts1, nameParts2))
    return cmpNameParts([escapeName(x) for x in nameParts1], 
                         [escapeName(x) for x in nameParts2])
    
def isNameIn(name, listOfNames):
    for rName in listOfNames:
        if compareNames(name, rName):
            return True
    return False

"""
    Filter class, which needs to be initialized with a reference list of
    students.
"""
class StudentFilter(object):
    
    def __init__ (self, refStudList):
        self.__refStudList = refStudList
        
    # filters an incoming list of dict-like objects
    def filterList (self, submissions):
        res = []
        indices = list(range(len(self.__refStudList)))
        
        for subm in submissions:
            for i in indices:
                student = self.__refStudList[i]
                # if the reference and the test value have the same mail,
                # then they are identic
                if subm['Mail'] == student['Mail']:
                    res.append(subm)
                    indices.remove(i) # remove index if student was found
                    break
                
                # otherwise compare name parts 
                # nameparts are the name splitted by space and each of this
                # parts capitalize is called (sometimes students are writing 
                # only lowercase
                elif compareNames(subm['Name'], student['Name']):
                    res.append(subm)
                    indices.remove(i)
                    break
                
        return res
    
    def findStudentByName (self, name):
        matchValue = {x:0 for x in self.__refStudList}

        perfectMatch = False

        for student in self.__refStudList:
            for namePart in name.split(' '):
                if namePart in student['Name']:
                    matchValue[student] += 1
                    perfectMatch = True
        
        mkNameparts = lambda s: [x.capitalize() for x in s.split(' ')]
        if not perfectMatch:
            
            for student in self.__refStudList:
                if compareNames(name, student['Name']):
                    matchValue[student] += len(mkNameparts(name))
                
                    
        matchValue = sorted([(k, v) for k,v in matchValue.items()],
                        key = lambda x: -x[1])
        maxCount = matchValue[0][1]

        return [x[0] for x in matchValue if (x[1] == maxCount and 
                x[1] > 0) or name == '']
                    
        