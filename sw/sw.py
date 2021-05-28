#! /usr/bin/python3
import os
import sys

sys.path.insert(0, './modules/dlink')
from mac_hex_to_sex import TransformOid
from dlink_base import DlinkBase
from datetime import datetime
from app import app
from sqlalchemy.sql import select
from app import db
from models import Role, User, SwGroup, Sw
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
    try:
        sw = Sw.query.filter(Sw.ip == ip).first()
        community = sw.community_ro
        print(sw.ip)
    except:
        community = 'public'

    i_class = DlinkBase()
    model = i_class.sw_model(ip, community)
    return jsonify({'data': model})


@swApp.route('/api/sw/base', methods=['GET'])
def api_sw_base():
    ip = request.args.get('ip')
    try:
        sw = Sw.query.filter(Sw.ip == ip).first()
        community = sw.community_ro
        print(sw.ip)
    except:
        community = 'public'

    b_class = DlinkBase()
    s = b_class.sw_base(ip, community)
    return jsonify({'data': s})

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
