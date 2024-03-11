from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)
