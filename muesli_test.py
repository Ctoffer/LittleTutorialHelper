from muesli import MuesliApi
from muesli import getMaximumColumnSizes
from gmdata_managment import FolderManager

from os.path import join as pjoin
from student import Student

fm = FolderManager()

with MuesliApi(acc = fm.getMÜSLIAcc()) as mapi:
    info = mapi.getCurrentTutorials()
    #print(info)
    subject = info[0]['Subject']
    mapi.moveToTutorialMainPage(subject)
    #print(mapi.curURL)
    
    gMDataPath = '/home/christopher/Dokumente/Uni/SS17/ALDA-17/01_LTH_TestEnvir/GlobalMetaData'
    tutInfos = mapi.findExternalTutorialData(info[0]['Subject'], 
                        fm.getTFirstName() + ' ' + fm.getTLastName())
    
    keys = ['TID', 'Day', 'Time', 'Place', 'Subject', 'Link', 'Tutor']
    extTutRows = []
    
    for index, tutInfo in enumerate(tutInfos):
        #print(index, tutInfo)
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
        
        
            