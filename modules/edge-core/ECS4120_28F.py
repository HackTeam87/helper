#! /usr/bin/python3
import os
import time

# ip = '10.1.4.2'
# community ='billing'



class EdgeCoreBase:
    # Преобразуем  мак адрес с  hex в человеко-понятный вид
    def hex_to_sex(self,int_port,int_mac,vlan_id):
        try:
            if len(hex(int(int_mac[-6])).split('x')[-1]) == 1:
                r1 = '0' + hex(int(int_mac[-6])).split('x')[-1]
            else:
                r1 = hex(int(int_mac[-6])).split('x')[-1]

            if len(hex(int(int_mac[-5])).split('x')[-1]) == 1:
                r2 = '0' + hex(int(int_mac[-5])).split('x')[-1]
            else:
                r2 = hex(int(int_mac[-5])).split('x')[-1]

            if len(hex(int(int_mac[-4])).split('x')[-1]) == 1:
                r3 = '0' + hex(int(int_mac[-4])).split('x')[-1]
            else:
                r3 = hex(int(int_mac[-4])).split('x')[-1]

            if len(hex(int(int_mac[-3])).split('x')[-1]) == 1:
                r4 = '0' + hex(int(int_mac[-3])).split('x')[-1]
            else:
                r4 = hex(int(int_mac[-3])).split('x')[-1]

            if len(hex(int(int_mac[-2])).split('x')[-1]) == 1:
                r5 = '0' + hex(int(int_mac[-2])).split('x')[-1]
            else:
                r5 = hex(int(int_mac[-2])).split('x')[-1]

            if len(hex(int(int_mac[-1])).split('x')[-1]) == 1:
                r6 = '0' + hex(int(int_mac[-1])).split('x')[-1]
            else:
                r6 = hex(int(int_mac[-1])).split('x')[-1]

            mac = r1 + ':' + r2 + ':' + r3 + ':' + r4 + ':' + r5 + ':' + r6

            return {'port_index' : str(int_port),'vlan_id' : str(vlan_id),'mac' : str(mac.upper())}

        except:
            pass
    
    # порт статус если 0 то down
    def port_status(self,uptime):    
        if int(uptime) > 0:
            uptime = '1'
        else:
            uptime = '2'

        return uptime    

    def sw_model(self,ip, community):
        global cp
        # model
        sw_model = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.1.1.0')
        
        for m in sw_model:
            sw_m = m.split(':')[-1].strip()
            
        model = sw_m

        # description
        sw_desc = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.1.5.0')
        for d in sw_desc:
            sw_d = d.split(':')[-1].strip()

        # uptime
        sw_uptime = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.1.3.0')
        for u in sw_uptime:
            t = u.split('=')[1].split(' ')
            sw_u = t[-3] + ' ' + t[-2] + ' ' + t[-1].strip('\n')

        if model == '"ECS4120-28Fv2"':
            count_p = '28'
            cp = '28'
        if model == '"ECS4120-28F"':
            count_p = '28'
            cp = '28' 
        if model == '"8 SFP ports + 4 Gigabit Combo ports L2/L3/L4 managed standalone switch"':
            count_p = '12'
            cp = '12'        
    
        return [{'model': model}, {'sw_d': sw_d}, {'sw_u': sw_u}, {'count_p': count_p}]



    def sw_base(self, ip, community, *community_rw):
        
        # собираем порты
        p_count = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.16.1.1.1.1')
        port_list = []
        try:
            for pc in p_count:
                port_list.append({'port': pc.split('=')[0].split('.')[-1].strip(),
                                  'port_index': pc.split('=')[1].split(':')[-1].strip(),
                                  'status': '','mac_address': [], 'speed': '', 'vlan': '',
                                  'in_c': '', 'out_c': '', 'rx_errors': '', 'tx_errors': '',
                                  'desc': ''})
        except:
            pass
        
        try:
            if cp == '28':

                # порт статус up/down
                p_status = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.259.10.1.45.1.2.1.1.19')
                port_status = []
                for ps in p_status:
                    port_status.append({'port_index': ps.split('=')[0].split('.')[-1].strip(),
                                    'status': self.port_status(ps.split('=')[1].split(':')[-1].strip())})

                # duplex status
                sw_port_duplex_speed = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.259.10.1.45.1.2.1.1.8')
                port_speed = []
                for duplex_speed in sw_port_duplex_speed:
                    port_speed.append({'port_index': duplex_speed.split('=')[0].split('.')[-1].strip(),
                                   'speed': duplex_speed.split('=')[1].split(':')[-1].strip()})                    

                # описание портов  iso.3.6.1.4.1.259.6.10.57.1.2.1.1.2 для 12 портового                    
                sw_port_description = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.259.10.1.45.1.2.1.1.2')
                port_desc = []
                for des in sw_port_description:
                     port_desc.append({'port_index': des.split('=')[0].split('.')[-1].strip(),
                                   'desc': des.split('=')[1].split(':')[-1].strip('"').strip('"\n').strip()}) 

            if cp == '12':

                # порт статус up/down
                p_status = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.4.1.259.6.10.57.1.2.1.1.5')
                port_status = []
                for ps in p_status:
                    port_status.append({'port_index': ps.split('=')[0].split('.')[-1].strip(),
                                    'status': ps.split('=')[1].split(':')[-1].strip()})

                # duplex status
                sw_port_duplex_speed = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.259.6.10.57.1.2.1.1.8')
                port_speed = []
                for duplex_speed in sw_port_duplex_speed:
                    port_speed.append({'port_index': duplex_speed.split('=')[0].split('.')[-1].strip(),
                                   'speed': duplex_speed.split('=')[1].split(':')[-1].strip()})                     

                # описание портов  iso.3.6.1.4.1.259.6.10.57.1.2.1.1.2 для 12 портового
                sw_port_description = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.4.1.259.6.10.57.1.2.1.1.2')
                port_desc = []
                for des in sw_port_description:
                     port_desc.append({'port_index': des.split('=')[0].split('.')[-1].strip(),
                                   'desc': des.split('=')[1].split(':')[-1].strip('"').strip('"\n').strip()})                                                                             
        except:
            pass
        
        # собираем маки
        p_mac_address = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.17.7.1.2.2.1.2')
        port_mac_address = []
        for mac in p_mac_address:
            int_mac = mac.split('=')[0].split('.')
            int_port = mac.split('=')[1].split(':')[1].strip('"\n').strip()
            vlan_id = int_mac[-7]
            port_mac_address.append(self.hex_to_sex(int_port, int_mac, vlan_id))


        try:
            sw_port_out = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.259.10.1.45.1.2.6.1.5')
            port_out = []
            for p_out in sw_port_out:
                 port_out.append({'port_index': p_out.split('=')[0].split('.')[-1].strip(),
                                   'out_c': p_out.split('=')[1].split(':')[-1].strip()})                 
        except:
            pass     


        # in  
        try:
            sw_port_in = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.259.10.1.45.1.2.6.1.2')
            port_in = []
            for p_in in sw_port_in:
                 port_in.append({'port_index': p_in.split('=')[0].split('.')[-1].strip(),
                                   'in_c': p_in.split('=')[1].split(':')[-1].strip()})                 
        except:
            pass

        # out  
        try:
            sw_port_out = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.259.10.1.45.1.2.6.1.5')
            port_out = []
            for p_out in sw_port_out:
                 port_out.append({'port_index': p_out.split('=')[0].split('.')[-1].strip(),
                                   'out_c': p_out.split('=')[1].split(':')[-1].strip()})                 
        except:
            pass



        for item in port_list:
            try:
                for item2 in  port_desc: 
                    if item['port_index'] == item2['port_index']:
                       item['desc'] = item2['desc'] 
            except:
                pass
            try:
                for item3 in  port_status: 
                    if item['port_index'] == item3['port_index']:
                       item['status'] = item3['status'] 
            except:
                pass 

            try:
                for item4 in  port_mac_address: 
                    if item['port_index'] == item4['port_index']:
                         item['mac_address'].append(item4['mac'] + ' ' +'('+ item4['vlan_id']+ ')')
            except:
                pass 

            try:
                for item5 in  port_in: 
                    if item['port_index'] == item5['port_index']:
                         item['in_c'] = item5['in_c'] 
            except:
                pass 

            try:
                for item6 in  port_out: 
                    if item['port_index'] == item6['port_index']:
                         item['out_c'] = item6['out_c'] 
            except:
                pass 

            try:
                for item7 in  port_speed: 
                    if item['port_index'] == item7['port_index']:
                         item['speed'] = item7['speed'] 
            except:
                pass                   
        # print(port_list)
        return port_list




    def cab_init(self, ip, community, community_rw, port):
        pair1 = []
        return [pair1]   
    