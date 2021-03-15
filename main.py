from datetime import datetime
import random

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


@app.route("/game", methods=["GET"])
def game():
    secret_number = request.cookies.get("secret_number")  # check if there is already a cookie named secret_number

    response = make_response(render_template("game.html"))
    if not secret_number:  # if not, create a new cookie
        new_secret = random.randint(1, 30)
        response.set_cookie("secret_number", str(new_secret))

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    secret_number = int(request.cookies.get("secret_number"))

    if guess == secret_number:
        message = "Correct! The secret number is {0}".format(str(secret_number))
        response = make_response(render_template("result.html", message=message))
        response.set_cookie("secret_number", str(random.randint(1, 30)))  # set the new secret number
        return response
    elif guess > secret_number:
        message = "Your guess is not correct... try something smaller."
        return render_template("result.html", message=message)
    elif guess < secret_number:
        message = "Your guess is not correct... try something bigger."
        return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run()
