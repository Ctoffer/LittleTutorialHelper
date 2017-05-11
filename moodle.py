#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 12:52:08 2017

@author: christopher
"""

from bs4 import BeautifulSoup
from re import compile as rcompile
from requests import Session
import requests # only needed for requests.codes.ok - TODO find more elegant way
from os.path import join as pjoin

from account_exceptions import LoginException
from account_exceptions import LogoutException


"""
    Read-only-data-storage class
    This class represents submission data
"""
class Submission(object):
    
    def __init__ (self, name, mail, submissionState, overdue, fileLink, fileName):
        self.__name = name
        self.__mail = mail
        self.__subState = submissionState
        self.__overdue = overdue
        self.__fileLink = fileLink
        self.__fileName = fileName
        
    # dict-like read access
    def __getitem__ (self, key):
        if key == 'Name':
            return self.__name
        
        elif key == 'Mail':
            return self.__mail
        
        elif key == 'SubState':
            return self.__subState
        
        elif key == 'Overdue':
            return self.__overdue
        
        elif key == 'Link':
            return self.__fileLink
        
        elif key == 'FileName':
            return self.__fileName
    
    @staticmethod    
    def getKeys():
        return ['Name', 'Mail', 'SubState', 'Overdue', 'Link', 'FileName']

    
    def __iter__(self):
        keys = self.getKeys()
        for i in range(len(keys)):
            yield self[keys[i]]

class MoodleApi(object):
    
    def __init__ (self, acc = ('User', 'Password')):
        self.__acc = acc
        self.__baseURL = 'https://elearning2.uni-heidelberg.de'
        self.__session = None
        self.curURL = None
        self.__sesskey = None
        
    def login (self):
        print('Moodle - login()')
        self.__session = Session()
        website = self.__baseURL + "/login/index.php"
        r = self.__session.post(website, data = dict(username = self.__acc[0], password = self.__acc[1]))
        
        if r.url == self.__baseURL + '/login/index.php' or r.status_code != requests.codes.ok:
            raise LoginException('Login failed! - Check ur internet connection, username and password')
        self.curURL = str(r.url)
        
        soup = BeautifulSoup(self.__session.get(self.curURL).text, 'html.parser')
        start = soup.text.find('sesskey')
        # "sesskey":"adsasnin", - pattern
        self.__sesskey = soup.text[start - 1:].split(',')[0].split(':')[1][1:-1]
        
    def __enter__ (self):
        self.login()
        return self

    def logout (self):
        print('Moodle - logout()')
       
        website = self.__baseURL + '/login/logout.php?sesskey=%s' % self.__sesskey
        r = self.__session.post(website)
        
        self.__session.close()
        self.__session = None
        self.__sesskey = None
        self.curURL = None
        
        if r.status_code != requests.codes.ok:
            raise LogoutException('Logout Failed - Session was closed!')
            
    def __exit__ (self, type, value, traceback):
        self.logout()
        
    def moveToStart (self):
        self.curURL = self.__baseURL
        
    def listFacilities (self):
        self.moveToStart()
        soup = BeautifulSoup(self.__session.get(self.curURL).text, 'html.parser')
        rows = soup.findAll('a', href = rcompile('http://elearning2\.uni-heidelberg\.de/course/category.php\?id=\d+'))
        
        res = []
        
        for row in rows:
            res.append({'ID':row['href'].split('?id=')[1], 'Name':row.text, 'Link':row['href']})
        
        return res
            
            
    def getFacility (self, partitialName = 'Informatik'):
        for fac in self.listFacilities():
            if partitialName in fac['Name']:
                return fac
            
        return None
    
    def moveToFacility (self, partitialName = 'Informatik'):
        self.curURL = self.__session.get(self.getFacility(partitialName)['Link']).url
        
    def listSubFacilitiesOf (self, partitialName = 'Informatik'):
        self.moveToFacility(partitialName)
        r = self.__session.get(self.curURL)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.findAll('a', href = rcompile('https://elearning2\.uni-heidelberg\.de/course/index\.php\?categoryid=\d+$'), attrs={'itemprop':False})
        
        res = []
        
        for row in rows:
            res.append({'ID':row['href'].split('?categoryid=')[1], 'Name':row.text, 'Link':row['href']})
        
        return res
    
    def getSubFacility (self, pFacName = 'Informatik', pSFacName = 'Informatik'):
        for subFac in self.listSubFacilitiesOf(pFacName):
            if pSFacName in subFac['Name']:
                return subFac
            
        return None
    
    def listCoursesOf (self, pFacName = 'Informatik', pSFacName = 'Informatik'):
        subFacLink = self.getSubFacility(pFacName, pSFacName)['Link']        
        r = self.__session.get(subFacLink)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        elem = soup.find('div', attrs={'class':'course_category_tree clearfix '})
        rows = elem.findAll('a', href = rcompile('https://elearning2\.uni-heidelberg\.de/course/view\.php\?id=\d+'))
        
        return [x.text for x in rows]
    
    def findCourse (self, pFacName = 'Informatik', pSFacName = 'Informatik', course = 'Datenstrukt'):
        subFacLink = self.getSubFacility(pFacName, pSFacName)['Link']        
        r = self.__session.get(subFacLink)
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.findAll('a', href = rcompile('https://elearning2\.uni-heidelberg\.de/course/view\.php\?id=\d+'))
        
        for row in rows:
            if course in row.text:
                return row['href']
            
    def moveToCourse (self, courseData = ('Informatik', 'Informatik', 'Datenstrukt'), link = ''):
        if link == '':
            self.curURL = self.findCourse(courseData[0], courseData[1], courseData[2])
        else:
            self.curURL = link

            
    def moveToAllSubmissionsInCourse (self, sheetNr):
        r = self.__session.get(self.curURL)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        anchors = soup.findAll('a', onclick = True, href = True)

        text = 'Übungsblatt %i Aufgabe' % sheetNr
        fil = lambda x: [a for a in x if text == a.text][0]
        # TODO random shit
        #print('href')
        #for a in anchors:
            #print(a.text)
        sheetLink = fil(anchors)['href']
        
        if sheetLink == None:
            raise ValueError('The exercise sheet was not found')

        btnAs = BeautifulSoup(self.__session.get(sheetLink).text, 'html.parser').findAll('a', href=True, attrs={'class':'btn'}, text='Alle Abgaben anzeigen')
        if len(btnAs) == 1:
            self.curURL = btnAs[0]['href']
            
        elif len(btnAs) < 1:
            raise ValueError('No btn found!')
            
        else:
            raise ValueError('Too much btns found!')
        
        soup = BeautifulSoup(self.__session.get(self.curURL).text, 'html.parser')
        classAttrs = soup.find('body').attrs['class']
        formData = {}
        for attr in classAttrs:
            if 'context-' in attr:
                formData['contextid'] = attr.split('-')[1]
            elif 'cmid-' in attr:
                formData['id'] = attr.split('-')[1]
                
  
        # href contains a link where the userid is  a subsequence of
        # split the href at ?. right side contains userid (uid)
        # pattern of uidElem = id=<num>
        uidElem = soup.find('a', href = True, attrs = {'class':'icon menu-action', 'role':'menuitem', 'data-title':'profile,moodle'})
        
        formData['userid'] = uidElem['href'].split('?')[1].split('=')[1]
        formData['action'] = 'saveoptions'
        formData['sesskey'] = self.__sesskey
        formData['_qf__mod_assign_grading_options_form'] = '1'
        formData['mform_isexpanded_id_general'] = '0'
        formData['perpage'] = '-1'
        formData['downloadasfolders'] = '1'
        
        self.__session.post(self.curURL, data = formData)
        
    def extractSubscriptionRowsFor (self, courseData = ('Informatik', 'Informatik', 'Datenstrukt'), link = '', sheetNr = 1, studFilter = None):
        self.moveToCourse(courseData, link)
        self.moveToAllSubmissionsInCourse(sheetNr)
        
        data = []
        soup = BeautifulSoup(self.__session.get(self.curURL).text , 'html.parser')
        table = soup.findAll('table', attrs={'class':'flexible generaltable generalbox'})[0]
        rows = table.findChildren('tr')
    
        # Row structure
        # Cell 0: CheckBox 
        # Cell 1: Picture
        # Cell 2: Name                   <<<
        # Cell 3: E-Mail
        # Cell 4: State                  <<<
        # Cell 5: Grade
        # Cell 6: Edit
        # Cell 7: Last Modified
        # Cell 8: Filelink               <<<
        # Cell 9 - 13: Feedbackstuff
        
        for row in rows:
            name = row.find('td', attrs={'class':'cell c2'})
            if name != None:
                name = name.find('a').text
            else:
                continue
            
            mail = row.find('td', attrs={'class':'cell c3 email'})
            if mail != None:
                mail = mail.text
            
            date = row.find('td', attrs={'class':'cell c4'})
            if date == None:
                continue
            
            oDue = date.find('div', attrs={'class':'overduesubmission'})
            if oDue != None:
                oDue = oDue.text
            else:
                lSub = date.find('div', attrs={'class':'latesubmission'})
                oDue = '' if lSub is None else lSub.text
                
            subState = date.find('div').text
            
            submFile = row.find('td', attrs={'class':'cell c8'})
            if submFile == None:
                continue

            submFileAnchor = submFile.find('a', href=True)
            if submFileAnchor == None:
                continue
            submFileLink = submFileAnchor['href']
            submFileName = submFileAnchor.text
            
            # name, mail, submissionState, overdue, fileLink, fileName
            subm = Submission(name, mail, subState, oDue, submFileLink, submFileName)
            data.append(subm)

        return data if studFilter == None else studFilter.filterList(data)
            
    def downloadSubmissions (self, submissions, destDir):
        archives = []
        
        for submission in submissions:
            print('Downloading submission of %s in %s...' % (submission['Name'], pjoin(destDir, submission['FileName'])), end = '', flush = True)
            r = self.__session.get(submission['Link'], stream = True)
            
            if r.status_code == requests.codes.ok:
                archivePath = pjoin(destDir, submission['FileName'])
                
                with open(archivePath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size = 128):
                        f.write(chunk)
                    archives.append(f.name) 
                print('[OK]')
            else:
                print('Error @ %s - %s' % (submission['Name'], submission['Link']))
                
        return archives
