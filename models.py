#! /usr/bin/python3
from app import db
from datetime import datetime
from flask_security import UserMixin, RoleMixin

# Define models

#USER
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    last_name = db.Column(db.String(150), nullable=False)
    login = db.Column(db.String(120))
    password = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean())
    created = db.Column(db.DateTime, default=datetime.now())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.login

#SW
class SwGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<SwGroup id: {}, name: {}>'.format(self.id, self.name)


class Sw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(150), unique=True)
    community_ro = db.Column(db.String(150))
    community_rw = db.Column(db.String(150))
    model = db.Column(db.String(150))
    description = db.Column(db.String(150))
    status = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now())
    up = db.Column(db.DateTime)
    down = db.Column(db.DateTime)
    group_id = db.Column(db.Integer, db.ForeignKey('sw_group.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Sw id: {}, ip: {}>'.format(self.id, self.ip)

#VLAN
class VlanList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vlan_id = db.Column(db.Integer)
    vlan_type = db.Column(db.String(200))
    vlan_name = db.Column(db.String(200))
    start_ip = db.Column(db.String(200))
    stop_ip = db.Column(db.String(200))
    gateway = db.Column(db.String(200))
    mask = db.Column(db.String(200))
    desc = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<SwInfo id: {}, vlan_name: {}>'.format(self.id, self.vlan_name)

#OLT
class OltModules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(200))

    def __repr__(self):
        return '<OltModules id: {}, module_name: {}>'.format(self.id, self.module_name)



class Olt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(200))
    model = db.Column(db.String(200))
    ip = db.Column(db.String(200))
    place = db.Column(db.String(200))
    uptime = db.Column(db.String(200))
    temp = db.Column(db.String(200))
    cpu = db.Column(db.String(200))
    pon_type = db.Column(db.String(200))
    community_ro = db.Column(db.String(200))
    community_rw = db.Column(db.String(200))
    desc = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.now())
    modules_id = db.Column(db.Integer, db.ForeignKey('olt_modules.id', ondelete='CASCADE'))
    status = db.Column(db.Integer)
    sort_id = db.Column(db.Integer)
    up = db.Column(db.DateTime)
    down = db.Column(db.DateTime)

    def __repr__(self):
        return '<Olt id: {}, model: {}>'.format(self.id, self.model)


class OnuStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    olt_id = db.Column(db.Integer)
    onu_id = db.Column(db.Integer)
    mac_onu = db.Column(db.String(200))
    signal = db.Column(db.String(200))
    uptime = db.Column(db.String(200))
    temp = db.Column(db.String(200))
    onu_log = db.Column(db.String(200))
    desc = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Onu_status id: {}, Olt_id: {}>'.format(self.id, self.Olt_id)

