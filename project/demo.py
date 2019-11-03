from flask import Flask
from vives import init_blue
from models import init_db,User,Blog,Replay
from flask_script import Manager, Shell
from flask_mail import Mail, Message
from threading import Thread
import os,random
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456' 

#数据库配置
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:myself@localhost:3306/job"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JSON_AS_ASCII'] = False

db=SQLAlchemy(app)

init_blue(app)
init_db(app)



# db.create_all()



if __name__ == '__main__':
    app.run(debug=True)