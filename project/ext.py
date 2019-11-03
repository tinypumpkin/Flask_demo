import os,uuid
from wtforms import Form,FileField,StringField,SubmitField
from wtforms.validators import InputRequired
# from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired,FileAllowed
from flask import Flask, request, render_template ,flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from werkzeug.datastructures import CombinedMultiDict

base=os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base,'static/upload')



class Uploadimg(Form):
    avatar = FileField(validators=[FileRequired(),       #FileRequired必须上传
                                   FileAllowed(['jpg','png','gif'],'只能为图片')     #FileAllowed:必须为指定的格式的文件
                                   ])
    # text = StringField(validators=[InputRequired()])
    save = SubmitField('posts') # 保存按钮

def get_img(form):
    print(form.avatar.data)
    if form.validate():
        print('已验证')
        print('提交通过')
        print(form.avatar.data.filename)
        filename=get_id()
        form.avatar.data.save(os.path.join(path,filename))
        print(filename)
        return filename
    else:
        return False

def get_id():
    name=str(uuid.uuid4())+'.jpg'
    return name


def _path():
    return path