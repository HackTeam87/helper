#! /usr/bin/python3
import os
import time
from mac_hex_to_huawei import TransformOidHuawei

# ip = '10.2.1.117'
# community ='public'

class HuaweiBase:
    def sw_model(self, ip, community):
        # model
        sw_m = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.1.1.0')
        res = []
        for m in sw_m:
            s_model = m.split('"')
            for test in s_model:
                res.append( test.split(' '))
        model = res[1][0]

        # description
        sw_desc = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.1.5.0')
        for d in sw_desc:
            sw_d = d.split(':')[1].strip().strip('"').strip('"\n').strip('\"').strip('\\')

        # uptime
        sw_uptime = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.1.3.0')
        for u in sw_uptime:
            t = u.split('=')[1].split(' ')
            sw_u = t[-3] + ' ' + t[-2] + ' ' + t[-1]


        if model == 'S2326TP-EI':
            count_p = '26'

        if model == 'S2318TP-EI':
            count_p = '18'


        return [{'model': model}, {'sw_d': sw_d}, {'sw_u': sw_u}, {'count_p': count_p}]

    def sw_base(self, ip, community, *community_rw):
        p_count = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.17.1.4.1.2')
        port_list = []
        try:
            for pc in p_count:
                port_list.append({'port': pc.split('=')[0].split('.')[-1].strip(),
                                  'port_index': pc.split('=')[1].split(':')[-1].strip(),
                                  'status': '','mac_address': []})
        except:
            pass
        p_status = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.2.2.1.8')
        port_status = []
        try:
            for ps in p_status:
                port_status.append({'port_index': ps.split('=')[0].split('.')[-1].strip(),
                                    'status': ps.split('=')[1].split(':')[-1].strip()})
        except:
            pass

        # Список Mac
        sh_mac = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.17.4.3.1.2')
        mac = []
        try:
            for m in sh_mac:
                mac.append((TransformOidHuawei().get_mac(m)))
        except:
            pass

        for item in port_list:

            try:
                for item2 in port_status:
                    if item['port_index'] == item2['port_index']:
                        item['status'] = item2['status']
            except:
                pass

            try:
                for item3 in  mac:
                    if item['port'] == item3['port']:
                        item['mac_address'].append(item3['mac_address'])
            except:
                pass



        return port_list

