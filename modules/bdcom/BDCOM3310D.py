#! /usr/bin/python3
import os
import time
import re


class BD_COM_Base:

    def base_info(self, ip, community):
        # Uptime
        uptime = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.1.3.0')
        # Temp
        temp = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.9.181.1.1.7.1')
        # Cpu
        cpu = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.9.109.1.1.1.1.3.1')
        # Desc
        desc = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.11.1.1.4')

        r_uptime = ''
        r_temp = ''
        r_cpu = ''
        desc = ''
        pattern = "/([E,G]PON[0-9]{1,2})\/([0-9]{1,2})$/"

        for u in uptime:
            t = u.split('=')[1].split(' ')
            r_uptime = t[-3] + ' ' + t[-2] + ' ' + t[-1]
        for tmp in temp:
            r_temp = tmp.split('=')[1].split(' ')[-1].strip()

        for c in cpu:
            r_cpu = c.split('=')[1].split(' ')[-1].strip()

        return {'r_uptime': r_uptime, 'r_temp': r_temp, 'r_cpu': r_cpu}
    def eth_status(self, ip, community):
        pass     

    def port_onu_count(self, ip, community):
        r_pon_count = []
        r_port_holding = []
        # PonPortCount

        pon_count = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + '  1.3.6.1.4.1.3320.101.6.1.1.2')
        for pc in pon_count:
            r_pon_count.append({'port_id': pc.split('=')[0].split('.')[-1].strip(),
                                'onu_count': pc.split('=')[1].split(':')[-1].strip(), 'port_holding': ''})

        port_holding = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + '  1.3.6.1.4.1.3320.101.6.1.1.20')
        for ph in port_holding:
            r_port_holding.append({'port_id': ph.split('=')[0].split('.')[-1].strip(),
                                   'port_holding': ph.split('=')[1].split(':')[-1].strip()})
        for item in r_pon_count:
            try:
                for item2 in r_port_holding:
                    if item['port_id'] == item2['port_id']:
                        item['port_id'] = item['port_id'].replace(item['port_id'], 'EPON0/' + item['port_id'])
                        item['port_holding'] = item2['port_holding']
            except:
                pass
        return r_pon_count

    def port_info(self, ip, community):
        # Onu
        Onu = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.10.5.1.1')
        # OnuPort
        OnuPort = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.31.1.1.1.1')
        # OnuMac
        OnuMac = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.3320.101.10.1.1.3')
        # OnuLenght
        OnuLenght = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.10.1.1.27')
        # OnuSignal
        OnuSignal = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.10.5.1.5')
        # OnuStatus
        OnuStatus = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.2.2.1.8')
        # OnuDescriptiom
        OnuDesc = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.11.1.1.4')

        r_onu = []
        r_onu_port = []
        r_onu_mac = []
        r_onu_lenght = []
        r_onu_status = []
        r_onu_signal = []

        # Собираем Ону
        for o in Onu:
            r_onu.append({'id': o.split('=')[1].split(' ')[-1].strip(),
                          'port': '', 'mac': '', 'onu_lenght': '', 'onu_status': '', 'onu_signal': ''})

        for op in OnuPort:
            r_onu_port.append(
                {'id': op.split('=')[0].split('.')[-1].strip(), 'port': op.split('=')[1].split(' ')[-1].strip()})

        # Собираем маки ону
        for m in OnuMac:
            r_onu_mac.append({'id': m.split('=')[0].split('.')[-1].strip(),
                              'mac': m.split('=')[1].split(':')[-1].strip().replace(' ', ':')})
        # Собираем длину волокна ону
        for l in OnuLenght:
            r_onu_lenght.append({'id': l.split('=')[0].split('.')[-1].strip(),
                                 'onu_lenght': l.split('=')[1].split(':')[-1].strip()})

        for s in OnuStatus:
            r_onu_status.append({'id': s.split('=')[0].split('.')[-1].strip(),
                                 'onu_status': s.split('=')[1].split(':')[-1].strip()})

        for sig in OnuSignal:
            r_onu_signal.append({'id': sig.split('=')[0].split('.')[-1].strip(),
                                 'onu_signal': sig.split('=')[1].split(':')[-1].strip()})                          

        for item in r_onu:
            try:
                for item2 in r_onu_port:
                    if item['id'] == item2['id']:
                        item['id'] = item2['id'].strip()
                        item['port'] = item2['port'].strip('"')
            except:
                pass

            try:
                for item3 in r_onu_mac:
                    if item['id'] in item3['id']:
                        item['mac'] = item3['mac'].strip()
            except:
                pass

            try:
                for item4 in r_onu_lenght:
                    if item['id'] in item4['id']:
                        item['onu_lenght'] = item4['onu_lenght'].strip()
            except:
                pass

            try:
                for item5 in r_onu_status:
                    if item['id'] in item5['id']:
                        item['onu_status'] = item5['onu_status'].strip()
            except:
                pass

            try:
                for item6 in r_onu_signal:
                    if item['id'] in item6['id']:
                        item['onu_signal'] = item6['onu_signal'].strip()
            except:
                pass
        # print(r_onu)
        return r_onu

    def onu_info(self, ip, community, OnuId):
        # OnuPort
        OnuPort = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.31.1.1.1.1.' + OnuId)
        for op in OnuPort:
            onu_port = op.split('=')[1].split(' ')[-1].strip()
        # OnuPortWan
        OnuWan = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.12.1.1.8.' + OnuId)
        for wan in OnuWan:
            onu_wan = wan.split('=')[1].split(' ')[-1].strip()
        # OnuMac
        onu_mac = []
        OnuMac = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.3320.101.10.1.1.3.' + OnuId)
        for m in OnuMac:
            onu_mac.append({'user_mac': m.split('=')[1].split(':')[-1].strip().replace(' ', ':')})
        # OnuSignalRX
        OnuSignalRX = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.10.5.1.5.' + OnuId)
        for sig_rx in OnuSignalRX:
            onu_signal_rx = sig_rx.split('=')[1].split(':')[-1].strip()
        # OnuSignalTX
        OnuSignalTX = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.10.5.1.6.' + OnuId)
        for sig_tx in OnuSignalTX:
            onu_signal_tx = int(sig_tx.split('=')[1].split(':')[-1].strip()) / 10
        # OnuLenght
        OnuLenght = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.10.1.1.27.' + OnuId)
        for l in OnuLenght:
            onu_lenght = l.split('=')[1].split(':')[-1].strip()
        # OnuModel
        OnuModel = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.3320.101.10.1.1.2.' + OnuId)
        for m in OnuModel:
            onu_model = m.split('=')[1].split(':')[-1].strip('"')
        # OnuVendor
        OnuVendor = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.3320.101.10.1.1.1.' + OnuId)
        for v in OnuVendor:
            onu_vendor = v.split('=')[1].split(':')[-1].strip('"')

        # OnuVerHard
        OnuVerHard = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.3320.101.10.1.1.4.' + OnuId)
        for vhr in OnuVerHard:
            onu_ver_hard = vhr.split('=')[1].split(':')[-1].strip('"')

        # OnuVolt
        OnuVolt = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.10.5.1.3.' + OnuId)
        for vol in OnuVolt:
            onu_volt = vol.split('=')[1].split(':')[-1].strip().strip('"')
            onu_volt = int(onu_volt) / 10000
            onu_volt = "%.2f" % onu_volt

        # OnuTemp
        OnuTemp = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.3320.101.10.5.1.2.' + OnuId)
        for temp in OnuTemp:
            onu_temp = temp.split('=')[1].split(':')[-1].strip().strip('"')
            onu_temp = int(onu_temp) / 256
            onu_temp = str("%.1f" % onu_temp) + ' ℃'
        # OnuDesc
        OnuDesc = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.31.1.1.1.18.' + OnuId)
        for d in OnuDesc:
            onu_desc = d.split('=')[1].split(':')[-1].strip('"')

        return [
            {'port': onu_port, 'status_wan': onu_wan, 'signal_rx': onu_signal_rx, 'signal_tx': onu_signal_tx,
             'distance': onu_lenght, 'user_mac': onu_mac, 'log': '', 'vendor': onu_vendor,
             'model': onu_model, 'volt': onu_volt, 'temp': onu_temp, 'ver_hard': onu_ver_hard,
             'ver_soft': '', 'desc': onu_desc}]
