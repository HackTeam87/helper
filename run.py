#! /usr/bin/python3
from app import app
from app import db
from vlan.vlan import vlanApp
from pon.pon import ponApp
import views

### Blueprint
app.register_blueprint(vlanApp, url_prefix='/vlan')
app.register_blueprint(ponApp, url_prefix='/pon')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
