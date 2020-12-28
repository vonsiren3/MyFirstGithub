# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Good, Comment, Buycar
from exts import db
from decorators import login_required
from sqlalchemy import or_



app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)



@app.route('/')
def index():
    context = {
        'goods': Good.query.order_by('create_time').all()
    }
    return render_template('index.html', **context)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号或密码错误！'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码！'
        else:
            if password1 != password2:
                return u'两次密码不相等！'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))


@app.route('/shelf/', methods=['GET', 'POST'])
@login_required
def shelf():
    if request.method == 'GET':
        return render_template('shelf.html')
    else:
        title = request.form.get('title')
        price = request.form.get('price')
        content = request.form.get('content')

        good = Good(title=title, price=price, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        good.author = user

        db.session.add(good)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<good_id>/')
def detail(good_id):
    good_model = Good.query.filter(Good.id == good_id).first()
    return render_template('detail.html', good=good_model)

@app.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('comment_content')
    good_id = request.form.get('good_id')

    comment = Comment(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    good = Good.query.filter(Good.id == good_id).first()
    comment.good = good
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', good_id=good_id))

@app.route('/search/')
def search():
    q = request.args.get('q')
    goods = Good.query.filter(or_(Good.title.contains(q), Good.content.contains(q)))
    context = {
        'goods': goods
    }
    return render_template('index.html', **context)

@app.route('/car/', methods=['GET', 'POST'])
@login_required
def car():
    if request.method == 'GET':
        return render_template('car.html')
    else:
        title = request.form.get('title2')
        price = request.form.get('price2')
        good_id = request.form.get('good_id2')
        author_id = session.get('user_id')

        judge = Buycar.query.filter(Buycar.good_id == good_id).first()
        if judge:

            return u'该商品已添加至购物车，不能重复添加！'
        else:
            buycar = Buycar(title=title, price=price, good_id=good_id, author_id=author_id)

            author = User.query.filter(User.id == author_id).first()
            buycar.author = author

            db.session.add(buycar)
            db.session.commit()

            return redirect(url_for('detail', good_id=good_id))

@app.route('/buy/', methods=['GET','POST'])
@login_required
def buy():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()

    car_id = Buycar.query.filter(Buycar.author_id == user_id).all()
    # car1 = Buycar(author_id=user_id)

    cars = []
    for car in car_id:
        car = Good.query.filter(Good.id == car.good_id).first()
        good = Buycar.query.filter(Buycar.good_id == car.id).first()

        cars.append(car.title)

    return render_template('car.html', user=user, cars=cars, good=good, car_id=car_id)

@app.route('/record/', methods=['GET','POST'])
@login_required
def record():
    pass

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}



if __name__ == '__main__':
    app.run()
