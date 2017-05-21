#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

import html_mail_modifier as HTMLMM

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from gmdata_managment import FolderManager as FM

from account_exceptions import LoginException
from smtplib import SMTP
    
iTempPath = FM().getInfoTemplatePath()
rTempPath = FM().getReturnTemplatePath()
me = FM().getMyEmailData()
me = {'Name':me[0], 'Mail':me[1]}

class Sender(object):
    
    def __init__(self, address = 'extmail.urz.uni-heidelberg.de', port = 587, acc = ('user', 'passw'), allowed = False):
        self.server = {'address' : address, 'port' : port}
        self.conn = None
        self.acc = acc
        self.allowed = allowed
        
    def isConnected(self):
        return self.conn != None
            
    def login(self):
        print('Trying to connect to %s:%s' % (self.server['address'], self.server['port']))
        self.conn = SMTP(self.server['address'], self.server['port'])
        self.conn.ehlo()
        
        print('Connection established.')
        try:
            print('Uni-Mail Login')
            self.conn.login(self.acc[0], self.acc[1])
        except Exception as exc:
            raise LoginException('Login failed! %s' % str(exc))
            
    def __enter__(self):
        self.login()
        return self
    
    def __exit__(self, type, value, traceback):
        self.logout()
            
    def logout(self):
        print('Uni-Mail Logout')
        self.conn.quit()
        self.conn = None
        
    def sendHTMLMail(self, senderMail, receiverMail, subject, htmltxt, attachments = []):
        print('sendHTMLMail (%s) from \'%s\' to \'%s\' with %d attachments' % (subject, senderMail, receiverMail, len(attachments)))
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = senderMail
        msg['To'] = receiverMail
        
        plaintxt = "Wenn diese Mail dir nicht angezeigt wird, dann unterstützt dein E-Mailclient keine HTML-Mails.\nSollte dies der Fall sein, dann schreibe mir bitte unverzüglich eine Mail!"
        
        part1 = MIMEText(plaintxt, 'plain', 'utf-8')
        part2 = MIMEText(htmltxt, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)

        for f in attachments:
            with open(f, "rb") as fil:
                part = MIMEApplication(fil.read(), Name=os.path.basename(f))
                part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
                msg.attach(part)
        
        if self.allowed:
            self.conn.sendmail(senderMail, receiverMail, msg.as_string())
        
    def sendInfoMail(self, student, lecture, infotitle, contentpath, attachments = []):
        print('sendInfoMail')
        global iTempPath
        global me
        subject = "[" + lecture + "] " + infotitle
        
        htmltxt = HTMLMM.createInfoMailFromTemplate(me, iTempPath, infotitle, contentpath)
        
        self.sendHTMLMail(me['Mail'], student['Mail'], subject, htmltxt, attachments)
        
    def sendInfoMailToAll(self, students, lecture, infotitle, contentpath, attachments = []):
        print('sendInfoMailToAll')
        global iTempPath
        global me
        subject = "[" + lecture + "] " + infotitle
        
        htmltxt = HTMLMM.createInfoMailFromTemplate(me, iTempPath, infotitle, contentpath)
        
        for student in students:
            self.sendHTMLMail(me['Mail'], student['Mail'], subject, htmltxt, attachments)
            
        print('Info Mail was sent to %d students' % len(students))
        
    def sendInfoTestMail(self, lecture, infotitle, contentpath, attachments = []):
        print('sendInfoTestMail')
        global me
        self.sendInfoMail(me, lecture, infotitle, contentpath, attachments)
        
    def sendFeedbackMails(self, lecture, sheetNr, mailPathDict):
        global me
        subject = '[ %s ] Zettelrückgabe %s' % (lecture, str(sheetNr).zfill(2))
    
        i = 0
        maxI = len(mailPathDict)
        for mail, path in mailPathDict.items():
            with open(path, 'r') as fd:
                print('Send Mail %s of %s to %s' % (str(i + 1).zfill(2), str(maxI).zfill(2), mail))
                
                text = fd.read()
                
                self.sendHTMLMail(me['Mail'], mail, subject, text)
                # TODO only debug
                self.sendHTMLMail(me['Mail'], me['Mail'], subject, text)
                i += 1
            
    def sendReturnTestMail(self, lecture, contentpaths, attachments = []):
        global rTempPath
        global me
        
        sheetNr = 28
        creds = [11.0, 6.5, 3.5, 11.0]
        tutinfo = {'Day':'Samstag', 'Time':'25:98'}
        subject = '[ %s ] Zettelrückgabe Blatt %s' % (lecture, str(sheetNr).zfill(2))
        
        htmltxt = HTMLMM.createReturnMailFromTemplate(me, [me], creds, tutinfo, rTempPath, sheetNr, contentpaths)
        
        self.sendHTMLMail(me['Mail'], me['Mail'], subject, htmltxt, attachments)
