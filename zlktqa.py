#encoding utf8
from flask import Flask,render_template,redirect,g,request,url_for,session
import config
from models import User,Question,Answer
from exts import db
from decorators import login_required
from sqlalchemy import or_
from hashlib import md5


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
        user = User.query.filter(User.telephone==telephone).first()
        if user and user.verify_password(password):
            session['user_id'] = user.id
            # print(user.id)
            return redirect(url_for('index'))
        else:
            return 'telephone or password Error'
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
            return 'Registed! Try Again'
        if password1 != password2:
            return 'Confirm your password'
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


@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == "GET":
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title = title,content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_detail = Question.query.filter(Question.id == question_id).first()
    question_comments = question_detail.answers
    return render_template("detail.html",question_detail = question_detail)


@app.route('/cmt/',methods=['POST'])
@login_required
def comment():
    comment_content = request.form.get('comment')
    question_id = request.form.get('question_id')

    answer = Answer(content=comment_content)
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    # g.answers = question.answers
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/search/')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.content.contains(q),Question.title.contains(q))).order_by('-creat_time')
    return render_template('index.html',questions = questions)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter(User.username == username).first()
    return render_template('user.html',user = user)

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user

@app.context_processor
def  my_context_processor():
    user_id = session.get('user_id')
    if  user_id:
        user = User.query.filter(User.id==user_id).first()
        return {'user':user}
    else:
        return {}

if __name__ == '__main__':
    app.run(port=8000)
