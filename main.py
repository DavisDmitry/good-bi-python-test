from flask import Flask, render_template

from services import on_startup, get_all_passenger, get_top_10_passengers


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', passengers=get_top_10_passengers())


@app.route('/data.json')
def data():
    return {'data': get_all_passenger()}


if __name__ == '__main__':
    on_startup()
    app.run(debug=True)
