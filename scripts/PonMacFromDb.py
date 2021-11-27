#!/usr/bin/env python3
import sys
import subprocess
import pymysql.cursors
import pymysql

try:
    DevIp=(sys.argv[1])
except:
    pass


def db():
    
    conn = ( pymysql.connect(host = '185.190.150.7',
                             user = 'script',
                             password = 'golden1306!',
                             database = 'service',
                             charset='utf8' ) )

    cursor = conn.cursor()
    cursor.execute('''SELECT cl.agreement, eq.ip, b.mac, b.port
                      FROM eq_bindings b
                      JOIN equipment eq on eq.id = b.switch
                      JOIN client_prices act on act.id = b.activation
                      JOIN clients cl on cl.id = act.agreement
                      WHERE eq.ip = %s''',(DevIp))
    for r in cursor:
        try:
            command_success = 'python3 user_pon.py ' + str(r[1]) +' '+ str(r[2])+' '+str(r[0])
            subprocess.check_output(
            [command_success], shell=True)
            print('success: '+str(r[0])) 
        except:
             print('error: '+str(r[0]))
             pass     
if __name__ == '__main__':                            
    db()

 