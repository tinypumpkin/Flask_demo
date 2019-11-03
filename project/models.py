from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_
from werkzeug.security import generate_password_hash, check_password_hash #对密码哈希化 以及验证哈希值
from datetime import datetime
import random
import os

db=SQLAlchemy()

def init_db(app):
    db.init_app(app)


class User(db.Model):
    __tablename__="User"
    username = db.Column(db.String(20),primary_key=True)
    password_hash = db.Column(db.String(128))
    email=db.Column(db.String(128))
    #初始化
    def __init__(self,email,username,password_hash):
        self.email=email
        self.username=username
        self.password_hash=password_hash
    def __repr__(self):
        """非必须, 用于在调试或测试时, 返回一个具有可读性的字符串表示模型."""
        return '<User %r>' % self.username
    def to_json(self):
        return dict(email=self.email,username=self.username,password_hash=self.password_hash)

class Blog(db.Model):
    __tablename__="Blog"
    id=db.Column(db.Integer, primary_key=True)
    texts = db.Column(db.String(2048))
    titles=db.Column(db.String(128))
    category = db.Column(db.String(20))
    click=db.Column(db.Integer)
    like=db.Column(db.Integer)
    time=db.Column(db.DateTime,default=datetime.now())
    user = db.Column(db.String(20))



    #初始化
    def __init__(self,id,texts,titles,category,click,time,user,like):
        self.id=id
        self.texts=texts
        self.titles=titles
        self.category=category
        self.click=click
        self.time=time
        self.user=user
        self.like=like
    def __repr__(self):
        """非必须, 用于在调试或测试时, 返回一个具有可读性的字符串表示模型."""
        return '<Blog %r>' % self.titles
    def to_json(self):
        return dict(id=self.id,texts=self.texts,titles=self.titles,category=self.category,click=self.click,time=self.time,user=self.user,like=self.like)


class Replay(db.Model):
    __tablename__="Replay"
    username = db.Column(db.String(20))
    texts = db.Column(db.String(512))
    time=db.Column(db.DateTime)
    id=db.Column(db.Integer,primary_key=True)
    page_id=db.Column(db.Integer,db.ForeignKey(Blog.id))
    page_title=db.Column(db.String(128))
    like=db.Column(db.Integer)
    
    blog=db.relationship('Blog',backref=db.backref('Replay'))

    #初始化
    def __init__(self,username,texts,time,id,like,page_id,page_title):
        self.username=username
        self.texts=texts
        self.id=id
        self.like=like
        self.time=time
        self.page_id=page_id
        self.page_title=page_title
    def __repr__(self):
        """非必须, 用于在调试或测试时, 返回一个具有可读性的字符串表示模型."""
        return '<Replay %r>' % self.like
    def to_json(self):
        return dict(username=self.username,texts=self.texts,id=self.id,like=self.like,time=self.time,page_id=self.page_id,page_title=self.page_title)


class User_info(db.Model):
    __tablename__="User_info"        
    Info_id=db.Column(db.Integer)
    usr = db.Column(db.String(20),primary_key=True)
    intro=db.Column(db.String(128))
    img_url = db.Column(db.String(50))
    sex=db.Column(db.String(5))

    #初始化
    def __init__(self,Info_id,usr,intro,img_url,sex):
        self.Info_id=Info_id
        self.img_url=img_url
        self.intro=intro
        self.usr=usr
        self.sex=sex
    def __repr__(self):
        """非必须, 用于在调试或测试时, 返回一个具有可读性的字符串表示模型."""
        return '<User_info %r>' % self.usr
    def to_json(self):
        return dict(Info_id=self.Info_id,usr=self.usr,img_url=self.img_url,intro=self.intro,sex=self.sex)


class Like_num(db.Model):
    __tablename__="Like_num"    
    Info_id=db.Column(db.Integer, primary_key=True)
    like_id=db.Column(db.Integer)
    #初始化
    def __init__(self,Info_id,like_id):
        self.Info_id=Info_id
        self.like_id=like_id
    def __repr__(self):
        """非必须, 用于在调试或测试时, 返回一个具有可读性的字符串表示模型."""
        return '<Like %r>' % self.like_id
    def to_json(self):
        return dict(Info_id=self.Info_id,like_id=self.like_id)





#查询用户
def search_user(unknow):
    temp=None
    # rows = db.session.query(User).all()#查找全部
    temp=db.session.query(User.username).filter(User.username==unknow).first()
    # temp=session.query(User).filter(User.name==unknow).all()
    # print(rows)
    if temp != None:
        return True
    if temp == None:
        # temp='你傻呀根本没这号人'
        return False
#验证密码
def valid_psd(name,psd):
    temp=db.session.query(User.password_hash).filter(User.username==name).first()[0]
    check=check_password_hash(temp,psd)
    if check:
        return True
    else:
        return False

#插入用户
def add_U(username,password,email):
    password_hash = generate_password_hash(password)
    persopn = User(username=username,password_hash=password_hash,email=email)
    temp=''
    if search_user(username):
        temp='数据库已有此数据'
    else:
        db.session.add(persopn)
        db.session.commit()
        temp='插入成功'
    print(temp)


#查询帖子
def search_blog(unknow):
    temp=None
    # rows = db.session.query(User).all()#查找全部
    temp=db.session.query(Blog).filter(Blog.id==unknow).first()
        # temp='你傻呀根本没这号人'
    return temp
    
def show_page():
    data=Blog.query.order_by(-Blog.time).all()
    return data

#插入帖子
def add_B(id,texts,titles,category,click,time,user):
    # _id=random.randrange(100,999)
    persopn = Blog(id=id,texts=texts,titles=titles,category=category,click=click,time=time,user=user,like=like)
    temp=''
    if search_blog(id):
        temp='数据库已有此数据'
    else:
        db.session.add(persopn)
        db.session.commit()
        temp='插入成功'
    print(temp)

#获取帖子title
def get_title(id):
    temp=db.session.query(Blog.titles).filter(Blog.id==id).first()[0]
    return temp

#查询回复
def search_replay(unknow):
    temp=None
    # rows = db.session.query(User).all()#查找全部
    temp=db.session.query(Replay.id).filter(Replay.id==unknow).first()
    if temp != None:
        return temp
    if temp == None:
        return temp

#添加回复
def add_R(username,texts,time,id,like,page_id):
    # _id=random.randrange(100,999)
    title=db.session.query(Blog.titles).filter(Blog.id==page_id).first()[0]
    persopn = Replay(username=username,texts=texts,time=time,id=id,like=like,page_id=page_id,page_title=title)
    temp=''
    if search_replay(id):
        temp='数据库已有此数据'
    else:
        db.session.add(persopn)
        db.session.commit()
        temp='插入成功'
    print(temp)


#插入/新建帖子
def add_page(user,text,category,title):
    try:
        if search_user(user):
            id=random.randrange(10000,99999)
            num=0
            like=0
            time=datetime.now()
            page=Blog(id=id,texts=text,category=category,user=user,click=num,time=time,titles=title,like=like)
            db.session.add(page)
            db.session.commit()
            print('success')
            return 'success'
        else:
            return False
    except IOError:
        return False

#插入评论
def add_comment(page_id,user,text,like):
    try:
        id=random.randrange(10000,99999)
        title=get_title(page_id)
        time=datetime.now()
        comment=Replay(id=id,page_id=page_id,username=user,texts=text,time=time,like=like,page_title=title)
        db.session.add(comment)
        db.session.commit()
        print('评论插入成功')
        return True
    except IOError:
        return False

#查看评论
def show_com(id):  #帖子id
    com=db.session.query(Replay).order_by(Replay.time.desc()).filter(Replay.page_id==id).all()
    return com

#删除评论
def del_com(id):
    if id!=None:
        com=db.session.query(Replay).filter(Replay.id==id).first()
        db.session.delete(com)
        db.session.commit()
    else:
        return 'id为空'

#更改click的值
def click_add(id,num):
    page=db.session.query(Blog).filter(Blog.id==id).all()
    page.click=num
    db.session.commit()
    return db.session.query(Blog.id).filter(Blog.id==id).all()[0]


#查找关键字
def search_key(q):
    return db.session.query(Blog).filter(or_(Blog.titles.contains(q),Blog.texts.contains(q)))

#查询类别
def search_cat(cat):
    return db.session.query(Blog).filter(Blog.category==cat).all()

#查询用户发布的所有帖子(帖子)
def user_blog(usr):
    print(usr)
    return db.session.query(Blog).filter(Blog.user==usr).all()

#查询用户发布帖子(回复))
def _usr_blog(usr):
    print(usr)
    return db.session.query(Replay).order_by(Replay.time.desc()).filter(Replay.username==usr).all()

#个人信息设置
def person_setting(usr,intro,url,sex):
    temp=db.session.query(User_info.Info_id).filter(User_info.usr==usr).first()
    if temp:
        id=temp[0]
        print(id)
        info=db.session.query(User_info).filter(User_info.Info_id==id).first()
        info.sex=sex
        info.intro=intro
        try:
            base=os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base,'static/upload')
            path=os.path.join(path,info.img_url)
            if os.path.exists(path) and info.img_url!=url:
                os.remove(path)
            else:
                pass
        except IOError:
            return "文件未找到"
        info.img_url=url    #应先删除文件再做更改
        db.session.commit()
        return id
    else:
        id=random.randrange(10000,99999)
        info = User_info(Info_id=id,usr=usr,img_url=url,sex=sex,intro=intro)
        db.session.add(info)
        db.session.commit()
        return id

#个人简介及性别
def get_person(usr):
    return db.session.query(User_info).filter(User_info.usr==usr).first()
#查询url
def get_url(usr):
    url=db.session.query(User_info.img_url).filter(User_info.usr==usr).first()
    if url:
        return url[0]
    else:
        return False
    
def look_like(usr,id):
    try:
        inid=db.session.query(User_info.Info_id).filter(User_info.usr==usr).first()[0]
        like=db.session.query(Like_num).filter(and_(Like_num.Info_id==inid,Like_num.like_id==id)).first()
        # print(usr,id)
        # print(inid,like)
        if like:
            return True
        else:
            return False
    except TypeError:
        return False

#增加赞
def add_like(id):
    page=db.session.query(Blog).filter(Blog.id==id).first()
    com=db.session.query(Replay).filter(Replay.id==id).first()
    if page:
        # print('我是赞:',page.like,'我是他的类型:',type(page.like))
        likes=page.like+1
        page.like=likes
        db.session.commit()
    elif com:
        likes=com.like+1
        com.like=likes
        db.session.commit()
    else:
        return False

#取消赞
def pop_like(id):
    page=db.session.query(Blog).filter(Blog.id==id).first()
    com=db.session.query(Replay).filter(Replay.id==id).first()
    if page:
        if page.like>=1:
            likes=page.like-1
            page.like=likes
            db.session.commit()
        else:
            return False
    elif com:
        if com.like>=1:
            likes=com.like-1
            com.like=likes
            db.session.commit()
        else:
            return False
    else:
        return False

#向赞列表增加元素
def add_like_to(usr,id):
    inid=db.session.query(User_info.Info_id).filter(User_info.usr==usr).first()
    inid=inid[0]
    id=int(id)
    like=db.session.query(Like_num).filter(and_(Like_num.Info_id==inid,Like_num.like_id==id)).first()
    print('我是新增数据',inid,like,id)
    # print('类别',type(inid),type(id))
    if like:
        print('已经点赞')
        return False 
    else:
        print('增加前最后',inid,id,type(inid),type(id))
        link=Like_num(Info_id=inid,like_id=id)
        db.session.add(link)
        db.session.commit()

#从赞列表删除元素
def del_like_to(usr,id):
    inid=db.session.query(User_info.Info_id).filter(User_info.usr==usr).first()
    inid=inid[0]
    id=int(id)
    print(inid,id)
    like=db.session.query(Like_num).filter(and_(Like_num.Info_id==inid,Like_num.like_id==id)).first()
    if like:
        del_list=like
        db.session.delete(del_list)
        db.session.commit()
    else:
        print('未找到数据')
        return False

#赞的总数
def numberof_like(usr):
    try:
        rep=db.session.query(Replay.like).filter(Replay.username==usr).first()[0]
        com=db.session.query(Blog.like).filter(Blog.user==usr).first()[0]
        return int(rep)+int(com)
    except TypeError:
        return 0
#查询赞
def like_search(id):
    rep=db.session.query(Replay.like).filter(Replay.id==id).first()[0]
    com=db.session.query(Blog.like).filter(Blog.id==id).first()[0]
    if rep:
        return rep
    elif com:
        return com
    else:
        return False

#清空数据库
def clear_db(name):
    temp=Blog.query.filter(Blog.user==name).first()
    db.session.delete(temp)
    db.session.commit()


