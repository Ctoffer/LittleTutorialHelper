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
        if key == 'TID':
            return self.tid

        if key == 'Name':
            return self.name

        elif key == 'Mail':
            return self.mail

        elif key == 'Subject':
            return self.subject

        elif key == 'Active':
            return self.active

        elif key == 'Status':
            return self.status

        elif key == 'ExtTut':
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
        return tuple(self) == tuple(other)

    def __ne__(self, other):
        return not(self == other)


class ConsoleStudentGetter(object):
    def __init__(self, folderManager):
        self.__fm = folderManager

    def readStudent(self, initialGuess = ''):
        students = []

        while True:
            students = []
            if initialGuess != '':
                students = self.__fm.findStudentByName(initialGuess)
            else:
                students = self.__fm.findStudentByName(input('Name(part) of student: '))
                
            if len(students) > 1:
                print('Too much matches. Choose one result by index (Type -1 for retry): ')
                for i in range(len(students)):
                    print(str(i).zfill(2), students[i]['Name'])

                index = int(input('Index: '))
                if index == -1:
                    continue

                return students[index]

            elif len(students) == 1:
                return students[0]

            elif len(students) < 1:
                if input('No match found. Try again? (Y|n)') != 'Y':
                    sexit('Program terminated by User')
                    
"""
    Compare two lists of nameparts.
    If an element of the left list is found in the right list, then a counter
    will be increased by one. If the counter is 2 or bigger than at least
    two name parts did match - mostly the first and last name.
"""
def cmpNameParts(left, right):
    if len(left) > len(right):
        return cmpNameParts(right, left)
    
    #print(left, right)
    count = 0
    
    for l in left:
        if l in right:
            count += 1
            
    return count >= 2 # minimum match first and last name


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
                    indices.remove(i)
                    break
                
                # otherwise compare name parts 
                # nameparts are the name splitted by space and each of this
                # parts capitalize is called (sometimes students are writing 
                # only lowercase)
                mkNameparts = lambda s: [x.capitalize() for x in s['Name'].split(' ')]
                if cmpNameParts(mkNameparts(subm), mkNameparts(student)):
                    res.append(subm)
                    indices.remove(i)
                    break
                
        return res
