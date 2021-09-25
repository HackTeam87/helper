#! /usr/bin/python3
#Import Modules
import os
import sys
from datetime import datetime
from app import app
from sqlalchemy.sql import select
from app import db
from models import Role, User, SwGroup, Sw
from app import user_datastore
from flask import render_template, Response, request, flash, session, url_for, redirect, make_response, jsonify
from flask_security import login_required


# Switch All
@app.route('/sw/list', methods=['POST', 'GET'])
def index():
    group = SwGroup.query.all()
    sw = Sw.query.all()
    return render_template('index.html', group=group, sw=sw)


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
