#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:05:39 2017

@author: christopher
"""

from os import getcwd
from os import walk as owalk
from os.path import join as pjoin
from os.path import basename as pbasename
from os.path import dirname as pdirname
from os.path import split as osplit

from sys import argv

from gmdata_managment import FolderManager
from html_mail_modifier import createReturnMailFromTemplate
from html_mail_modifier import createDefaultReturnMailFromTemplate

from email_sender import Sender

from student import cmpNameParts

def extractCredits(path):
    with open(path, 'r') as fd:
        return [float(x.strip()) for x in fd.readline().split('|')[1:]]
    
def getMaxCredits(mCredPath):
    creds = []
    with open(mCredPath, 'r') as fd:
        for line in fd:
            creds.append(float(line))
    return creds
        
def splitpath(path, maxdepth = 20):
     ( head, tail ) = osplit(path)
     return splitpath(head, maxdepth - 1) + [ tail ] \
         if maxdepth and head and head != path \
         else [ head or tail ]    
         
def prepareMails(studs, me, wPath, template):
    gFeedback = None
    maxCreds = []
    result = {}
    me = {'Name':me[0], 'Mail':me[1]}
    
    for root, dirs, files in owalk(wPath):
        if 'GlobalFeedback.txt' in files:
            gFeedback = pjoin(root, 'GlobalFeedback.txt')
            maxCreds = getMaxCredits( pjoin(root, 'MaxCredits.txt'))
        
        if 'Feedback.txt' in files:
            #print(root, dirs, files)
            pathElems = splitpath(root)
            students = [x.split('(')[0].replace('-', ' ') for x in pbasename(root).split('_')[2:]]
            creds = extractCredits(pjoin(root, 'credits.txt'))
            creds = [creds[i] + maxC for i, maxC in enumerate(maxCreds)]
            sheetNr = int(pathElems[-4].split('_')[1])
            paths = {'Feedback': pjoin(root, 'Feedback.txt'), 'Global': gFeedback}
            
            htmlPath = createReturnMailFromTemplate(me, students, creds, template, sheetNr, paths, retPath = True)
            
            for name in students:
                for stud in studs:
                    if cmpNameParts(stud['Name'].split(' '), name.split(' ')):
                        studs.remove(stud)
                        result[stud['Mail']] = htmlPath
                        break
                    else:
                        replacer = {'ä':'ae', 'ü':'ue', 'ö':'oe', 'Ü':'Ue', 'Ö':'Oe', 'Ä':'Ae', 'ß':'ss'}
                        
                        #org = stud['Name']
                        tmp = stud['Name']
                        for k, v in replacer.items():
                            tmp = tmp.replace(k, v)
                    
                        if cmpNameParts(tmp.split(' '), name.split(' ')):
                            studs.remove(stud)
                            result[stud['Mail']] = htmlPath
                            break
                        
    for s in studs:
        result[s['Mail']] = createDefaultReturnMailFromTemplate(me, s['Name'], 
              template, sheetNr, gFeedback, 
              resultFilename = None, retPath = True)
    
    return result
                    
def sendFeedbackMails(wpath, sendable = False):
    fm = FolderManager(wpath)
    #print(os.path.basename(os.path.dirname(wpath)))
    sheetNr = pbasename(pdirname(wpath)).split('_')[1]
    
    studs = fm.getAllStudents(status = 'Local;Imported')
    mailHtmlDict = prepareMails(studs, fm.getMyEmailData(), wpath, fm.getReturnTemplatePath())

    if sendable:
        quest = 'Do u rly want to send Feedbackmails to ur students? (Y|n)'
        sendable = input(quest) == 'Y'
    else:
        print('Mails prepared. To send it after prepareing use -S as console parameter')
    
    if sendable:
        with Sender(acc = fm.getMailAcc()) as sender:
            sender.allowed = sendable
            sender.sendFeedbackMails(fm.getSubject(), sheetNr, mailHtmlDict)
    

if __name__ == '__main__':
    print('Starting Feedback-Sender in %s' % getcwd())
    print()
    sendFeedbackMails(getcwd(), '-S' in argv)