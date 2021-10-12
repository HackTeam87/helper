import os

r_all_port_name = []
r_all_onu_desc = []
r_all_onu_port = []
r_user_onu_mac = []

def port_onu_count(IP = '10.2.1.27', COMMUNITY = 'public'):

    port_name = os.popen('snmpwalk -v2c -c ' + COMMUNITY + ' ' + IP + ' 1.3.6.1.4.1.17409.2.3.3.1.1.21')
    for pn in port_name:
        r_all_port_name.append({
        'id': pn.split('=')[0].split('.')[-1].strip(),
        'port_name': pn.split('=')[1].split(':')[-1].strip().strip('"')
        })

    # ALL_ONU_DESC
    all_onu_desc = os.popen('snmpwalk -v2c -c ' + COMMUNITY + ' ' + IP + ' iso.3.6.1.4.1.17409.2.8.4.1.1.2')
    for desc in all_onu_desc:
        r_all_onu_desc.append({
        'id': desc.split('=')[0].split('.')[-1].strip(),
        'onu_desc': desc.split('=')[1].split(':')[-1].strip(),
        'port' : ''
        })


    for item in r_all_onu_desc:
        try:
            for item2 in r_all_port_name:
                r = hex(int(item['id']))
                port_id = (int(r[-4]+r[-3], 16))
                onu_id = (int(r[-2]+r[-1], 16))
                if str(port_id) in item2['id']:
                    item['port'] = item2['port_name'] + ':' + str(onu_id)
        except:
            pass      



    # ALL_ONU_PORT
    # all_onu_port = os.popen('snmpwalk -v2c -c ' + COMMUNITY + ' ' + IP + ' iso.3.6.1.2.1.2.2.1.2')
    # for port_id in all_onu_port:
    #     r_all_onu_port.append({
    #     'id': port_id.split('=')[0].split('.')[-1].strip(),
    #     'port': port_id.split('=')[1].split('.')[-1].split(' ')[-1].strip(),
    #     'user_mac': []
    # })

    # USER_MAC_ADDRESS
    # user_mac = os.popen('snmpwalk -v2c -c ' + COMMUNITY + ' ' + IP + ' iso.3.6.1.4.1.34592.1.3.100.5.4.1.3.10') 
    # for umac in user_mac:
    #     r_user_onu_mac.append({
    #     'id': umac.split('=')[0].split('.')[-2].strip(),
    #     'user_mac': umac.split('=')[1].split(':')[-1].strip().replace(' ', ':')
    #         })

    print(r_all_onu_desc)
# port_onu_count()


def onu_port_id(ID):
     r = hex(int(ID))
     port_id = (int(r[-4]+r[-3], 16))
     onu_id = (int(r[-2]+r[-1], 16))

     print({'port_id': port_id,'onu_id' : onu_id})

onu_port_id('16779285')


