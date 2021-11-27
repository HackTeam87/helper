#! /usr/bin/python3
import sys

sys.path.insert(0, './modules/mikrotik')
from Mikrotik import MikrotikBase
from Mikrotik import MikrotikDetail
from MikrotikApi import MikApi
from app import *
from flask import Blueprint, render_template, request, url_for, send_from_directory, redirect, flash, jsonify
from flask import session
from models import Role, User, SwGroup, Sw, SwModules
# from keystoneclient.session import Session
from flask_security import login_required


# from sqlalchemy import asc, desc
# from flask_security import login_required

mikrotikApp = Blueprint('mikrotikApp', __name__, static_folder='static', template_folder='templates')


# Mikrotik_INFO
@mikrotikApp.route("/", methods=['POST', 'GET'])
@login_required
def mikrotik_list():
    # group = SwGroup.query.all()
    # sw = Sw.query.filter(Sw.model == 'Mikrotik'+'*').all()
    sw = Sw.query.filter(Sw.model.like('Mikrotik%')).order_by(Sw.sort_id.asc()).all()
    group = SwGroup.query.filter(SwGroup.name.like('Mikrotik%')).all()
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
            return jsonify({'data': mb})
        except:
            pass        
    

# API Api
@mikrotikApp.route("/api/mikrotik/api", methods=['POST', 'GET'])
def api_mikrotik_api():
    ip = str(request.args.get('ip'))
    command = str(request.args.get('command'))
    res = db.session.query(Sw.ip, Sw.modules_id, Sw.community_ro,Sw.api_login, 
    Sw.api_password, Sw.api_port, SwModules.module_name) \
        .outerjoin(SwModules, Sw.modules_id == SwModules.id).filter(Sw.ip == ip).first()
    login = res.api_login
    password = res.api_password
    port = res.api_port
    
    if res.module_name == 'Mikrotik':
        try:
            ma = MikApi().getCommand(ip, login, password, port, command)
            return jsonify({'data': ma})
        except:
            pass         