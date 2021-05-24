#! /usr/bin/python3
class Configuration(object):
    DEBUG = True
    UPLOAD_FOLDER = '/www/static/img/olt'
    #    MYSQL_DATABASE_CHARSET = 'utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://grin:grin1306!@localhost/switcher'
    SECRET_KEY = '12345'
    # WTF_CSRF_ENABLED = False

    ### Flask-security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha256_crypt'
    ### Pagination
