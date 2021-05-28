#! /usr/bin/python3
import os
import time
import re


class C_DATA_Base_FD1208S:
    def base_info(self, ip, community):
        # Uptime
        r_uptime = ''
        uptime = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.1.2.1.1.5')
        for u in uptime:
            t = u.split('=')[1].split(' ')
            r_uptime = t[-3] + ' ' + t[-2] + ' ' + t[-1]
        return {'r_uptime': r_uptime}

        # olt_model = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.1.2.1.1.3')
        # olt_desc = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.1.2.1.1.2')
        # base_olt = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.1.2.1')
        # # All_Ports
        # all_ports = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.3.1.1.21')

    def port_onu_count(self, ip, community):
        r_all_onu_num = []
        r_all_onu_mac = []
        r_all_onu_signal = []
        r_all_onu_status = []
        r_all_onu_len = []

        all_onu_num = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.34592.1.3.4.1.1.14')
        for aon in all_onu_num:
            r_all_onu_num.append({'port': 'pon0/0/' +
                                          aon.split('=')[0].split('.')[-2].strip() +
                                          ':' + aon.split('=')[0].split('.')[-1].strip()})
        # print(r_all_onu_num)

        # All_Onu_Mac
        all_onu_mac = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.4.1.1.7')
        # Собираем массив ону-мак

        repls = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
                 '10': '10', '11': '11', '12': '12', '13': '13', '14': '14', '15': '15', '16': '16'}
        for aom in all_onu_mac:
            r = hex(int(aom.split('=')[0].split('.')[-1].strip()))
            port_id = int(r[-4] + r[-3], 16)
            onu_id = int(r[-2] + r[-1], 16)

            r_all_onu_mac.append(
                {'id': aom.split('=')[0].split('.')[-1].strip(), 'port': 'pon0/0/' + str(port_id) + ':' + str(onu_id),
                 'mac': aom.split('=')[1].split(':')[-1].strip().replace(' ', ':'),
                 'onu_signal': '', 'onu_lenght': '', 'onu_status': ''})

        onu_signal = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.3.6.1.2')
        for aos in onu_signal:
            r_all_onu_signal.append({'id': aos.split('=')[0].split('.')[-1].strip(),
                                     'onu_signal': aos.split('=')[1].split(':')[-1].strip()})

        onu_status = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.17409.2.3.4.1.1.8')
        for aost in onu_status:
            r_all_onu_status.append({'id': aost.split('=')[0].split('.')[-1].strip(),
                                     'onu_status': aost.split('=')[1].split(':')[-1].strip()})

        onu_len = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.17409.2.3.4.1.1.15')
        for ol in onu_len:
            r_all_onu_len.append({'id': ol.split('=')[0].split('.')[-1].strip(),
                                  'onu_lenght': ol.split('=')[1].split(':')[-1].strip()})

        for item in r_all_onu_mac:
            try:
                for item2 in r_all_onu_signal:
                    if item['id'] in item2['id']:
                        item['onu_signal'] = '-' + item2['onu_signal']
            except:
                pass

            try:
                for item3 in r_all_onu_status:
                    if item['id'] in item3['id']:
                        item['onu_status'] = item3['onu_status']
            except:
                pass

            try:
                for item4 in r_all_onu_len:
                    if item['id'] in item4['id']:
                        item['onu_lenght'] = item4['onu_lenght']
            except:
                pass

        return r_all_onu_mac

    def port_onu_active(self, ip, community):
        r_all_onu_active = []
        r_port_holding = []

        all_onu_active = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.3.1.1.8')
        for ana in all_onu_active:
            r_all_onu_active.append({'port_id': ana.split('=')[0].split('.')[-1].strip(),
                                     'onu_count': ana.split('=')[1].split(':')[-1].strip(), 'port_holding': ''})

        port_holding = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.3.1.1.7')
        for ph in port_holding:
            r_port_holding.append({'port_id': ph.split('=')[0].split('.')[-1].strip(),
                                   'port_holding': ph.split('=')[1].split(':')[-1].strip()})

        for item in r_all_onu_active:
            try:
                for item2 in r_port_holding:
                    if item['port_id'] == item2['port_id']:
                        item['port_id'] = item['port_id'].replace(item['port_id'], 'EPON0/' + item['port_id'])
                        item['port_holding'] = item2['port_holding']
            except:
                pass
        # print(r_all_onu_active)
        return r_all_onu_active



    def onu_info(self, ip, community, OnuId):
        # Status_Wan
        status_wan = []
        onuStatusWan = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.17409.2.3.5.1.1.5.' + OnuId)
        for sts in onuStatusWan:
            status_wan.append(sts.split('=')[1].split(':')[-1].strip('"').strip())

        # User_Mac
        onu_user_mac = []
        onuUserMac = os.popen(
            'snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.34592.1.3.100.13.1.1.5.' + OnuId)
        for um in onuUserMac:
            onu_user_mac.append({'user_port': um.split('=')[0].split('.')[-2].strip(),
                                 'user_mac': um.split('=')[1].split(':')[-1].strip().replace(' ', ':')})
        # Onu_Signal
        onuSignal = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.3.6.1.2.' + OnuId)
        for s in onuSignal:
            onu_signal = int(s.split('=')[1].split(':')[-1].strip('"').strip()) / 10
        # Onu_distance
        onuDistance = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.4.1.1.15.' + OnuId)
        for d in onuDistance:
            onu_distance = d.split('=')[1].split(':')[-1].strip('"').strip()

        # Onu_Vendor
        onuVendor = os.popen(
            'snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.4.1.1.25.' + OnuId)
        for v in onuVendor:
            onu_vendor = v.split('=')[1].split(':')[-1].strip('"').strip()

        # Onu_Model
        onuModel = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.4.1.1.26.' + OnuId)
        for m in onuModel:
            onu_model = m.split('=')[1].split(':')[-1].strip('"').strip()

        # Onu_Hard
        onuVerHard = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.4.1.1.27.' + OnuId)
        for vh in onuVerHard:
            onu_ver_hard = vh.split('=')[1].split(':')[-1].strip('"').strip()
        # Onu_Soft
        onuVerSoft = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.4.1.1.13.' + OnuId)
        for vs in onuVerSoft:
            onu_ver_soft = vs.split('=')[1].split(':')[-1].strip('"').strip()

        # OnuLog
        OnuLog = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.34592.1.3.100.12.3.1.1.7.' + OnuId)
        for l in OnuLog:
            onu_log = l.split('=')[1].split(':')[-1].strip('"').strip()

        # OnuDesc
        OnuDesc = os.popen(
            'snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.4.1.1.2.' + OnuId)
        for ds in OnuDesc:
            onu_desc = ds.split('=')[1].split(':')[-1].strip('"').strip()

        return [{'status_wan': status_wan, 'signal': onu_signal, 'distance': onu_distance,
                 'user_mac': onu_user_mac, 'log': onu_log, 'vendor': onu_vendor, 'model': onu_model,
                 'ver_hard': onu_ver_hard, 'ver_soft': onu_ver_soft, 'desc': onu_desc}]


    def test2(self):
        # All_Onu_Wan_Mac
        all_onu_wan_mac = os.popen(
            'snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.34592.1.3.100.13.1.1.5.16779017')
        sfp_status = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.2.2.1.8')
        # Status_onu
        status_onu = os.popen(
            'snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.17409.2.3.4.1.1.8.16779009')
        # Status_onu_wan
        status_onu_wan = os.popen(
            'snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.17409.2.3.5.1.1.5.16779009')
        # Onu_Desc
        onu_desc = os.popen(
            'snmpwalk -v2c -c ' + community + ' ' + ip + ' iso.3.6.1.4.1.17409.2.3.4.1.1.2.16779010')
        # Onu_Vendor
        onu_vendor = os.popen(
            'snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.4.1.1.26.16779009')
        onu_signal = os.popen(
            'snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.17409.2.3.3.6.1.2.16779009 ')
        pass

