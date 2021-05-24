#! /usr/bin/python3
import os
import time
from mac_hex_to_sex import TransformOid


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

    def vlan_name(self, ip, community):
        sw_v = ''
        sw_vl = ''
        # Версия прошивки
        sw_sys_ver = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.16.19.2.0')
        sw_vlan_name = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.17.7.1.4.3.1.1')

        for v in sw_sys_ver:
            sw_v = v.split('=')[1].split(' ')[-1].strip('"\n')

        for vl in sw_vlan_name:
            sw_vl = vl.split('=')[1].split(' ')[-1].strip('"\n')

        return [{'sw_v': sw_v}, {'sw_vl': sw_vl}]

    def sw_base(self, ip, community, *community_rw):

        # Список Mac
        sh_mac = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.17.7.1.2.2.1.2')
        # Порт статус
        sw_port_status = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.2.2.1.8')
        # Скорость порта
        sw_port_speed = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.2.2.1.5')

        # IN/OUT
        sw_port_in = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.2.2.1.10')
        sw_port_out = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.2.2.1.16')

        def in_out():
            in_count = []
            for in_n in sw_port_in:
                in_count.append(
                    {'port': in_n.split('=')[0].split('.')[-1].strip(),
                     'in': in_n.split('=')[1].split(' ')[-1].strip()})
            return in_count

        # port description
        sw_port_description = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.31.1.1.1.18')

        def description():
            desc = []
            for des in sw_port_description:
                desc.append({'port': des.split('=')[0].split('.')[-1].strip(),
                             'desc': des.split('=')[1].split(' ')[-1].strip('"').strip('"\n')})
            return desc

        def out_in():
            out_count = []
            for out_n in sw_port_out:
                out_count.append({'port': out_n.split('=')[0].split('.')[-1].strip(),
                                  'out': out_n.split('=')[1].split(' ')[-1].strip()})
            return out_count

        # порт статус UP/DOWN
        def port_status():
            po = []
            for p in sw_port_status:
                po.append(
                    {'port': p.split('=')[0].split('.')[-1].strip(),
                     'status': p.split('=')[1].split(' ')[-1].strip()})
            return po

        # список интерфейсов
        def port_count():
            try:
                m_sw = self.sw_model(ip, community)[-1]['count_p']
                port_list = []
                for n in port_status():
                    if n['port'] and int(n['port']) < int(m_sw + 1) not in port_list:
                        port_list.append(
                            {'desc': '', 'port': n['port'], 'mac_address': [], 'vlan': [], 'status': n['status'],
                             'speed': '', 'in_c': '', 'out_c': ''})
            except:
                print('not found device model')
            return port_list

        # скорость по портам
        def port_speed():
            speed = []
            for ps in sw_port_speed:
                speed.append({'port': ps.split('=')[0].split('.')[-1].strip(),
                              'speed': ps.split('=')[1].split(' ')[-1].strip()})
            return speed

        # маки за портами в человекопонятном виде
        def mac():
            ma = []
            for m in sh_mac:
                ma.append((TransformOid().get_mac(m)))
            return ma

        pc = port_count()
        ma = mac()
        ps = port_speed()
        in_n = in_out()
        out_n = out_in()
        desc = description()

        for c in pc:

            try:
                if str(desc[int(c['port'])]['port'].strip() == str(c['port'].strip())):
                    for d in desc:
                        if d['port'].strip() == c['port'].strip():
                            c['desc'] = d['desc']
            except:
                pass
            try:
                if str(in_n[int(c['port'])]['port'].strip() == str(c['port'].strip())):
                    for i in in_n:
                        if i['port'].strip() == c['port'].strip():
                            c['in_c'] = i['in']
            except:
                pass

            try:
                if str(out_n[int(c['port'])]['port'].strip() == str(c['port'].strip())):
                    for o in out_n:
                        if o['port'].strip() == c['port'].strip():
                            c['out_c'] = o['out']
            except:
                pass
            try:
                if str(ps[int(c['port'])]['port'].strip() == str(c['port'].strip())):
                    for p in ps:
                        if p['port'].strip() == c['port'].strip():
                            c['speed'] = p['speed']
            except:
                pass
            try:
                if str(ma[int(c['port'])]['port'].strip() == str(c['port'].strip())):
                    for m in ma:
                        if m['port'].strip() == c['port'].strip():
                            c['mac_address'].append(m['mac'] + ' ' + '(' + m['vlan_id'] + ')')
                            if m['vlan_id'] not in c['vlan']:
                                c['vlan'].append(m['vlan_id'])
            except:
                pass

        # print(pc)
        return (pc)

    def cab_init(self, ip, community, community_rw, port):
        for cinit in os.popen(
                'snmpset -v2c -c ' + community_rw + ' ' + ip + ' 1.3.6.1.4.1.171.12.58.1.1.1.12.' + str(port) + ' i 1'):
            time.sleep(3)

        for len1 in os.popen(
                'snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.171.12.58.1.1.1.8.' + str(port)):
            pair1 = len1.split('=')[1].split(' ')[-1].strip()

        for len2 in os.popen(
                'snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.171.12.58.1.1.1.9.' + str(port)):
            pair2 = len2.split('=')[1].split(' ')[-1].strip()

        for len3 in os.popen(
                'snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.171.12.58.1.1.1.10.' + str(port)):
            pair3 = len3.split('=')[1].split(' ')[-1].strip()

        for len4 in os.popen(
                'snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.171.12.58.1.1.1.11.' + str(port)):
            pair4 = len4.split('=')[1].split(' ')[-1].strip()

        # result_len = {'pair1': pair1, 'pair2': pair2}
        # Возможные
        # значения:
        #
        # ok(0)
        # open(1)
        # short(2)
        # open - short(3)
        # crosstalk(4)
        # unknown(5)
        # count(6)
        # no - cable(7)
        # other(8)

        # Диагностика кабеля
        # cтатус первой пары
        for c1 in os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.171.12.58.1.1.1.4.' + str(port)):
            test1 = c1.split('=')[1].split(' ')[-1].strip()
            if test1 == '0':
                test1 = 'ok'
            if test1 == '1':
                test1 = 'open'
            if test1 == '2':
                test1 = 'short'
            if test1 == '3':
                test1 = 'open-short'
            if test1 == '4':
                test1 = 'crosstalk'
            if test1 == '5':
                test1 = 'unknown'
            if test1 == '6':
                test1 = 'count'
            if test1 == '7':
                test1 = 'no-cable'
            if test1 == '8':
                test1 = 'other'

        # cтатус второй пары
        for c2 in os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.171.12.58.1.1.1.5.' + str(port)):
            test2 = c2.split('=')[1].split(' ')[-1].strip()
            if test2 == '0':
                test2 = 'ok'
            if test2 == '1':
                test2 = 'open'
            if test2 == '2':
                test2 = 'short'
            if test2 == '3':
                test2 = 'open-short'
            if test2 == '4':
                test2 = 'crosstalk'
            if test2 == '5':
                test2 = 'unknown'
            if test2 == '6':
                test2 = 'count'
            if test2 == '7':
                test2 = 'no-cable'
            if test2 == '8':
                test2 = 'other'

        # cтатус третьей пары
        for c3 in os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.171.12.58.1.1.1.6.' + str(port)):
            test3 = c3.split('=')[1].split(' ')[-1].strip()
            if test3 == '0':
                test3 = 'ok'
            if test3 == '1':
                test3 = 'open'
            if test3 == '2':
                test3 = 'short'
            if test3 == '3':
                test3 = 'open-short'
            if test3 == '4':
                test3 = 'crosstalk'
            if test3 == '5':
                test3 = 'unknown'
            if test3 == '6':
                test3 = 'count'
            if test3 == '7':
                test3 = 'no-cable'
            if test3 == '8':
                test3 = 'other'

        # cтатус четвертой пары
        for c4 in os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.171.12.58.1.1.1.7.' + str(port)):
            test4 = c4.split('=')[1].split(' ')[-1].strip()
            if test4 == '0':
                test4 = 'ok'
            if test4 == '1':
                test4 = 'open'
            if test4 == '2':
                test4 = 'short'
            if test4 == '3':
                test4 = 'open-short'
            if test4 == '4':
                test4 = 'crosstalk'
            if test4 == '5':
                test4 = 'unknown'
            if test4 == '6':
                test4 = 'count'
            if test4 == '7':
                test4 = 'no-cable'
            if test4 == '8':
                test4 = 'other'

        return [test1, pair1, test2, pair2, test3, pair3, test4, pair4]
