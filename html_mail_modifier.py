import os
from re import compile as rcompile

def escapeTags(txt):
    res = ''
    i = 0
    while i < len(txt):
        if txt[i] is '<':
            if i + 4 < len(txt) and txt[i + 1] is '/' and txt[i + 4] is '>':
                res += txt[i] + txt[i + 1] + txt[i + 2] + txt[i + 3] + txt[i + 4]
                i += 5
                continue
            if i + 3 < len(txt) and txt[i + 1] is '/' and txt[i + 3] is '>':
                res += txt[i] + txt[i + 1] + txt[i + 2] + txt[i + 3]
                i += 4
                continue
            elif i + 2 < len(txt) and txt[i + 2] is '>':
                res += txt[i] + txt[i + 1] + txt[i + 2]
                i += 3
                continue
            elif i + 3 < len(txt) and txt[i + 3] is '>':
                res += txt[i] + txt[i + 1] + txt[i + 2] + txt[i + 3]
                i += 4
                continue
            else:
                res += '&#60;'
                i += 1
                continue
        elif txt[i] is '>':
            res += '&#62;'
            i += 1
            continue
        else:
            res += txt[i]
            i += 1
    return res

def toHyperLink(link):
    part1 = '<span style=\"text-decoration: underline; font-size: 20px; line-height: 21px;\"><a style=\"color:#C7702E\" title=\"link\" href=\"'
    part2 = '\" target=\"_blank\" rel=\"noopener noreferrer\">'
    part3 = '</a></span>'

    return part1 + link + part2 + link + part3

def markHyperlinks(txt):
    res = ''
    pattern = rcompile('.*https?://.*')

    for line in txt.split('\n'):
        if res != '':
            res += '\n'

        for word in line.split(' '):
            if pattern.match(word):
                res += (' ' if res != '' else '') + toHyperLink(word)

            else:
                res += (' ' if res != '' else '') + word

    return res

def handleLineStructure(line, op):
    if not line:
        return ('<br><br>', op)
    
    elif '<code>' in line:
        #print('Found Code')
        return ('', True)
    
    elif '</code>' in line:
        #print('Code finished')
        return ('> ', False)
    
    elif line.startswith(' '):
        res = ''
        i = 0
        while i < len(line) and line[i] == ' ':
            res += '&nbsp;'
            i += 1
        return (res + line[i:], op)        
    
    else:
        return (line, op)

def lineReplacer(txt):
    res = ''
    op = False

    for line in txt.split('\n'):
        if res != '':
            res += '\n'

        tup = handleLineStructure(line, op)
        op = tup[1]
        
        if op and tup[0] != '<br><br>':
            res += '> ' + tup[0] + '<br>'
            
        elif op and tup[0] == '<br><br>':
            res += '> <br>'
            
        else:
            if op:
                res += '> '
            res += tup[0]

    return res

def createInfoMailFromTemplate(me, template, subject, textPath, resultFilename = None):
    print('createInfoMailFromTemplate %s %s' % (template, textPath))
    print(me)
    
    with open(template, 'r') as f:
        txt = f.read().replace("VID:=SUBJECT", escapeTags(subject))
        txt = txt.replace('VID:=ME_NAME', me['Name']).replace('VID:=ME_MAIL', me['Mail'])

        with open(textPath, 'r') as f2:
            body = markHyperlinks(escapeTags(lineReplacer(f2.read())))
            txt = txt.replace("VID:=GLOBAL_TEXT", body)
            
        if resultFilename is None:
            resultFilename = os.path.splitext(os.path.abspath(textPath))[0]+'.html'

        with open(resultFilename, 'w') as o:
            o.write(txt)
            
        return txt
    
def extractCreditsFromLine(line):
    return [float(x) for x in line.split['|'][1:-1]]
    
def buildTableHeaders(creds):
    buffer = ''
    
    for i in range(len(creds)):
        buffer += '<th style=\"text-align: center;\">A' + str(i).zfill(2)  + '</th>'
        
    return buffer
    
def buildTableElements(creds):
    buffer = ''

    for cred in creds:
        buffer += '<td style=\"text-align: center;\">' + str(cred)  + '</td>'
        
    return buffer

def toNamesLine(students, sep = ' ', namesep = ', '):
    names = ''
    
    for student in students:
        nick = ('%s %s' % (student.split(' ')[0], student.split(' ')[-1])).replace(' ', sep)
        
        if names == '':
            names += nick
        else:
            names += namesep + nick
            
    return names
    
def preInterpretFeedbackSyntax(text):
    result = ''
    for line in text.split('\n'):
        if line.startswith('#Aufgabe'):
            result += '<br><u><b>Aufgabe %s</b></u><br><br>' % line.split(' ')[1] + '\n'
                
        elif rcompile('#\[(\+|-)?\d+(\.\d+)?\]$').match(line):
            num = float(line[2:-1])
            numseq = '%s pkt' % str(num) if num == -1 or num == 1 else '%s pkte' % str(num)
            result += '<br>[%s]<br>' % numseq + '\n'
            
        elif line.startswith('#SUM['):
            num = float(line[5:-1])
            numseq = '%s pkt' % str(num) if num == -1 or num == 1 else '%s pkte' % str(num)
            result += '<br><b>SUM</b>:[%s]' % numseq + '\n'
            
        elif line.startswith('#>Code'):
            result += '<code>\n'
            
        elif line.startswith('#<'):
            result += '</code>\n'
            
        else:
            result += line + '\n'
    
    return result
    
def createReturnMailFromTemplate(me, studentNames, creds, template, sheetNr, paths, resultFilename = None, retPath = False):
    print('createReturnMailFromTemplate(%s)' % str(studentNames))
    with open(template, 'r') as f:
        txt = f.read().replace("VID:=B_NUMMER", str(sheetNr).zfill(2))
        txt = txt.replace('VID:=ME_NAME', me['Name']).replace('VID:=ME_MAIL', me['Mail'])
        txt = txt.replace('VID:=W_DAY', '')
        
        with open(paths['Global'], 'r') as f2:
            body = markHyperlinks(escapeTags(lineReplacer(f2.read())))
            txt = txt.replace("VID:=GLOBAL_TEXT", body)
            
        with open(paths['Feedback'], 'r') as f2:
            f2Text = preInterpretFeedbackSyntax(f2.read())
            body = markHyperlinks(escapeTags(lineReplacer(f2Text)))
            
            txt = txt.replace('VID:=MEMBER_NAMES', toNamesLine(studentNames))
            txt = txt.replace("VID:=LOCAL_FEEDBACK", body)
            txt = txt.replace('VID:=HTML_TH_EX', buildTableHeaders(creds))
            txt = txt.replace('VID:=HTML_TD_P', buildTableElements(creds))
            txt = txt.replace('VID:=P_SUM', str(sum(creds)))

        if resultFilename == None:
            resultFilename = os.path.join(os.path.dirname(paths['Feedback']), 'html_%s.html' % (toNamesLine(studentNames, sep = '-', namesep = '_')))

        with open(resultFilename, 'w') as o:
            o.write(txt)
        
        if retPath:
            return resultFilename
        return txt
    
def createDefaultReturnMailFromTemplate(me, studentName, template, sheetNr, gFeedbackPath, resultFilename = None, retPath = False):
     print('createDefaultReturnMailFromTemplate(%s)' % str(studentName))
     with open(template, 'r') as f:
        txt = f.read().replace("VID:=B_NUMMER", str(sheetNr).zfill(2))
        txt = txt.replace('VID:=ME_NAME', me['Name']).replace('VID:=ME_MAIL', me['Mail'])
        txt = txt.replace('VID:=W_DAY', '')
        
        with open(gFeedbackPath, 'r') as fd:
            body = markHyperlinks(escapeTags(lineReplacer(fd.read())))
            txt = txt.replace("VID:=GLOBAL_TEXT", body)
            
        
        body = 'Es konnte keine Übereinstimmung zwischen dir und einer Abgabe hergestellt werden. Sollte dies ein Fehler sein, dann schreib mir eine Mail.'
            
        txt = txt.replace('VID:=MEMBER_NAMES', studentName)
        txt = txt.replace("VID:=LOCAL_FEEDBACK", body)
        txt = txt.replace('VID:=HTML_TH_EX', '')
        txt = txt.replace('VID:=HTML_TD_P', '')
        txt = txt.replace('VID:=P_SUM', '---')

        if resultFilename == None:
            resultFilename = os.path.join(os.path.dirname(gFeedbackPath), 'html_%s.html' % (studentName.replace(' ', '-')))

        with open(resultFilename, 'w') as o:
            o.write(txt)
        
        if retPath:
            return resultFilename
        return txt


createReturnMailFromTemplate({'Name':'Christopher', 'Mail':'christopher.schuster@stud.uni-heidelberg.de'}, 
                                    ['Ein Student', 'Vorname Zweitname Nachname'],
                                    [7, 16, 16],
                                    '/home/christopher/Dokumente/Uni/SS17/ALDA-17/GlobalMetaData/return_template.html',
                                    3,
                                    {'Global':'/home/christopher/Dokumente/Uni/SS17/ALDA-17/00_Tutorialsnake/GlobalFeedback.txt',
                                     'Feedback':'/home/christopher/Dokumente/Uni/SS17/ALDA-17/00_Tutorialsnake/Feedback.txt'
                                     },
                                    'HTML_mail01.html'
                                    )