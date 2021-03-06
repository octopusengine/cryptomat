# ------------------------------
# 2017/09 - RPi3 (wifi)
# /dev/ttyAMA0 previously used to access the UART now connects to Bluetooth.
# The miniUART is now available on /dev/ttyS0.
#
#
print("Nextion display write test")
import sys, os, subprocess, time, datetime
import struct

#mport urllib2 #course
#import json
#from socket import gethostname, gethostbyname #getIp
from time import sleep

from socket import gethostname, gethostbyname #getIp
from time import sleep
from threading import Thread 

#---nextion
nxRead="00"
nx1="03"
nx2="04"
nx3="05"
nx4="06"
nx5="07"
nx6="08"
nx7="13"  
nexThread = True

b22 = bytes('"'.encode('ascii'))
#bFF = bytes(str(chr(0xff)).encode('utf-8')) #https://docs.python.org/3/howto/unicode.html
#bFF = (b'\xff', 'iso-8859-1') #https://wiki.python.org/moin/Python3UnicodeDecodeError

#https://stackoverflow.com/questions/35454378/python3-sending-serial-data-to-nextion-display
bFF=struct.pack('B', 0xff)

# ======uart tft serial monitor / nextion===== 9600 / 115200
import serial
"""
#RPi2
s = serial.Serial(port='/dev/ttyAMA0',baudrate=9600,                                                   
            timeout=1.0,
            xonxoff=False, rtscts=False, 
            writeTimeout=3.0,
            dsrdtr=False, interCharTimeout=None)
"""
#RPi3
s = serial.Serial(port='/dev/ttyS0',baudrate=9600,                                                   
            timeout=3.0,
            xonxoff=False, rtscts=False, 
            writeTimeout=3.0,
            dsrdtr=False, interCharTimeout=None)
            
# timeout=1.0, bylo 3 ---9600
# co="bauds=115200"
# neXcmd(co)             
# ===============================================

#---nextion 2015/12-
  #simple label (similar arduino test)
def neXcmd(cmd):   
    s.write(bytes(cmd.encode('ascii'))) 
    s.write(bFF)
    s.write(bFF)
    s.write(bFF)
    time.sleep(0.001)

def neXtxt(lab,label):
    #s.write("t0.txt=")
    ###s.write(kam)
    s.write(bytes(lab.encode('ascii')))
    #s.write(".txt=")
    #s.write(bytes(".txt=".encode('ascii')))
    s.write(b".txt=")    
    s.write(b22)
    #s.write("testLAB2")
    s.write(bytes(label.encode('ascii')))
    s.write(b22)
    s.write(bFF)
    s.write(bFF)
    s.write(bFF)
    #s.write("\n")
    #displLab("testLAB raspi 2 " + ver)
    #def n(co):
    #hh.dispWrite(chr(co))
    time.sleep(0.05) 

def nexth(): ##thread
 global nxRead, nexThread
 s.flushInput()
 cntx=0
 nacti= 7
 while nexThread:     
   try:
    hodnota = s.read(nacti) #7
    print(hodnota)
    iok=2 
    for ii in range (nacti):
     if ((hodnota[ii]).encode("hex")=="65"):
      iok = ii # index      
      nexWrite=((hodnota[iok+2]).encode("hex"))
      nxRead = nexWrite   

           
   except:
    # print "Err.data"
    nic = True   
   
   time.sleep(0.7)
   cntx=cntx+1

def nexRead():
   #global frn #file read nextion
   time.sleep(0.7)
   frn = open(intranetNex,"r")
   nexread = frn.read()
   frn.close()
    
   if (nxRead!="00"):
     return nxRead  
     #fwn = open(intranetNex,"w")  
     #fws.write("00")
     #fws.close()
   else:
     return "99"
   #frn.close()

# thread for reading
#thrnx = Thread(target=nexth)
#thrnx.start()

#-----------------------------------------

neXcmd("page intro")

i=0
while i<3:
  print(i)	
  neXtxt("t0",str(3-i))
  i +=1
  time.sleep(1)
  
neXcmd("page select")


#import serial
#ser = serial.serial_for_url('socket://10.0.2.234:23', timeout=5)
 
def read():
    out_hex = ''
    ff = 0
    while s.inWaiting():
 
        read_ser = s.read()
        print(read_ser),
 
        if read_ser == b'\xff': #xff
            ff += 1
            if ff == 3:
                print('GET cmd: ', out_hex)
                ff = 0
                out_hex = ''
 
        else:
            out_hex += "0x{:02x} ".format(ord(read_ser))
            s.flush
			#print(out_hex),    
 
#while True:
#####read()
time.sleep(1)

#---------------===============dwarf----------------
def nexth(): ##thread
 global nxRead, nexThread
 s.flushInput()
 cntx=0
 nacti= 7
 while nexThread:
 #for ii in range (30): 
   ###print str(ii)+":::::" 
   ##fws = open(intranetSub,"w")
   ##fws.write("sub"+str(cntx))
   ##fws = close()   
      
   try:
    hodnota = s.read(nacti) #7
    ##print hodnota
    iok=2 
    for ii in range (nacti):
     print((hodnota[ii]).encode("hex")),
     if ((hodnota[ii]).encode("hex")=="65"):
      iok = ii # index      
      nexWrite=((hodnota[iok+2]).encode("hex"))
      ##print "::::::::nex-th:::::::::::"+nexWrite
      nxRead = nexWrite 
     
      ##fwn = open(intranetNex,"w")
      ##fwn.write(nexWrite)
      ##fwn.close() 
     
      #hh.neXtxt2("d0","thr:::"+nexWrite) ##nevypisuje se od v 239.63
           
   except:
    # print "Err.data"
    nic = True   
   
   time.sleep(0.7)
   cntx=cntx+1

def nexRead():
   #global frn #file read nextion
   time.sleep(0.7)
   #frn = open(intranetNex,"r")
   #nexread = frn.read()
   #frn.close()

   print "nexRead() ="+ nexread
   if (nexread<>"00"):
     return nexread  
     #fwn = open(intranetNex,"w")  
     #fws.write("00")
     #fws.close()
   else:
     return "99"
   #frn.close()


#----------------------------------------------------------------------thread
#hh.neXtxt2("ti3","multi threading start")
#exec_command("sudo python nex.py")
thrnx = Thread(target=nexth)
thrnx.start()
#--------------------------------------------------------------------------------

cekej = True
ccnt=0
#s2.flushInput()
#for rx in range (20):

while cekej: #cekani na stisk
  ccnt=ccnt+1
  ctu = nxRead
  #print("nxRead var ="+ ctu)
  neXtxt("d0",str(ccnt) + ">"+str(ctu))
  if (ctu<>"00"): 
     ##pip(1800,0.05) #ctu
     #print "---stisknuto-ok---" + ctu
     if (ctu==nx1): print("nx1")
     if (ctu==nx2): print("nx2")
  else: 
     #print "---nic----" + ctu
     nic = True
  time.sleep(1.1)
 

#-------------------------end --------------
