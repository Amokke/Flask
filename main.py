from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)
