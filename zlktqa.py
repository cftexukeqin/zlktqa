from flask import Flask,render_template,redirect,g,request,url_for,session
import config
from models import User,Question
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    content = {
        "questions": Question.query.all()
    }
    return render_template('index.html',**content)
@app.route('/login/',methods=['GeT','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone==telephone,User.password==password).first()
        if user:
            session['user_id'] = user.id
            print(user.id)
            return redirect(url_for('index'))
        else:
            return '手机号或者密码错误，请核对后重新输入！'
@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.telephone == 'telephone').first()
        if user:
            return '该手机号已被注册，请重新输入！'
        if password1 != password2:
            return '两次输入的密码不一致，请核对后重新输入！'
        else:
            user = User(telephone=telephone,username=username,password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    #session.pop('user_id')
    #del session['user_id']
    session.clear()
    return redirect(url_for('index'))

@app.context_processor
def  my_context_processor():
    user_id = session.get('user_id')
    if  user_id:
        user = User.query.filter(User.id==user_id).first()
        return {'user':user}
    else:
        return {}
@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == "GET":
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title = title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
