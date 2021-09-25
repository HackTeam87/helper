#! /usr/bin/python3
import os

# ip = '185.253.216.129'
# community ='billing'

class MikrotikBase:
    def mik_model(self, ip, community):
        

        # model
        mik_name = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.1.1.0')
        for n in mik_name:
            mik_n = n.split(':')[1].strip().strip('"').strip('"\n').strip('\"').strip('\\')
        mik_n = 'Model: ' + str(mik_n)    

        # soft
        mik_soft = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.47.1.1.1.1.2.65536')
        for soft in mik_soft:
            mik_s = soft.split(':')[1].strip().strip('"').strip('"\n').strip('\"').strip('\\')
        mik_s = 'Soft: ' + str(mik_s)        

         # total_memory
        mik_total_memory = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.25.2.3.1.5.65536')
        for total_memory in  mik_total_memory:
            mik_t_m = total_memory.split(':')[1].strip().strip('"').strip('"\n').strip('\"').strip('\\')
        mik_t_m = int(mik_t_m) / 1024
        mik_t_m = "%.2f" % mik_t_m 
        mik_t_m = 'Total_Memory: ' + str(mik_t_m) + ' mb'  
            
         # used_memory
        mik_used_memory = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.25.2.3.1.6.65536')
        for used_memory in mik_used_memory:
            mik_u_m = used_memory.split(':')[1].strip().strip('"').strip('"\n').strip('\"').strip('\\') 
        mik_u_m = int(mik_u_m) / 1024
        mik_u_m = "%.2f" % mik_u_m 
        mik_u_m = 'Used_Memory: ' + str(mik_u_m) + ' mb'

      
      
        # uptime
        mik_uptime = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.1.3.0')
        for u in mik_uptime:
            t = u.split('=')[1].split(' ')
            mik_u = t[-3] + ' ' + t[-2] + ' ' + t[-1]
            mik_u.strip().strip("'\n'")
        mik_u = 'Uptime: ' + str(mik_u)    

        # indentity
        mik_indentity = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.1.5.0')
        for indenty in mik_indentity:
            mik_ind = indenty.split(':')[1].strip('"').strip().strip('"').strip() 
        mik_ind = 'Indentity: ' + str(mik_ind)

          # temperature
        mik_temperature = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.14988.1.1.3.10.0')
        for temp in mik_temperature:
            mik_tmp = temp.split(':')[1].strip('"').strip().strip('"').strip()
        mik_tmp = int(mik_tmp) /10    
        mik_tmp = 'Temperature: ' + str(mik_tmp) + ' °C'           

        
        # location
        mik_location = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.1.6.0')
        for location in mik_location:
           
            if location.split(':')[1].strip(' ') == "":
                 mik_loc = 'not set' 
            else:
                mik_loc = location.split(':')[1].strip('"').strip().strip('"').strip()
        mik_loc = 'Location: ' + str(mik_loc)   


         # cpu
        mik_cpu = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.25.3.3.1.2')
        count_cpu = 0
        mik_cp = []
        
        for cpu in mik_cpu:
            mik_cp.append(cpu.split(':')[1].strip('"').strip().strip('"').strip())
            count_cpu += 1
        for rcpu in mik_cp:
            rcpu+rcpu
              
        cpu = 'cpu: count ' +  str(count_cpu) + ', load: ' + str(rcpu) +'%'


        res_base = [{'uptime': mik_u, 'name': mik_n,'soft': mik_s,  'indentity': mik_ind, 
                    'location': mik_loc , 'memory_total':  mik_t_m, 'memory_used':  mik_u_m, 
                    'temperature': mik_tmp, 'cpu': cpu}]
        
       
        return res_base

class MikrotikDetail:
    def mik_vlan(self, ip, community):
         # model
        mik_vl = []
        mik_vlan = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.2.2.1.2')
        for vlan in mik_vlan:
           
            mik_vl.append({'id': vlan.split('=')[0].split('.')[-1].strip(), 
                           'vlan': vlan.split(':')[-1].strip()})
                          
        return mik_vl