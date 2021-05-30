#! /usr/bin/python3

class TransformOidHuawei:

    def hex_to_sex(self,int_port,int_mac):
        try:
            # Преобразуем  мак адрес с  hex в человеко-понятный вид
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
            return {'port' : str(int_port),'mac_address' : str(mac.upper())}

        except:
            pass
    def get_mac(self,oid):
        try:
            s = oid
            int_mac = s.split(' = ')[0].split('.')
            int_port = s.split(' = ')[1].split(':')[1].strip().strip('\n')
            return self.hex_to_sex(int_port, int_mac)
        except:
            pass


