import os

ip = '10.1.1.11'
community ='billing'

#t = ''.join(['%08d' % int(bin(int('0x%s' % i, 16)).replace('0b', '')) for i in data.aplit(' ')])




def get_vlan_tag(vlan_id,sw_port):
    r = os.popen('snmpwalk -v2c -c ' + community + ' ' + ip + ' 1.3.6.1.2.1.17.7.1.4.3.1.4.' + vlan_id)
    for res in r:
        hex_vlan = res.split(':')[1].strip()
    t = list(''.join(['%08d' % int(bin(int('0x%s' % i, 16)).replace('0b', '')) for i in hex_vlan.split(' ')]))
    for i in range(0,int(sw_port)):
        if t[i] == '1':
            print({'port': i+1, 'value': 'U'})
        if t[i] == '0':
            print({'port': i+1, 'value': 'T'})

get_vlan_tag('301','28')
