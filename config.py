# coding:utf-8

import os

DEBUG = True

SECRET_KEY = os.urandom(24)

# 数据库类型
DIALCT = "mysql"
# 数据库驱动
DRIVER = "pymysql"
# 数据库用户名
USERNAME = "root"
# 数据库密码
PASSWORD = "root"
# 服务器IP地址
HOST = "127.0.0.1"
# 端口号，默认3306
PORT = "3306"
# 数据库名
DATABASE = "shop"
# 将数据库信息格式化成一个固定的字符串，赋予给DB_URI(注意是DB_URI 而不是DB_URL，这是很多新手容易遇到的坑！！)
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALCT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

