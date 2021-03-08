from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    moj_pozdrav = 'Pozdravljen svet!'
    trenutno_leto = datetime.now().year

    vsi_uporabniki = ['Janez', 'Micka', 'Špelca', 'Alfonzija']

    return render_template('index.html', pozdrav=moj_pozdrav, leto=trenutno_leto, uporabniki=vsi_uporabniki)


@app.route('/about')
def fakebook():
    return render_template('fakebook.html', data={'name': 'Matej Korbar'})


@app.route('/portfolio')
def portfolio():
    return render_template('porfolio.html')


if __name__ == '__main__':
    app.run()
