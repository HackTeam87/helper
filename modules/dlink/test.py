#! /usr/bin/python3
# маки за портами в человекопонятном виде
import os
from mac_hex_to_sex import TransformOid

ip = '10.1.1.11'
community ='billing'

sw_port_status = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.2.2.1.8')
sh_mac = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.2.1.17.7.1.2.2.1.2')

# Диагностика кабеля
sw_cab_lenght = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.4.1.171.12.58.1.1.1.8')


# Возможные значения:
#
# ok(0)
# open(1)
# short(2)
# open-short(3)
# crosstalk(4)
# unknown(5)
# count(6)
# no-cable(7)
# other(8)

sw_cab_status1 = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.171.12.58.1.1.1.4')
sw_cab_status2 = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.171.12.58.1.1.1.5')
sw_cab_status3 = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.171.12.58.1.1.1.6')
sw_cab_status4 = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' .1.3.6.1.4.1.171.12.58.1.1.1.7')



def cable_d():
    cab = []
    cabn = []
    for c in sw_cab_diag_1:
        cab.append(
            {'port': c.split('=')[0].split('.')[-1].strip(), 'cable': []}
             )
    for c2 in sw_cab_diag_1,sw_cab_diag_2,sw_cab_diag_3,sw_cab_diag_4:
        try:
            for c3 in c2:
                cab[int(c3.split('=')[0].split('.')[-1].strip())]['cable'].append(c3.split('=')[1].split(' ')[-1].strip())
        except:
            pass
    print(cab)
cable_d()


# порт статус UP/DOWN
def port_status():
    po = []
    for p in sw_port_status:
        po.append(
            {'port': p.split('=')[0].split('.')[-1].strip(), 'status': p.split('=')[1].split(' ')[-1].strip()})
    return po

# маки за портами в человекопонятном виде
def mac():
    ma = []
    for m in sh_mac:
        ma.append((TransformOid().get_mac(m)))
    return ma

# список интерфейсов
def port_count():
    port_list = []
    for n in port_status():
        if n['port'] not in port_list:
            port_list.append({'port': n['port'], 'mac-address': []})
    return port_list


ma = mac()
pc = port_count()
mac_list = []

for c in pc:
    try:
        if str(ma[int(c['port'])]['port'].strip() == str(c['port'].strip())):
            for m in ma:
                if m['port'].strip() == c['port'].strip():
                    c['mac-address'].append(m['mac'])
    except:
        pass

