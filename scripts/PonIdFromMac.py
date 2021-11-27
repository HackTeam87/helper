#!/usr/bin/env python3
import sys
import re
import time
import telnetlib



#LOGIN = 'TrialRooT'
#PASSWORD = 'GrinWin2021'

class Test:
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

  def to_bytes(self,line):
    return f"{line}\r\n".encode("utf-8")



  def onu_id_by_mac_sn(self,IP,MacSn):
      LOGIN = 'service'
      PASSWORD = 'billing'


      global model
      tn = telnetlib.Telnet(IP)
      tn.write(self.to_bytes(LOGIN))
      time.sleep(0.5)
      tn.write(self.to_bytes(PASSWORD))
      banner = tn.read_very_eager()
      olt = re.search("\w{1,4}.OLT", str(banner)).group().split(' ')
      tn.write(self.to_bytes('enable'))
      tn.write(self.to_bytes('config'))
      tn.write(self.to_bytes('vty output show-all'))

      if olt[0] == 'EPON':
          model = 'EPON'
      if olt[0] == 'GPON':
         model = 'GPON'

      tn.write(self.to_bytes('show location '+str(MacSn)))
      time.sleep(1)
      

      r = tn.read_very_eager()
      x = re.search("pon.{1,15}", str(r)).group().split(' ')
      tn.close()
      x = list(filter(None, x))
    
      return(x) 

  
  onu_id = onu_id_by_mac_sn(IP,MacSn)
  print(model)

  PortId = list(onu_id[0].split('pon')[-1])
  PON = PortId[0] + PortId[1] + PortId[2]
  PON = PON.strip()
  PORT = PortId[4].strip()
  OnuId = onu_id[1].strip()

  Onu = {
  'PON': PON,
  'PORT': PORT,
  'OnuId': OnuId
      }    
   
  print(Onu['PON'])  
  print(Onu['PORT'])
  print(Onu['OnuId'])

  def onu_description(self,IP,DESC): 
    LOGIN = 'service'
    PASSWORD = 'billing'


    tn = telnetlib.Telnet(IP)
    tn.write(self.to_bytes(LOGIN))
    time.sleep(0.5)
    tn.write(self.to_bytes(PASSWORD))
    tn.write(self.to_bytes('enable'))
    tn.write(self.to_bytes('config'))
    
    if model == 'EPON':
        tn.write(self.to_bytes('interface epon '+str(self.Onu['PON'])))
        time.sleep(0.5)
    if model == 'GPON':
        tn.write(self.to_bytes('interface gpon '+str(self.Onu['PON']))) 

    tn.write(self.to_bytes('ont description '+str(self.Onu['PORT'])+' '+str(self.Onu['OnuId'])+' '+ str(DESC)))
    time.sleep(0.5)
    tn.write(self.to_bytes('exit'))
    time.sleep(0.3)
    tn.write(self.to_bytes('save'))
    time.sleep(0.5)
    tn.close()

    
   

  print('success')
