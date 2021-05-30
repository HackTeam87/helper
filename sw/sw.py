#! /usr/bin/python3
import os
import sys

sys.path.insert(0, './modules/dlink')
sys.path.insert(0, './modules/huawei')
from dlink_base import DlinkBase
from S2326TP_EI import HuaweiBase
from datetime import datetime
from app import app
from sqlalchemy.sql import select
from app import db
from models import Role, User, SwGroup, Sw, SwModules
from app import user_datastore
from flask import Blueprint, render_template, request, url_for, send_from_directory, redirect, flash, jsonify
from flask_security import login_required

# from sqlalchemy import asc, desc
# from flask_security import login_required

swApp = Blueprint('swApp', __name__, static_folder='static', template_folder='templates')


# SW
@swApp.route('/sw')
@login_required
def sw():
    user = User.query.all()
    return render_template('switcher.html',user=user)


@swApp.route('/sw/add')
@login_required
def sw_add():
    group = SwGroup.query.all()
    sw = Sw.query.all()
    return render_template('sw_add.html', group=group, sw=sw)


@swApp.route("/sw/add/group/save", methods=['POST', 'GET'])
@login_required
def group_add():
    if request.method == 'POST':
        name = request.form.get('name')
        g = SwGroup(name=name)
        db.session.add(g)
        db.session.commit()
    return redirect(url_for('swApp.sw_add'))


@swApp.route("/sw/add/group/delete=<int:id>")
@login_required
def group_delete(id):
    SwGroup.query.filter(SwGroup.id == id).delete()
    db.session.commit()
    return redirect(url_for('swApp.sw_add'))


@swApp.route("/sw/add/switch/save", methods=['POST', 'GET'])
@login_required
def switch_add():
    if request.method == 'POST':
        ip = request.form.get('ip')
        community_ro = request.form.get('community_ro')
        community_rw = request.form.get('community_rw')
        model = request.form.get('model')
        description = request.form.get('description')
        group_id = request.form.get('group_id')
        s = Sw(ip=ip, community_ro=community_ro,community_rw=community_rw, model=model, description=description, group_id=group_id)
        db.session.add(s)
        db.session.commit()
    return redirect(url_for('swApp.sw_add'))


@swApp.route("/sw/add/switch/delete=<int:id>")
@login_required
def switch_delete(id):
    Sw.query.filter(Sw.id == id).delete()
    db.session.commit()
    return redirect(url_for('swApp.sw_add'))


# API
@swApp.route('/api/sw/info', methods=['GET'])
def api_sw_mac():
    ip = str(request.args.get('ip'))
    res = db.session.query(Sw.ip, Sw.modules_id, Sw.community_ro, SwModules.module_name) \
        .outerjoin(SwModules, Sw.modules_id == SwModules.id).filter(Sw.ip == ip).first()
    community = res.community_ro
    if res.module_name == 'd-link':
        try:
            model = DlinkBase().sw_model(ip, community)
            return jsonify({'data': model})
        except:
            pass

    if res.module_name == 'huawei':
        try:
            model = HuaweiBase().sw_model(ip, community)
            return jsonify({'data': model})
        except:
            pass



@swApp.route('/api/sw/base', methods=['GET'])
def api_sw_base():
    ip = str(request.args.get('ip'))
    res = db.session.query(Sw.ip, Sw.modules_id, Sw.community_ro, SwModules.module_name) \
        .outerjoin(SwModules, Sw.modules_id == SwModules.id).filter(Sw.ip == ip).first()
    community = res.community_ro
    if res.module_name == 'd-link':
        try:
            s = DlinkBase().sw_base(ip, community)
            return jsonify({'data': s})
        except:
            pass
    if res.module_name == 'huawei':
        try:
            s = HuaweiBase().sw_base(ip, community)
            return jsonify({'data': s})
        except:
            pass


@swApp.route('/api/sw/port/len', methods=['GET'])
def api_sw_port_len():
    ip = request.args.get('ip')
    port = request.args.get('port')
    try:
        sw = Sw.query.filter(Sw.ip == ip).first()
        community = sw.community_ro
        community_rw = sw.community_rw
        print(sw.ip)
    except:
        community = 'public'
        community_rw = 'private'

    b_class = DlinkBase()
    s = b_class.cab_init(ip,  community, community_rw, port)
    return jsonify({'data': s})
