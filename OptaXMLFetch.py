import requests,os,shutil,datetime
import time

def copyC50FromSource(optaNatchNo):
   print("c50 are copied")

def renameC50(optaNatchNo):
   print("c50 are renamed")

def dropC50(optaNatchNo):
   print("c50 are dropped")

###check whether C2  & C3 is processed or not
def checkFile(fileName):
   if os.path.isfile("D:\\Watch\\Success\\"+fileName):
      return  True
   else:
      return False

def waiting_For_processing(fileName,timeStart):
   Cmoved=timeStart
   isProcessed=checkFile(fileName)
   i = 0
   while i == 0:
      ###waiting for c2 to get processed
      if isProcessed == False:
         j = 0
         while (j == 0):
            print("Waiting for " + fileName + " to get processed")
            check_processState = checkFile(fileName)
            if check_processState == True:
               j = 1
               i = 1
               print(fileName, " processed")
               return True
            else:
               time.sleep(60)
               waitingToprocess = time.time()
               if (waitingToprocess - Cmoved) > 420:
                  print("Please check for ",fileName," its not getting processed...")
                  exit(0)
      else:
         print(fileName, " processed")
         i = 1
         return True

def move_C2_C3_ToInbox(fileName):
   ####moving the c2 and c3 file in destination
   moveto = "D:\Watch\Inbox"
   c2c3_filePath="D:\\OptaXML\\XMLs\\"
   if os.path.isfile(c2c3_filePath + fileName):
      src = c2c3_filePath + fileName
      dst = moveto + '\\' + fileName
      shutil.move(src, dst)
      Cmoved = time.time()
      print(fileName," moved to inbox")
      return Cmoved
   else:
      print(fileName, " is not available to drop in inbox")
      a=input("Press Enter to exit")
      exit(0)

def generateC2C3(optaMatchNo):
   c2c3_filePath = "D:\\OptaXML\\XMLs\\"
   c2Url = 'http://omo.akamai.opta.net/?game_id={}&feed_type=c2&user=PrimeFocus&psw=eZPW4bhFYtX'.format(optaMatchNo)
   resp = requests.get(r'' + c2Url)
   with open(c2c3_filePath + 'crml-' + optaMatchNo + '_C2_.xml', 'wb') as foutput:
      foutput.write(resp.content)

   c3Url = 'http://omo.akamai.opta.net/?game_id={}&feed_type=c3&user=PrimeFocus&psw=eZPW4bhFYtX'.format(optaMatchNo)
   resp = requests.get(r'' + c3Url)
   with open(c2c3_filePath + 'crml-' + optaMatchNo + '_C3_.xml', 'wb') as foutput:
      foutput.write(resp.content)

   # ##removing the unwanted line from XML
   for roots, dirs, files in os.walk(c2c3_filePath):
      fileNames = os.listdir(c2c3_filePath)
      for file in fileNames:
         with open(c2c3_filePath + file, 'r') as fin:
            data = fin.read().splitlines(True)
         with open(c2c3_filePath + file, 'w') as fout:
            fout.writelines(data[8:])

   ###finding &lt;  br  &gt;   and replacing with <  br/ >
   for roots, dirs, files in os.walk(c2c3_filePath):
      fileNames = os.listdir(c2c3_filePath)
      for file in fileNames:
         with open(c2c3_filePath + file, 'r')as inputFile:
            fileData = inputFile.read()
         fileData = fileData.replace('&lt;', '<')
         fileData = fileData.replace('br', 'br/')
         fileData = fileData.replace('&gt;', '>')
         with open(c2c3_filePath + file, 'w')as file:
            file.write(fileData)

def processAll(optaMatchNo):
   c2moved=move_C2_C3_ToInbox('crml-{}_C2_.xml'.format(optaMatchNo))
   i=0
   while i==0:
      j=waiting_For_processing('crml-{}_C2_.xml'.format(optaMatchNo),c2moved)
      if(j==True):
         i=1
   ###if C2 processed moving C3 to inbox
   c3moved = move_C2_C3_ToInbox('crml-{}_C3_.xml'.format(optaMatchNo))
   i = 0
   while i == 0:
      j = waiting_For_processing('crml-{}_C3_.xml'.format(optaMatchNo), c3moved)
      if (j == True):
         i = 1
   ####processing c50
   copyC50FromSource(optaMatchNo)
   renameC50(optaMatchNo)
   dropC50(optaMatchNo)

option=int(input("Please select processing steps :-\n1 => To process All(C2,C3,C50)\n2 => To process only C2\n"
      "3 => To process only C3\n4 => To process C50\n5 => To check status\n6 => To exit\n").strip())

if(option in (1,2,3)):
   optaMatchNo = input("Please enter opta match id : ").strip()

   if(option==1):
      generateC2C3(optaMatchNo)
      processAll(optaMatchNo)

   elif(option==2):
      isC2Processed=checkFile('crml-{}_C2_.xml'.format(optaMatchNo))
      if isC2Processed==False:
         if os.path.isfile("D:\\OptaXML\\XMLs\\" + 'crml-{}_C2_.xml'.format(optaMatchNo)):
            c2moved = move_C2_C3_ToInbox('crml-{}_C2_.xml'.format(optaMatchNo))
            i = 0
            while i == 0:
               j = waiting_For_processing('crml-{}_C2_.xml'.format(optaMatchNo), c2moved)
               if (j == True):
                  i = 1
         else:
            print('crml-{}_C2_.xml'.format(optaMatchNo), " is not in source to drop")
      else:
         print('crml-{}_C2_.xml'.format(optaMatchNo)," is already processed,available in success folder")
   ###processing C3
   else:
      ##checking whether c2 processed or not
      isC2Processed = checkFile('crml-{}_C2_.xml'.format(optaMatchNo))
      if isC2Processed==True:
         isC3Processed = checkFile('crml-{}_C3_.xml'.format(optaMatchNo))
         if isC3Processed == False:
            if os.path.isfile("D:\\OptaXML\\XMLs\\" + 'crml-{}_C3_.xml'.format(optaMatchNo)):
               c3moved = move_C2_C3_ToInbox('crml-{}_C3_.xml'.format(optaMatchNo))
               i = 0
               while i == 0:
                  j = waiting_For_processing('crml-{}_C3_.xml'.format(optaMatchNo), c3moved)
                  if (j == True):
                     i = 1
            else:
               print('crml-{}_C3_.xml'.format(optaMatchNo), " is not in source to drop")
         else:
            print('crml-{}_C3_.xml'.format(optaMatchNo), " is already processed,available in success folder")
      else:
         print('crml-{}_C2_.xml'.format(optaMatchNo)," is not processed yet,Please process ",
               'crml-{}_C2_.xml'.format(optaMatchNo)," first")

elif(option==4):
   optaMatchNo = input("Please enter opta match id : ").strip()
   isC2Processed = checkFile('crml-{}_C2_.xml'.format(optaMatchNo))
   if isC2Processed==True:
      isC3Processed = checkFile('crml-{}_C3_.xml'.format(optaMatchNo))
      if isC3Processed==True:
         print("processing c50 can start")
         copyC50FromSource(optaMatchNo)
         renameC50(optaMatchNo)
         dropC50(optaMatchNo)

      else:
         print('crml-{}_C3_.xml'.format(optaMatchNo), " is not processed yet,Please process ",
               'crml-{}_C3_.xml'.format(optaMatchNo), " first")

   else:
      print('crml-{}_C2_.xml'.format(optaMatchNo), " is not processed yet,Please process ",
            'crml-{}_C2_.xml'.format(optaMatchNo), " first")

elif(option==5):
   optaMatchNo = input("Please enter opta match id : ").strip()
   print("printing status")

else:
   a=input("Exiting.....")
   exit(0)