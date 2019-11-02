import requests,os,shutil,datetime
import time


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
               if (waitingToprocess - Cmoved) > 100:
                  print("Please check for ",fileName," its not getting processed...")
                  exit(0)
      else:
         print(fileName, " processed")
         i = 1
         return True

def moveC2ToInbox(optaNatchNo):
   ####moving the c2 and c3 file in destination
   moveto = "D:\Watch\Inbox"
   c2c3_filePath="D:\\OptaXML\\XMLs\\"
   if os.path.isfile(c2c3_filePath + ('crml-{}_C2_.xml'.format(optaMatchNo))):
      src = c2c3_filePath + ('crml-{}_C2_.xml'.format(optaMatchNo))
      dst = moveto + '\\' + ('crml-{}_C2_.xml'.format(optaMatchNo))
      shutil.move(src, dst)
      c2moved = time.time()
      print('crml-{}_C2_.xml'.format(optaMatchNo)," moved to inbox")
      return c2moved
   else:
      print('crml-{}_C2_.xml'.format(optaMatchNo), " is not available to drop in inbox")
      a=input("Press Enter to exit")
      exit(0)

def moveC3ToInbox(fileName):
   c2moved = time.time()
   moveto = "D:\Watch\Inbox"
   c2c3_filePath = "D:\\OptaXML\\XMLs\\"
   if os.path.isfile(c2c3_filePath + ('crml-{}_C3_.xml'.format(optaMatchNo))):
      src = c2c3_filePath + ('crml-{}_C3_.xml'.format(optaMatchNo))
      dst = moveto + '\\' + ('crml-{}_C3_.xml'.format(optaMatchNo))

      ###true if c2 processed successfully.If c2 processed moving c3 to inbox
      check_C2_processState = checkFile('crml-{}_C2_.xml'.format(optaMatchNo))
      if check_C2_processState == True:
         shutil.move(src, dst)
         print('crml-{}_C3_.xml'.format(optaMatchNo), " moved to inbox")
         c3moved = time.time()
         return c3moved
      # If c2 not processed, waiting c2 to get processed and then moving c3 to inbox
      else:
         i = 0
         while (i == 0):
            print("Waiting for " + 'crml-{}_C2_.xml'.format(optaMatchNo) + " to get processed")
            check_C2_processState = checkFile('crml-{}_C2_.xml'.format(optaMatchNo))
            ###if c2 processed and is in success folder, moving c3 to inbox
            if check_C2_processState == True:
               shutil.move(src, dst)
               print('crml-{}_C3_.xml'.format(optaMatchNo), " moved to inbox")
               c3moved = time.time()
               return c3moved
            else:
               time.sleep(60)
               waitingForC2Toprocess = time.time()
               if (waitingForC2Toprocess - c2moved) > 100:
                  print('crml-{}_C3_.xml'.format(optaMatchNo), " is not available to drop in inbox")
                  a = input("Press Enter to exit")
                  exit(0)

def generateC2C3(optaMatchNo):
   c2Url = 'http://omo.akamai.opta.net/?game_id={}&feed_type=c2&user=PrimeFocus&psw=eZPW4bhFYtX'.format(optaMatchNo)
   c3Url = 'http://omo.akamai.opta.net/?game_id={}&feed_type=c3&user=PrimeFocus&psw=eZPW4bhFYtX'.format(optaMatchNo)
   c2c3_filePath = "D:\\OptaXML\\XMLs\\"
   ###Creating C2 file
   resp = requests.get(r'' + c2Url)
   with open(c2c3_filePath + 'crml-' + optaMatchNo + '_C2_.xml', 'wb') as foutput:
      foutput.write(resp.content)

   ###Creating C3 file
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
   c2moved=moveC2ToInbox(optaMatchNo)
   isC2Processed=checkFile('crml-{}_C2_.xml'.format(optaMatchNo))
   i=0
   while i==0:
      j=waiting_For_processing('crml-{}_C2_.xml'.format(optaMatchNo),c2moved)
      if(j==True):
         i=1
   ###if C2 processed moving C3 to inbox
   c3moved = moveC3ToInbox(optaMatchNo)
   isC3Processed = checkFile('crml-{}_C3_.xml'.format(optaMatchNo))
   i = 0
   while i == 0:
      j = waiting_For_processing('crml-{}_C3_.xml'.format(optaMatchNo), c3moved)
      if (j == True):
         i = 1

option=int(input("Please select processing steps :-\n1 => To process All(C2,C3,C50)\n2 => To process only C2\n"
      "3 => To process only C3\n4 => To process C50\n5 => To check status\n6 => To exit\n").strip())

if(option in (1,2,3)):
   optaMatchNo = input("Please enter opta match id : ").strip()
   ###generating c2 and c3
   generateC2C3(optaMatchNo)

   if(option==1):
      processAll(optaMatchNo)

   elif(option==2):
      c2moved = moveC2ToInbox(optaMatchNo)
      isC2Processed = checkFile('crml-{}_C2_.xml'.format(optaMatchNo))
      i = 0
      while i == 0:
         j = waiting_For_processing('crml-{}_C2_.xml'.format(optaMatchNo), c2moved)
         if (j == True):
            i = 1
   else:
      c3moved = moveC3ToInbox(optaMatchNo)
      isC3Processed = checkFile('crml-{}_C3_.xml'.format(optaMatchNo))
      i = 0
      while i == 0:
         j = waiting_For_processing('crml-{}_C3_.xml'.format(optaMatchNo), c3moved)
         if (j == True):
            i = 1

elif(option==4):
   optaMatchNo = input("Please enter opta match id : ").strip()
   print("processing c50")

elif(option==5):
   optaMatchNo = input("Please enter opta match id : ").strip()
   print("printing status")

else:
   a=input("Exiting.....")
   exit(0)