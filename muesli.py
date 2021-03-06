from bs4 import BeautifulSoup
import re
import requests
import sys

from account_exceptions import LoginException
from account_exceptions import LogoutException
from account_exceptions import TutNotFoundException
from util import getMaximumColumnSizes

from student import cmpNameParts
from student import compareNames

def createCreditDictionary(creditFile):
    result = {}
    
    with open(creditFile, 'r') as cFile:
        for line in cFile:
            cols = [x.strip() for x in line.split('|')[1:-1]]
            result[cols[0]] = cols[1:]
            
    return result

class MuesliApi(object):
    
    def __init__ (self, acc = ('user', 'passw')):
        self.__acc = acc
        self.baseURL = 'https://muesli.mathi.uni-heidelberg.de'
        self.session = None
        self.curURL = None

    def login (self):
        print('MÜSLI - login()')
        self.session = requests.Session()
        website = self.baseURL + "/user/login"
        r = self.session.post(website, data = dict(email = self.__acc[0], password = self.__acc[1]))
        if r.url == website or r.status_code != requests.codes.ok:
            raise LoginException('Login failed! - Check ur internet connection, username and password')
        self.curURL = str(r.url)
        
    def __enter__ (self):
        self.login()
        return self

    def logout (self):
        print('MÜSLI - logout')
        website = self.baseURL + '/user/logout'
        resultWeb = "https://muesli.mathi.uni-heidelberg.de/"
        r = self.session.post(website)
        self.session.close()
        self.session = None
        self.curURL = None

        if r.url != resultWeb or r.status_code != requests.codes.ok:
            raise LogoutException('Logout Failed - Session was closed!')
            
    def __exit__ (self, type, value, traceback):
        self.logout()

    def moveToStart (self):
        self.curURL = self.baseURL + '/start'
        
    def moveToTutorium (self, day, time):
        self.curURL = self.getTutorialInfoForDay(day, time)['Link']
        
    def moveToExcercise (self, day, time, sheetNr, link = None):
        if link == None:
            self.moveToTutorium(day, time)
        else:
            self.curURL = link
        soup = BeautifulSoup(self.session.get(self.curURL).text, 'html.parser')
        anchors = soup.findAll("a", href = re.compile("/exam/enter_points/.*"),
                               text=re.compile("(.*ü|Ü)bung " + str(sheetNr)))
        self.curURL = self.baseURL + anchors[0].get("href")

    def moveToPresented (self, day, time):
        self.moveToTutorium(day, time)
        soup = BeautifulSoup(self.session.get(self.curURL).text, 'html.parser')
        anchors = soup.findAll("a", href=re.compile("/exam/enter_points/.*"), text='Vorrechnen')
        self.curURL = self.baseURL + anchors[0].get("href")

    def getCurrentTutorialLinks (self):
        self.moveToStart()
        r = self.session.post(self.curURL)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        anchors = soup.findAll("a", href=re.compile("/tutorial/view/\d*"), title=False)
        result = []

        for i in range(0, len(anchors)):
            result.append(self.baseURL + anchors[i].get("href"))

        return result
    
    #==========================================================================
    # Advanced stuff for cross-over shit
    #==========================================================================
    
    def moveToTutorialMainPage (self, name):
        self.moveToStart()
        r = self.session.post(self.curURL)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        anchors = []
        for anchor in soup.findAll("a", href=re.compile("/lecture/view/\d*")):
            if anchor.text.strip() == name:
                anchors.append(anchor)
        
        self.curURL = self.baseURL + anchors[0].get("href")
        
    def findExternalTutorialData (self, subjectName, myName):
        self.moveToTutorialMainPage(subjectName)
        print(self.curURL)
        r = self.session.post(self.curURL)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table')
        res = []
        
        days = {"Mo" : "Montag",
                "Di" : "Dienstag",
                "Mi" : "Mittwoch",
                "Do" : "Donnerstag",
                "Fr" : "Freitag",
                "Sa" : "Samstag",
                "So" : "Sonntag"
                }
        
        keys = ['Day', 'Time', 'Place', 'Tutor', 'Link']
        
        for row in table.findAll('tr'):
            tds = row.findAll('td')
            if len(tds) == 0:
                continue
            
            entries = tds[0].text.strip().split(' ')\
                        + [tds[1].text.strip(), 
                           tds[3].text.strip(), 
                           self.baseURL + tds[5].find('a', href = True)['href']]
    
            entries[0] = days[entries[0]]
            if not compareNames(entries[3], myName):
                tutInfo = {}
                for i in range(len(entries)):
                    tutInfo[keys[i]] = entries[i]
                res.append(tutInfo)
        print(res)    
        return res
    
    def moveToExternalTutorium (self, infos = [], tutor = '', day = '', time = '', tid = None):
        for info in infos:
            if tid != None and info['TID'] == tid:
                self.curURL = info['Link']
                break
            
            elif compareNames(info['ExtTut'], tutor) \
                    and info['Day'] == day \
                    and info['Time'] == time:        
                self.curURL = info['Link']
                break
        
    
    def moveToExternalExcercise (self, subjectName, tutor, day, time, sheetNr):
        self.moveToExternalTutorium(subjectName, tutor, day, time)
        
        soup = BeautifulSoup(self.session.get(self.curURL).text, 'html.parser')
        anchors = soup.findAll("a", href = re.compile("/exam/enter_points/.*"),
                               text=re.compile("(.*ü|Ü)bung " + str(sheetNr)))
        
        self.curURL = self.baseURL + anchors[0].get("href")
            
    #==========================================================================

    def extractTutorialInfo (self, tutoralLink):
        r = self.session.post(tutoralLink)
        soup = BeautifulSoup(r.text, 'html.parser')
        headers = soup.findAll("h2")
        pattern = re.compile("Übungsgruppe .*")

        result = {}
        days = {"Mo" : "Montag",
                "Di" : "Dienstag",
                "Mi" : "Mittwoch",
                "Do" : "Donnerstag",
                "Fr" : "Freitag",
                "Sa" : "Samstag",
                "So" : "Sonntag"}

        for header in headers:
            if pattern.match(header.text):
                words = header.text.split(' ')
                for i in range(0, len(words)):
                    if "Vorlesung" == words[i]:
                        result["Subject"] = (words[i + 1] + ' ' + words[i + 2] + ' ' + words[i + 3]).replace('\n', '')

                    elif "am" == words[i]:
                        result["Day"] = days[words[i + 1]]
                        result["Time"] = words[i + 2]

                    elif re.compile("\(.*,").match(words[i]):
                        result["Place"] = (words[i] + ' ' + words[i + 1] + ' ' + words[i + 2]).replace('\n','')[1:-1]

        result["Link"] = tutoralLink

        return result

    def extractAllTutorialsInfo (self, tutLinks):
        result = []
        
        for link in tutLinks:
            result.append(self.extractTutorialInfo(link))
            
        return result
    
    def getCurrentTutorials(self):
        return self.extractAllTutorialsInfo(self.getCurrentTutorialLinks())

    def getTutorialInfoForDay (self, day, time):
        for info in self.extractAllTutorialsInfo(x['Link'] for x in self.getCurrentTutorials()):
            if info["Day"] == day and info["Time"] == time:
                return info
        raise TutNotFoundException('The Tutorium %s %s was not found!' % (day, time))

    def getStudentsMetaData (self, tutorialside):
        r = self.session.post(tutorialside)
        soup = BeautifulSoup(r.text, 'html.parser')
        tables = soup.findAll("table", attrs={"class":"colored"})
        students = []

        if len(tables) != 1:
            print("On", tutorialside, "there where", len(tables), "colored tables (1 expected)!")

        for row in tables[0].findAll('tr'):
            cols = row.find_all('td')
            if len(cols) > 0:
                #(name, mail, subject)
                students.append({'Name':cols[0].text, 'Mail':cols[0].find('a')['href'][len('mailto:'):], 'Subject':cols[1].text})

        return sorted(students, key=lambda x: x['Name'])

    def generateMetadataTable (self, info, stream = sys.stdout):
        students = self.getStudentsMetaData(info["Link"])
        maxs = getMaximumColumnSizes(students)

        divider = '+' + '-' * (maxs[0] + 2) + '+' + '-' * (maxs[1] + 2) + '+' + '-' * (maxs[2] + 2) + '+\n'
        headerDiv = '+' + '=' * (maxs[0] + 2) + '+' + '=' * (maxs[1] + 2) + '+' + '=' * (maxs[2] + 2) + '+\n'

        stream.write(headerDiv)
        stream.write('| ' + "NAME".rjust(maxs[0]) + ' | ' + "MAIL".rjust(maxs[1]) + ' | ' + "FACH".rjust(maxs[2]) + ' |\n')
        stream.write(headerDiv)

        for student in students:
            stream.write('| ' + student['Name'].rjust(maxs[0]) + ' | ' + student['Mail'].rjust(maxs[1]) + ' | ' + student['Subject'].rjust(maxs[2]) + ' |\n')
            stream.write(divider)
            
            
    def uploadCredits (self, info, creditFile, sheetNr):
        müsliStudents = self.getStudentsMetaData(info['Link'])
        self.moveToExcercise(info['Day'], info['Time'], sheetNr, link = info['Link'])
        
        payload = {"submit":"1"}
        
        cData = createCreditDictionary(creditFile)
        idData = {}
        notMatched = []
                
        soup = BeautifulSoup(self.session.get(self.curURL).text, 'html.parser')
        tables = soup.findChildren('table')
        rows = tables[0].findChildren(['th', 'tr'])
        
        for row in rows:
            if re.compile('<tr id=\"row-\d\d\d\d\">.*').match(str(row)):
                idData[row.findAll('td')[0].text] = [x['name'] for x in row.findAll('input', {"name":True})]
                
        #print(cData)
        #print(idData)
        
        result = {}
        
        for cStudentName, creds in cData.items():
            nameTuple = None
            for iStudentName, ids in idData.items():
                #if 'Maria' in iStudentName and 'Kag' in iStudentName:
                    #print(cStudentName)
                if compareNames(cStudentName, iStudentName):
                    nameTuple = (iStudentName, cStudentName)
                    print('Matched %s from file with %s from MÜSLI' % (cStudentName, iStudentName))
                    break
                
                
            if nameTuple != None:
                ids = idData[nameTuple[0]]
                for i, cred in enumerate(cData[nameTuple[1]]):
                    payload[ids[i]] = cred
                    
                #payload[nameTuple[0]] = cData[nameTuple[1]]
                result[nameTuple[0]] = cData[nameTuple[1]]
                del idData[nameTuple[0]]
        
        #for k,v in payload.items():
        #   print(k, v)
            
        
        #print('\n[ WARNING ] Uploading not implemented!\n')
        r = self.session.post(self.curURL, data=payload)
        
        return (result, idData)
        
    def setPresentedState (self, student, day = '', time = '', date = None, presented = True):
        if date != None:
            day = date[0]
            time = date[1]
        self.moveToPresented(day, time)
        
        payload = {"submit":"1"}
        rowId = ''
        
        soup = BeautifulSoup(self.session.get(self.curURL).text, 'html.parser')
        tables = soup.findChildren('table')
        rows = tables[0].findChildren(['th', 'tr'])
        
        for row in rows:
            if re.compile('<tr id=\"row-\d\d\d\d\">.*').match(str(row)):
                if student['Name'] == str(row).split('\n')[1][4:-5]:
                    rowId = [x['name'] for x in row.findAll('input', {'class':'points', 'name':True})][0]
                    break
        
        if rowId == '':
            raise ValueError('No Entry found for %s (@%s, %s)' % (student['Name'], day, time))
        else:
            payload[rowId] = '1' if presented else ''
            
        self.session.post(self.curURL, data=payload)
        
