#! /usr/bin/python3
import sys

sys.path.insert(0, './modules/mikrotik')
from Mikrotik import MikrotikBase
from Mikrotik import MikrotikDetail
from app import *
from flask import Blueprint, render_template, request, url_for, send_from_directory, redirect, flash, jsonify
from flask import session
from models import Role, User, SwGroup, Sw, SwModules
# from keystoneclient.session import Session


# from sqlalchemy import asc, desc
# from flask_security import login_required

mikrotikApp = Blueprint('mikrotikApp', __name__, static_folder='static', template_folder='templates')


# Mikrotik_INFO
@mikrotikApp.route("/", methods=['POST', 'GET'])
def mikrotik_list():
    group = SwGroup.query.all()
    # sw = Sw.query.filter(Sw.model == 'Mikrotik'+'*').all()
    sw = Sw.query.filter(Sw.model.like('Mikrotik%')).order_by(Sw.sort_id.asc()).all()
    # olt = Olt.query.order_by(Olt.sort_id.asc()).all()
    return render_template('mikrotik.html', group=group, sw=sw)


# API
@mikrotikApp.route("/api/mikrotik/base", methods=['POST', 'GET'])
def api_mikrotik_base():
    ip = str(request.args.get('ip'))
    res = db.session.query(Sw.ip, Sw.modules_id, Sw.community_ro, SwModules.module_name) \
        .outerjoin(SwModules, Sw.modules_id == SwModules.id).filter(Sw.ip == ip).first()
    community = res.community_ro
    device = Sw.query.filter(Sw.ip == ip).first()
    
    if res.module_name == 'Mikrotik':
        try:
            m = MikrotikBase().mik_model(ip, community)
            device.uptime = str(m[0]['uptime'])
            db.session.commit()
            return jsonify({'data': m})
        except:
            pass

 # API Detail
@mikrotikApp.route("/api/mikrotik/detail", methods=['POST', 'GET'])
def api_mikrotik_vlan():
    ip = str(request.args.get('ip'))
    res = db.session.query(Sw.ip, Sw.modules_id, Sw.community_ro, SwModules.module_name) \
        .outerjoin(SwModules, Sw.modules_id == SwModules.id).filter(Sw.ip == ip).first()
    community = res.community_ro

    if res.module_name == 'Mikrotik':
        try:
            mb = MikrotikDetail().mik_vlan(ip, community)
            print(mb)
            return jsonify({'data': mb})
        except:
            pass        
    