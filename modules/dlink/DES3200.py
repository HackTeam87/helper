#! /usr/bin/python3
import os
import time
from mac_hex_to_huawei import TransformOidHuawei

# ip = '10.2.1.117'
# community ='public'

class DlinkBase:
    # Определяем модель свитча
    def sw_model(self, ip, community):
        # Имя свитча
        sw_n = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.1.1')
        # Описание свитча
        sw_desc = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.1.5')
        # Аптайм
        sw_uptime = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.1.3')

        port_n = ''
        sw_d = ''
        sw_u = ''

        for d in sw_desc:
            sw_d = d.split(':')[1].strip().strip('"').strip('"\n').strip('\"').strip('\\')
        for u in sw_uptime:
            t = u.split('=')[1].split(' ')
            sw_u = t[-3] + ' ' + t[-2] + ' ' + t[-1]

        for n in sw_n:
            model = n.split(':')[1].strip().strip('"')
            if model == 'D-Link DES-1228/ME Metro Ethernet Switch':
                port_n = 28
            if model == 'D-Link DES-3200-26 Fast Ethernet Switch':
                port_n = 26
            if model == 'DES-3200-26/C1 Fast Ethernet Switch':
                port_n = 26
            if model == 'DES-3200-28/C1 Fast Ethernet Switch':
                port_n = 28
            if model == 'D-Link DES-3200-28 Fast Ethernet Switch':
                port_n = 28
            if model == 'DES-3200-28F/C1 Fast Ethernet Switch':
                port_n = 28
            if model == 'D-Link DES-3200-18 Fast Ethernet Switch':
                port_n = 18
            if model == 'DES-1210-28/ME/B2':
                port_n = 28
            if model == 'DGS-3420-28SC Gigabit Ethernet Switch':
                port_n = 28
            if model == 'DGS-3000-26TC Gigabit Ethernet Switch':
                port_n = 26

        return [{'model': model}, {'sw_d': sw_d}, {'sw_u': sw_u}, {'count_p': port_n}]

    def sw_base(self, ip, community, *community_rw):
        p_count = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.17.1.4.1.2')
        port_list = []
        try:
            for pc in p_count:
                port_list.append({'port': pc.split('=')[0].split('.')[-1].strip(),
                                  'port_index': pc.split('=')[1].split(':')[-1].strip(),
                                  'status': '','mac_address': [], 'speed': '', 'vlan': '',
                                  'in_c': '', 'out_c': '', 'rx_errors': '', 'tx_errors': ''})
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

        p_speed = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.2.2.1.5')
        port_speed = []
        try:
            for psd in p_speed:
                port_speed.append({'port_index': psd.split('=')[0].split('.')[-1].strip(),
                                    'speed': psd.split('=')[1].split(':')[-1].strip()})
        except:
            pass

        p_vlan = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.17.7.1.4.5.1.1')
        port_vlan = []
        try:
            for vlan in p_vlan:
                port_vlan.append({'port_index': vlan.split('=')[0].split('.')[-1].strip(),
                                   'vlan': vlan.split('=')[1].split(':')[-1].strip()})
        except:
            pass

        p_count_in = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.31.1.1.1.6')
        port_count_in = []
        try:
            for count_in in p_count_in:
                port_count_in.append({'port_index': count_in.split('=')[0].split('.')[-1].strip(),
                                  'in_c': count_in.split('=')[1].split(':')[-1].strip()})
        except:
            pass

        p_count_out = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.2.1.31.1.1.1.10')
        port_count_out = []
        try:
            for count_out in p_count_out:
                port_count_out.append({'port_index': count_out.split('=')[0].split('.')[-1].strip(),
                                      'out_c': count_out.split('=')[1].split(':')[-1].strip()})
        except:
            pass

        p_rx_errors = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.2.2.1.14')
        port_rx_errors = []
        try:
            for rx_errors in p_rx_errors:
                port_rx_errors.append({'port_index': rx_errors.split('=')[0].split('.')[-1].strip(),
                                       'rx_errors': rx_errors.split('=')[1].split(':')[-1].strip()})
        except:
            pass

        p_tx_errors = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.2.2.1.20')
        port_tx_errors = []
        try:
            for tx_errors in p_tx_errors:
                port_tx_errors.append({'port_index': tx_errors.split('=')[0].split('.')[-1].strip(),
                                       'tx_errors': tx_errors.split('=')[1].split(':')[-1].strip()})
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

            try:
                for item4 in port_speed:
                    if item['port_index'] == item4['port_index']:
                        item['speed'] = item4['speed']
            except:
                pass

            try:
                for item5 in port_vlan:
                    if item['port_index'] == item5['port_index']:
                        item['vlan'] = item5['vlan']
            except:
                pass

            try:
                for item6 in port_count_in:
                    if item['port_index'] == item6['port_index']:
                        item['in_c'] = item6['in_c']
            except:
                pass

            try:
                for item7 in port_count_out:
                    if item['port_index'] == item7['port_index']:
                        item['out_c'] = item7['out_c']
            except:
                pass

            try:
                for item8 in port_rx_errors:
                    if item['port_index'] == item8['port_index']:
                        item['rx_errors'] = item8['rx_errors']
            except:
                pass

            try:
                for item9 in port_tx_errors:
                    if item['port_index'] == item9['port_index']:
                        item['tx_errors'] = item9['tx_errors']
            except:
                pass



        return port_list

