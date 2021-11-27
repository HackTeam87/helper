#!/usr/bin/env python3
import sys
import re
import time
import telnetlib

try:
  IP=(sys.argv[1])
except:
  pass
try:
    MacSn=(sys.argv[2])
except:
  pass   

try:
    DESC=(sys.argv[3])
except:
  pass  

LOGIN = 'service'
PASSWORD = 'billing'

#LOGIN = 'TrialRooT'
#PASSWORD = 'GrinWin2021'

def to_bytes(line):
    return f"{line}\r\n".encode("utf-8")



def onu_id_by_mac_sn():
    global model
    tn = telnetlib.Telnet(IP)
    tn.write(to_bytes(LOGIN))
    time.sleep(0.5)
    tn.write(to_bytes(PASSWORD))
    banner = tn.read_very_eager()
    olt = re.search("\w{1,4}.OLT", str(banner)).group().split(' ')
    tn.write(to_bytes('enable'))
    tn.write(to_bytes('config'))
    tn.write(to_bytes('vty output show-all'))

    if olt[0] == 'EPON':
       model = 'EPON'
       tn.write(to_bytes('show ont info by-mac '+str(MacSn)))
       time.sleep(1)
      
    if olt[0] == 'GPON':
       model = 'GPON'
       tn.write(to_bytes('show ont info by-sn '+str(MacSn)))
       time.sleep(1)

    r = tn.read_very_eager()
    x = re.search("0/0.{0,9}", str(r)).group().split(' ')
    tn.close()
    return(x) 

onu_id = onu_id_by_mac_sn()
print(model)     

if model == 'EPON':
  Onu = {
  'PON': onu_id[0].strip(),
  'PORT': onu_id[2].strip(),
  'OnuId': onu_id[4].strip()
      }

if model == 'GPON':
  Onu = {
  'PON': onu_id[0].strip(),
  'PORT': onu_id[1].strip(),
  'OnuId': onu_id[3].strip()
      }      
   
print(Onu['PON'])  
print(Onu['PORT'])
print(Onu['OnuId'])



def onu_description():
    tn = telnetlib.Telnet(IP)
    tn.write(to_bytes(LOGIN))
    time.sleep(0.5)
    tn.write(to_bytes(PASSWORD))
    tn.write(to_bytes('enable'))
    tn.write(to_bytes('config'))
    
    if model == 'EPON':
        tn.write(to_bytes('interface epon '+str(Onu['PON'])))
        time.sleep(0.5)
    if model == 'GPON':
        tn.write(to_bytes('interface gpon '+str(Onu['PON']))) 

    tn.write(to_bytes('ont description '+str(Onu['PORT'])+' '+str(Onu['OnuId'])+' '+ str(DESC)))
    time.sleep(0.5)
    tn.write(to_bytes('exit'))
    time.sleep(0.3)
    tn.write(to_bytes('save'))
    time.sleep(0.5)
    tn.close()

    

onu_description()  

print('success')
