from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'8tyMwiCQ-81EdKVtcRMqVKxtAlXgqQkZT0kDvVYG-gk'


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        mail = session['mail']
        return render_template('index.html', username=username, mail=mail)
    else:
        return redirect(url_for('login'))


@app.route('/cloth/')
def cloth():
    _cloth = [
        {
            "name": "Шапка-ушанка",
            "price": '4500 Р',
            "description": ' Зимняя меховая, суконная или комбинированная шапка (первоначально — мужская), широко распространённый головной убор в России.',
        },
        {
            "name": "Шляпа",
            "price": '2500 Р',
            "description": 'головной убор, состоящий из двух частей ',
        },
    ]
    return render_template('cloth.html', content=_cloth)


@app.route('/shoes/')
def shoes():
    _shoes = [
        {
            "name": "Туфли",
            "price": '3500 Р',
            "description": 'Туфли — это классическая обувь, чаще всего созданная для дополнения официального внешнего вида. ',
        },
        {
            "name": "Босоножки",
            "price": '2500 Р',
            "description": 'Классическая открытая обувь с каблуком или платформой, которую носят преимущественно в тёплое время года либо в помещении. ',
        },
    ]
    return render_template('shoes.html', content=_shoes)


@app.route('/jacket/')
def jacket():
    _jacket = [
        {
            "name": "Жакет",
            "price": '3500 Р',
            "description": 'Разновидность короткой верхней (в основном — женской) одежды из трикотажа или шерстяной ткани. ',
        },
        {
            "name": "Косуха",
            "price": '2500 Р',
            "description": 'Короткая кожаная куртка с зауженной талией и молнией наискосок ',
        },
    ]
    return render_template('jacket.html', content=_jacket)


@app.get('/login/')
def checker_get():
    return render_template('login.html')


@app.post('/login/')
def login():
    if request.method == 'POST':
        if not request.form['username']:
            flash('Ошибка, не введено имя!', 'danger')
            return redirect(url_for('login'))
        if not request.form['mail']:
            flash('Ошибка, не введена почта!', 'danger')
            return redirect(url_for('login'))
        session['username'] = escape(request.form.get('username'))
        session['mail'] = escape(request.form.get('mail'))
        response = make_response(render_template('index.html', username=session['username'], mail=session['mail']))
        response.set_cookie('username', session['username'])
        response.set_cookie('mail', session['mail'])
        return response


@app.route('/logout/')
def logout():
    session.pop('username', None)
    session.pop('mail', None)
    print(f'(Exit) username: {request.cookies.get("username")}')
    print(f'mail: {request.cookies.get("mail")}')
    response = make_response(render_template('login.html'))
    response.delete_cookie("username")
    response.delete_cookie("mail")
    return response


if __name__ == '__main__':
    app.run(debug=True)
