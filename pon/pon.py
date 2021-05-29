#! /usr/bin/python3
import os
import sys

sys.path.insert(0, './modules')
from bdcom.BDCOM3310D import BD_COM_Base
from cdata.FD1204S import C_DATA_Base_1204S
from cdata.FD1208S import C_DATA_Base_FD1208S
from app import *
from flask import Blueprint, render_template, request, url_for, send_from_directory, redirect, flash, jsonify
from flask import session, send_from_directory
# from keystoneclient.session import Session
from models import OltModules, Olt, OnuStatus
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

# from sqlalchemy import asc, desc
# from flask_security import login_required

ponApp = Blueprint('ponApp', __name__, static_folder='static', template_folder='templates')

ALLOWED_EXTENSIONS = set(['ico','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# PON ADD
@ponApp.route("/add/", methods=['POST', 'GET'])
def pon_add():
    modules = OltModules.query.all()
    device = Olt.query.all()
    return render_template('olt_add.html', modules=modules, device=device)

@ponApp.route("/add/save", methods=['POST', 'GET'])
def pon_add_save():
    ip = request.form.get('ip')
    model = request.form.get('model')
    community_ro = request.form.get('community_ro')
    community_rw = request.form.get('community_rw')
    desc = request.form.get('desc')
    modules_id = request.form.get('modules_id')
    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        o = Olt(modules_id=modules_id, ip=ip, model=model,
                community_ro=community_ro, community_rw=community_rw,  desc=desc, img=filename)
        db.session.add(o)
        db.session.commit()
    else:
        modules_id = request.form.get('modules_id')
        ip = request.form.get('ip')
        model = request.form.get('model')
        community_ro = request.form.get('community_ro')
        community_rw = request.form.get('community_rw')
        desc = request.form.get('desc')
        o = Olt(modules_id=modules_id, ip=ip, model=model,
                community_ro=community_ro, community_rw=community_rw, desc=desc)
        db.session.add(o)
        db.session.commit()

    return redirect(url_for('ponApp.pon_add'))

@ponApp.route("/add/delete=<int:id>")
def pon_add_delete(id):
    Olt.query.filter(Olt.id == id).delete()
    db.session.commit()
    return redirect(url_for('ponApp.pon_add'))

# PON
@ponApp.route("/main/", methods=['POST', 'GET'])
def pon():
    olt = Olt.query.order_by(Olt.sort_id.asc()).all()
    return render_template('pon.html', olt=olt)


@ponApp.route("/olt/detail/")
def olt_detail():
    return render_template('olt_detail.html')


@ponApp.route("/onu/detail/")
def onu_detail():
    return render_template('onu_detail.html')


# API_OLT
@ponApp.route("/api/olt/base", methods=['POST', 'GET'])
def base_info():
    ip = request.args.get('ip')
    res = db.session.query(Olt.ip, Olt.modules_id, Olt.community_ro, Olt.desc, OltModules.module_name) \
        .outerjoin(OltModules, Olt.modules_id == OltModules.id).filter(Olt.ip == ip).first()
    community = res.community_ro
    olt = Olt.query.filter(Olt.ip == ip).first()
    if res.module_name == 'C-DATA: FD1204SN':
        try:
            r = C_DATA_Base_1204S().base_info(ip, community)
            print(r['r_uptime'])
            olt.uptime = str(r['r_uptime'])
            db.session.commit()
            res_base = [{'desc': res.desc + ' ' + ip}, {'uptime': str(r['r_uptime'])}]
            return jsonify({'data': res_base})
        except:
            pass
    if res.module_name == 'C-DATA: FD1208SN':
        try:
            r = C_DATA_Base_FD1208S().base_info(ip, community)
            olt.uptime = str(r['r_uptime'])
            db.session.commit()
            res_base = [{'desc': res.desc + ' ' + ip}, {'uptime': str(r['r_uptime'])}]
            return jsonify({'data': res_base})
        except:
            pass
    if res.module_name == 'BDCOM: P3310C':
        try:
            r = BD_COM_Base().base_info(ip, community)
            olt.uptime = str(r['r_uptime'])
            olt.uptime = str(r['r_uptime'])
            olt.temp = str(r['r_temp'])
            olt.cpu = str(r['r_cpu'])
            db.session.commit()
            res_base = [{'desc': res.desc + ' ' + ip}, {'uptime': 'uptime ' + r['r_uptime']},
                        {'temp': 'temp ' + r['r_temp'] + ' ℃'},
                        {'cpu': 'cpu ' + r['r_cpu'] + '%'}]
            return jsonify({'data': res_base})
        except:
            pass


# API_OLT
@ponApp.route("/api/olt/onu/count", methods=['POST', 'GET'])
def onu_count():
    ip = request.args.get('ip')
    res = db.session.query(Olt.ip, Olt.modules_id, Olt.community_ro, OltModules.module_name) \
        .outerjoin(OltModules, Olt.modules_id == OltModules.id).filter(Olt.ip == ip).first()
    community = res.community_ro
    if res.module_name == 'C-DATA: FD1204SN':
        try:
            res_count = C_DATA_Base_1204S().port_onu_active(ip, community)
            return jsonify({'data': res_count})
        except:
            pass
    if res.module_name == 'C-DATA: FD1208SN':
        try:
            res_count = C_DATA_Base_FD1208S().port_onu_active(ip, community)
            return jsonify({'data': res_count})
        except:
            pass
    if res.module_name == 'BDCOM: P3310C':
        try:
            res_count = BD_COM_Base().port_onu_count(ip, community)
            return jsonify({'data': res_count})
        except:
            pass


# API_OLT
@ponApp.route("/api/olt/all", methods=['POST', 'GET'])
def olt_update():
    ip = request.args.get('ip')
    res = db.session.query(Olt.ip, Olt.modules_id, Olt.community_ro, OltModules.module_name) \
        .outerjoin(OltModules, Olt.modules_id == OltModules.id).filter(Olt.ip == ip).first()
    community = res.community_ro

    if res.module_name == 'C-DATA: FD1204SN':
        try:
            res_count = C_DATA_Base_1204S().port_onu_count(ip, community)
            return jsonify({'data': res_count})
        except:
            pass
    if res.module_name == 'C-DATA: FD1208SN':
        try:
            res_count = C_DATA_Base_FD1208S().port_onu_count(ip, community)
            return jsonify({'data': res_count})
        except:
            pass
    if res.module_name == 'BDCOM: P3310C':
        try:
            res_all = BD_COM_Base().port_info(ip, community)
            return jsonify({'data': res_all})
        except:
            pass


# API_ONU
@ponApp.route("/api/onu/info", methods=['POST', 'GET'])
def onu_info():
    ip = request.args.get('ip')
    OnuId = request.args.get('OnuId')
    res = db.session.query(Olt.ip, Olt.modules_id, Olt.community_ro, OltModules.module_name) \
        .outerjoin(OltModules, Olt.modules_id == OltModules.id).filter(Olt.ip == ip).first()
    community = res.community_ro

    if res.module_name == 'C-DATA: FD1204SN':
        try:
            res_onu = C_DATA_Base_1204S().onu_info(ip, community,  OnuId)
            return jsonify({'data': res_onu})
        except:
            pass
    if res.module_name == 'C-DATA: FD1208SN':
        try:
            res_onu = C_DATA_Base_FD1208S().onu_info(ip, community,  OnuId)
            return jsonify({'data': res_onu})
        except:
            pass
    if res.module_name == 'BDCOM: P3310C':
        try:
            res_onu = BD_COM_Base().onu_info(ip, community, OnuId)
            return jsonify({'data': res_onu})
        except:
            pass


# API_ONU_REBOOT
@ponApp.route("/api/onu/reboot", methods=['POST', 'GET'])
def onu_reboot():
    ip = request.args.get('ip')
    OnuId = request.args.get('OnuId')
    res = db.session.query(Olt.ip, Olt.modules_id, Olt.community_ro,Olt.community_rw, OltModules.module_name) \
        .outerjoin(OltModules, Olt.modules_id == OltModules.id).filter(Olt.ip == ip).first()
    community_rw = res.community_rw

    if res.module_name == 'C-DATA: FD1204SN':
        try:
            res_onu = C_DATA_Base_1204S().onu_reboot(ip, community_rw,  OnuId)
            return jsonify({'data': res_onu})
        except:
            pass
    if res.module_name == 'C-DATA: FD1208SN':
        try:
            res_onu = C_DATA_Base_FD1208S().onu_reboot(ip, community_rw,  OnuId)
            return jsonify({'data': res_onu})
        except:
            pass
    if res.module_name == 'BDCOM: P3310C':
        try:
            res_onu = BD_COM_Base().onu_reboot(ip, community_rw, OnuId)
            return jsonify({'data': res_onu})
        except:
            pass


# API_ONU_DELETE
@ponApp.route("/api/onu/delete", methods=['POST', 'GET'])
def onu_delete():
    ip = request.args.get('ip')
    OnuId = request.args.get('OnuId')
    res = db.session.query(Olt.ip, Olt.modules_id, Olt.community_ro,Olt.community_rw, OltModules.module_name) \
        .outerjoin(OltModules, Olt.modules_id == OltModules.id).filter(Olt.ip == ip).first()
    community_rw = res.community_rw

    if res.module_name == 'C-DATA: FD1204SN':
        try:
            res_onu = C_DATA_Base_1204S().onu_delete(ip, community_rw,  OnuId)
            return jsonify({'data': res_onu})
        except:
            pass
    if res.module_name == 'C-DATA: FD1208SN':
        try:
            res_onu = C_DATA_Base_FD1208S().onu_delete(ip, community_rw,  OnuId)
            return jsonify({'data': res_onu})
        except:
            pass
    if res.module_name == 'BDCOM: P3310C':
        try:
            res_onu = BD_COM_Base().onu_delete(ip, community_rw, OnuId)
            return jsonify({'data': res_onu})
        except:
            pass