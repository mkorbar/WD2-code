from datetime import datetime

from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    moj_pozdrav = 'Pozdravljen svet!'
    trenutno_leto = datetime.now().year

    vsi_uporabniki = ['Janez', 'Micka', 'Špelca', 'Alfonzija']

    return render_template('index.html', pozdrav=moj_pozdrav, leto=trenutno_leto, uporabniki=vsi_uporabniki)


@app.route('/about', methods=['GET'])
def fakebook():
    return render_template('fakebook.html', data={'name': 'Matej Korbar'})


@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    if request.method == 'POST':

        name = request.form.get('commentator-name')
        email = request.form.get('commentator-email')
        content = request.form.get('comment-content')

        print(name)
        print(email)
        print(content)

        response = make_response(render_template('success.html'))
        response.set_cookie('user_name', name)

        return response
    else:
        name = request.cookies.get('user_name')

        return render_template('porfolio.html', uname=name)


# @app.route('/comment', methods=['POST'])
# def getData():
#     print(request.form)
#     name = request.form.get('commentator-name')
#     email = request.form.get('commentator-email')
#     content = request.form.get('comment-content')
#
#     print(name)
#     print(email)
#     print(content)
#
#     return render_template('success.html')


if __name__ == '__main__':
    app.run()
