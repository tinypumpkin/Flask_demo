from flask import Blueprint ,redirect,render_template,current_app,url_for,request,jsonify,flash,g,session
from emails import get_code,valid_code
from models import search_user,valid_psd,add_U,add_page,clear_db,show_page,search_blog,add_comment,show_com,search_key,search_cat,user_blog,_usr_blog,get_title,person_setting,get_person,del_com,add_like,pop_like,add_like_to,del_like_to,look_like,numberof_like,like_search,get_url
from doctor import valid
from ext import get_id,_path,get_img,Uploadimg
from werkzeug.datastructures import CombinedMultiDict
# from wtforms import Form,FileField,StringField,SubmitField
# from flask_wtf.file import FileRequired,FileAllowed
import os

blue=Blueprint('first_blue',__name__)

def init_blue(app):
    app.register_blueprint(blueprint=blue)

#首页
@blue.route('/',methods=['GET','POST'])
def index():
    # data={'shows':show_page()}
    shows=show_page()
    nums=request.values.get('n')
    url=session.get('url')
    print(url)
    print('卧槽',nums ,url)
    return render_template('root.html',shows=shows,url=url)

@blue.route('/login',methods=['GET','POST'])
def login():
    usr=request.form.get('name_l','')
    psd=request.form.get('psd_l','')
    if search_user(usr):
        if valid_psd(usr,psd):
            session['name']=usr
            session['url']=''
            try:
                url=get_url(usr)
                session['url']=url
            except FileNotFoundError:
                pass
            session.permanent=True
            print('成功登录')
            return redirect(url_for('first_blue.setting'))
        else:
            flash('密码不正确',category='error')
    else:
        print("用户名未注册")
    return render_template('login.html')


@blue.route('/regist/',methods=['GET','POST'])
def regist():
    gcod=request.values.get('gcod','')
    # get_code(gcod)
    # code=valid_code()
    if request.method=='POST':
        usr=request.form.get('usr','')
        psd=request.form.get('psd','')
        email=request.form.get('mail','')
        valid=request.form.get('valid','')
        if search_user(usr)!=True:
            add_U(usr,psd,email)
            return redirect(url_for("first_blue.login"))
        else:
            flash('用户名已存在',category='error')
    return render_template('regist.html')

@blue.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('first_blue.index'))

#发布文章
@blue.route('/article',methods=['GET','POST'])
@valid
def article():
    if request.method=='GET':
        return render_template('article.html')
    if request.method=='POST':
        user=session.get('name')
        title=request.values.get('title')
        text=request.values.get('container')
        cat=request.values.get('cat')
        if cat =='-- 类别 --':
            flash('尚未选择类别，选择类别后提交',category='error')  #后期添加jQuery/jinja2反馈到页面
        else:
            add_page(user,text,cat,title)
            return redirect(url_for('first_blue.index'))  
        # clear_db(user)
        #中间可以添加发布成功的反馈flash
        return redirect(url_for('first_blue.article'))  

#界面显示
@blue.route('/page/<id>',methods=['GET','POST'])
def page(id):
    user=session.get('name')
    big_like='zan'
    if user:
        if look_like(user,id):
            big_like='yizan'
        else:
            pass
    page=search_blog(id)
    like=0
    link=''
    temp=user
    text=request.form.get('comment')
    if request.method=="GET":
        link=request.args.get('ns')
        print(link)
        if link:
            if link=='1':
                add_like(id)
                add_like_to(user,id)
            elif link=='-1':
                pop_like(id)
                del_like_to(user,id)
            return jsonify({'r':'成功'})
        else:
            pass
    if request.method=='POST':
        if user:
            add_comment(id,user,text,like)
        else:
            return redirect(url_for('first_blue.login'))       
    comment=show_com(id)  #这里是评论
    lens=len(comment)
    context={
    'page':page,
    'comment':comment,
    'temp':temp,
    'lens':lens,
    'big_like':big_like,
    'link':link
    }
    return render_template('page_detail.html',**context)


#删除评论
@blue.route('/page/delete/<id>/<id_c>',methods=['GET','POST'])
def delate_com(id,id_c):
    id_c=int(id_c)
    del_com(id_c)
    return redirect(url_for("first_blue.page",id=id))



#搜索提交
@blue.route('/search',methods=['GET'])
def search():
    temp=request.args.get('q')
    ser=search_key(temp)
    print(ser)
    return render_template('base.html',ser=ser)

#类别
@blue.route('/category/<cat>')
def category(cat):
    print(cat)
    cate=search_cat(cat)
    return render_template('base.html',cate=cate)

#个人主页
@blue.route('/person/<usr>')
def person(usr):
    temp=usr
    info=get_person(temp)
    return render_template('person.html',info=info)

#个人主页评论和文章
@blue.route('/person/<usr>/<option>')
def person_detial(usr,option):
    print(usr)
    print(option)
    url=session.get('url')
    temp=usr
    page=''
    replay=''
    num_like=numberof_like(usr)
    info=get_person(temp)
    if option=='p':
        page=user_blog(temp)
    if option=='r':
        replay=_usr_blog(temp)
    num_article=len(user_blog(temp))
    num_comment=len(_usr_blog(temp))
    context={
        'page':page,
        'replay':replay,
        'temp':temp,
        'num_article':num_article,
        'num_comment':num_comment,
        'info':info,
        'num_like':num_like,
        'url':url
    }
    return render_template('person.html',**context)



# class Uploadimg(Form):
#     avatar = FileField(validators=[FileRequired(),       #FileRequired必须上传
#                                    FileAllowed(['jpg','png','gif'],'只能为图片')     #FileAllowed:必须为指定的格式的文件
#                                    ])
#     # text = StringField(validators=[InputRequired()])
#     save = SubmitField('posts') # 保存按钮


#设置主页
@blue.route('/setting',methods=['GET','POST'])
def setting():
    usr=session.get('name')
    url=session.get('url')
    form = Uploadimg(CombinedMultiDict([request.form,request.files]))
    name_i=get_img(form)
    if request.method=='POST':
        if name_i:
            print(name_i)
            flash('添加图片成功',category='success')
            session['url']=name_i
            url=session.get('url')
        else:
            flash('上传格式不正确',category='error')
        sex=request.form.get('sex','保密')
        text=request.form.get('intro')
        person_setting(usr,text,url,sex)
        if sex and text:
            print(sex,text)
            return redirect(url_for('first_blue.index'))
            return jsonify({'r':'成功'})
        else:
            flash('应填写性别及简介',category='error')
        
    return render_template('setting.html',usr=usr,url=url)
 

#评论尝试（可删除）
@blue.route('/<id>',methods=['GET','POST'])
def page_try(id):
    page=search_blog(id)
    user=session.get('name')
    like=0
    likes=''
    link=''
    link_m=''
    # s_like='zan'
    big_like='zan'
    if user:
        if look_like(user,id):
            big_like='yizan'
    else:
        pass
    temp=user
    text=request.form.get('comment')
    if request.method=="GET":
        link=request.args.get('ns')
        # ppg=request.args.get('idp')
        # print(link,ppg)
        print(link)
        if link:
            if link=='1':
                add_like(id)
                add_like_to(user,id)
            else:
                pop_like(id)
                del_like_to(user,id)
            return jsonify({'r':'成功'})
        else:
            pass
    if request.method=="POST":
        add_comment(id,user,text,like)        #这里的ID是模板id是用来标定模板的id的
    
    # if request.method=="GET":
        likes=request.form.get('num')
        link_m=request.form.get('id')
        print(likes,link_m)
        if likes:
            if likes=='1':
                add_like(link_m)
                add_like_to(user,link_m)
            else:
                pop_like(link_m)
                del_like_to(user,link_m)
            return jsonify({'r':'成功'})
        else:
            pass
    comment=show_com(id)
    lens=len(comment)
    # idd=request.args.get('idd')
    # print('卧槽啥情况',idd)
    return render_template('评论尝试.html',page=page,comment=comment,temp=temp,lens=lens,big_like=big_like)



#上下文处理器
@blue.context_processor   #被这个装饰器装饰的函数必须返回一个字典
def my_context_proc():
    name=session.get('name')
    if name:
        return {'name':name}
    return {}








