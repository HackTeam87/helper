#! /usr/bin/python3
import os
import subprocess
import pymysql.cursors
import pymysql
from datetime import datetime

t = datetime.now()


def sw():
    conn = (pymysql.connect(host='127.0.0.1',
                            user='grin',
                            password='grin1306!',
                            database='switcher',
                            charset='utf8'))

    cursor = conn.cursor()
    cursor.execute(''' SELECT ip,group_id,up,down FROM `sw` LIMIT 0,300 ''')
    ips = []
    for p in cursor:
        ips.append(p)

    for p in ips:
        res = subprocess.call(['ping', '-c', '2', p[0]])
        if res == 0:
            # if p[3] != None and p[2] > p[3]:
            #     print('host_up update not necessary')
            # elif p[3] != None and p[2] < p[3]:
            #     print('host_down need update')
            cursor.execute('UPDATE sw SET status = 1, up=%s WHERE ip=%s', (t, str(p[0])))
            cursor.execute('UPDATE sw_group SET status = 1 WHERE id=%s', str((p[1])))
        elif res == 2:
            cursor.execute('UPDATE sw SET status = 0, down=%s WHERE ip=%s', (t, str(p[0])))
            cursor.execute('UPDATE sw_group SET status = 0 WHERE id=%s', str((p[1])))
        else:
            cursor.execute('UPDATE sw SET status = 0, down=%s WHERE ip=%s', (t, str(p[0])))
            cursor.execute('UPDATE sw_group SET status = 0 WHERE id=%s', str((p[1])))
            print("ping to", p[0], "failed!")
        conn.commit()
    cursor.close()
    conn.close()


sw()
