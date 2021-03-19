import random
from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, db

app = Flask(__name__)
db.create_all()

MAX_SECRET = 30


def get_user(user_email=None):
    if not user_email:
        user_email = request.cookies.get('email')
    return db.query(User).filter_by(email=user_email).first()


@app.route('/', methods=['GET'])
def index():
    user = get_user()
    return render_template('index.html', user=user, max_secret=MAX_SECRET)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        response = render_template('login.html')
    else:
        name = request.form.get('user-name')
        email = request.form.get('user-email')

        user = get_user(user_email=email)
        if not user:
            secret = random.randint(1, MAX_SECRET)
            user = User(name=name, email=email, secret_number=secret)
            db.add(user)
            db.commit()

        response = make_response(redirect(url_for('index')))
        response.set_cookie('email', user.email)

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    user = get_user()
    if not user:
        return redirect(url_for('login'))

    if guess == user.secret_number:
        message = "Pravilno! Skrito število je {0}".format(str(user.secret_number))
        response = make_response(render_template("result.html", message=message))
        user.secret_number = random.randint(1, MAX_SECRET)
        db.add(user)
        db.commit()
        return response
    elif guess > user.secret_number:
        message = "Ta poizkus ni pravilen. Poizkusi z manjšo številko."
        return render_template("result.html", message=message)
    elif guess < user.secret_number:
        message = "Ta poizkus ni pravilen. Poizkusi z večjo številko."
        return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run()
