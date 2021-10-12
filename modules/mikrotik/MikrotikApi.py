# -*- coding: utf-8 -*-
#!/usr/bin/python3
import routeros_api

class MikApi:
    
    def getCommand(self, host, uname, passwd, port, command):

        connection = routeros_api.RouterOsApiPool(host, port=int(port),
                                                  username=uname,
                                                  password=passwd,
                                                  plaintext_login=True
                                                  )
        api = connection.get_api()
        list = api.get_resource(command)
        result = list.get()
        connection.disconnect()
        

        return(result)
        #encoding="utf-8"
        # self.getlease(host, command)


# print(result[0]['id'])
# print(result[0]['address'])
# print(result[0]['mac-address'])
# print(result[0]['server'])
# print(result[0]['status'])
# print(result[0]['last-seen'])
#
