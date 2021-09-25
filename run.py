#! /usr/bin/python3
from app import app
from app import db
from sw.sw import swApp
from vlan.vlan import vlanApp
from pon.pon import ponApp
from mikrotik.mikrotik import mikrotikApp
import views

### Blueprint
app.register_blueprint(swApp, url_prefix='/sw')
app.register_blueprint(vlanApp, url_prefix='/vlan')
app.register_blueprint(mikrotikApp, url_prefix='/mikrotik')
app.register_blueprint(ponApp, url_prefix='/')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
