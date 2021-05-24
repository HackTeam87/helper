#! /usr/bin/python3
#Import Modules
import os
import sys
sys.path.insert(0, './modules/dlink')
from mac_hex_to_sex import TransformOid
from dlink_base import DlinkBase
from datetime import datetime
from app import app
from sqlalchemy.sql import select
from app import db
from models import Role, User,  SwGroup, Sw
from app import user_datastore
from flask import render_template, Response, request, flash, session, url_for, redirect, make_response, jsonify
from flask_security import login_required


#Route

#Users
@app.route('/user/list', methods=['POST', 'GET'])
def user_list():
    role = Role.query.all()
    user = User.query.all()
    return render_template('/users/user_list.html',  role=role, user=user)

@app.route("/user/delete=<int:id>")
def user_delete(id):
    User.query.filter(User.id == id).delete()
    db.session.commit()
    return redirect(url_for('user_list'))

@app.route("/user/add/save", methods=['POST', 'GET'])
@login_required
def user_add():
    if request.method == 'POST':
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        roles = request.form.get('roles')
        u = User(last_name=last_name, email=email, password=password)
        r = Role.query.filter(Role.id == roles).first()
        user_datastore.add_role_to_user(u,r)
        db.session.commit()

    return redirect(url_for('user_list'))


# Switch All
@app.route('/', methods=['POST', 'GET'])
def index():
    group = SwGroup.query.all()
    sw = Sw.query.all()
    return render_template('index.html', group=group, sw=sw)


# SW
@app.route('/sw')
@login_required
def sw():
    user = User.query.all()
    return render_template('switcher.html',user=user)


@app.route('/sw/add')
@login_required
def sw_add():
    group = SwGroup.query.all()
    sw = Sw.query.all()
    return render_template('sw/sw_add.html', group=group, sw=sw)


@app.route("/sw/add/group/save", methods=['POST', 'GET'])
@login_required
def group_add():
    if request.method == 'POST':
        name = request.form.get('name')
        g = SwGroup(name=name)
        db.session.add(g)
        db.session.commit()
    return redirect(url_for('sw_add'))


@app.route("/sw/add/group/delete=<int:id>")
@login_required
def group_delete(id):
    SwGroup.query.filter(SwGroup.id == id).delete()
    db.session.commit()
    return redirect(url_for('sw_add'))


@app.route("/sw/add/switch/save", methods=['POST', 'GET'])
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
    return redirect(url_for('sw_add'))


@app.route("/sw/add/switch/delete=<int:id>")
@login_required
def switch_delete(id):
    Sw.query.filter(Sw.id == id).delete()
    db.session.commit()
    return redirect(url_for('sw_add'))


# API
@app.route('/api/sw/info', methods=['GET'])
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


@app.route('/api/sw/base', methods=['GET'])
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

@app.route('/api/sw/port/len', methods=['GET'])
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

# Login
@app.route("/login", methods=['POST', 'GET'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    user = User.query.filter_by(login=login, password=password).first()
    if not user:
        flash('Please enter correct data')
        return render_template('login.html')
    return render_template('index.html')


# @app.errorhandler(404)
# def page_not_found(e):
#     return '<h1 style="text-align:center;color:red;">Error 404 , Страница не найдена;)<h1/>' \
#            '<p style="text-align:center;">Текст ошибки :</p>' + '<p style="text-align:center;">' + str(e) + '<p/>' \
#             '<br> <p style="text-align:center;">Обратитесь к администратору</p> <br>'
#
#
# @app.errorhandler(500)
# def server_error(e):
#     return '<h1 style="text-align:center;color:red;">Error 500 , Ошибка сервера;)<h1/>' \
#            '<p style="text-align:center;">Текст ошибки :</p>' + '<p style="text-align:center;">' + str(e) + '<p/>' \
#            '<br> <p style="text-align:center;">Обратитесь к администратору</p> <br>'
