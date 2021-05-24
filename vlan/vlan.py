#! /usr/bin/python3
import os
from app import *
from flask import Blueprint, render_template, request, url_for, send_from_directory, redirect, flash, jsonify
from flask import session
# from keystoneclient.session import Session
from models import VlanList

# from sqlalchemy import asc, desc
# from flask_security import login_required

vlanApp = Blueprint('vlanApp', __name__, static_folder='static', template_folder='templates')


# VLAN_INFO
@vlanApp.route("/list", methods=['POST', 'GET'])
def vlan_list():
    vlans = VlanList.query.all()
    return render_template('vlan_list.html', vlans=vlans)


@vlanApp.route("/vlan/save", methods=['POST', 'GET'])
def vlan_add():
    if request.method == 'POST':
        vlan_id = request.form.get('vlan_id')
        vlan_type = request.form.get('vlan_type')
        vlan_name = request.form.get('vlan_name')
        start_ip = request.form.get('start_ip')
        stop_ip = request.form.get('stop_ip')
        gateway = request.form.get('gateway')
        mask = request.form.get('mask')
        desc = request.form.get('desc')
        v = VlanList(vlan_id=vlan_id, vlan_type=vlan_type, vlan_name=vlan_name,
                     start_ip=start_ip, stop_ip=stop_ip, gateway=gateway, mask=mask, desc=desc)
        db.session.add(v)
        db.session.commit()

    return redirect(url_for('vlanApp.vlan_list'))


@vlanApp.route("/vlan/delete=<int:id>", methods=['POST', 'GET'])
def vlan_delete(id):
    v = VlanList.query.filter(VlanList.id == id).delete()
    db.session.commit()
    return redirect(url_for('vlanApp.vlan_list'))
