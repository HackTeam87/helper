#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
cd /www/ && gunicorn -w 3 run:app -b :5000 --timeout 600  --access-logfile /var/log/switcher/access.log
#--log-level debug
