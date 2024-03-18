from models import db, User
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm
import hashlib
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
app.config['SECRET_KEY'] = b'23987e90fb5a36d2731709682c980a071eb6e3b4bb6cbcd9767cd32380e9c7db840592ebbff3fa2cc3baddd0'
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return redirect(url_for('register'))


@app.cli.command("init-db")
def init_db():

    db.create_all()
    print('Ok')


@app.route('/register/', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if request.method == 'POST' and form.validate():

        name = form.username.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        print(name, surname, email, password)
        salt = os.urandom(32)
        password_protection = password
        key = hashlib.pbkdf2_hmac('sha256', password_protection.encode('utf-8'), salt, 100000, dklen=128)
        user = User(username=name, surname=surname, email=email, password=key)
        print(user)
        db.session.add(user)
        db.session.commit()
        return f'<h2>Пользователь : {name} добавлен в базу !</h2>'
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)