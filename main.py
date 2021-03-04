from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def fakebook():
    return render_template('fakebook.html', data={'name': 'Matej Korbar'})


@app.route('/portfolio')
def portfolio():
    return render_template('porfolio.html')


if __name__ == '__main__':
    app.run()
