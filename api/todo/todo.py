import datetime
import json
import os

from flask import Blueprint, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from models import db, Todo
from api.authentication import AuthError, requires_auth


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = './uploads'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def row_to_dict(row):
    out = {}
    for column in Todo.__table__.columns:
        if str(column.type) == 'DATE':
            out[column.name] = str(getattr(row, column.name))
        else:
            out[column.name] = getattr(row, column.name)
    return out


def get_todo(id):
    todo = db.get_or_404(Todo, id)
    return row_to_dict(todo)


def get_todos():
    todos = db.session.execute(db.select(Todo)).scalars().all()
    todos_json = [row_to_dict(row) for row in todos]
    return todos_json


def create_todo(data):
    todo_json = json.loads(data)

    todo = Todo(
        task=todo_json['task'],
        priority=todo_json['priority'],
        due_date=datetime.datetime.strptime(todo_json['due_date'], '%Y-%m-%d').date(),
        completed=todo_json['completed']
    )

    db.session.add(todo)
    db.session.commit()

    return row_to_dict(todo)


def update_todo(data, id):
    todo = db.get_or_404(Todo, id)
    data = json.loads(data)
    for field in data:
        if hasattr(todo, field):
            setattr(todo, field, data[field])

    db.session.add(todo)
    db.session.commit()

    return row_to_dict(todo)


def delete_todo(id):
    todo = db.get_or_404(Todo, id)
    db.session.delete(todo)
    db.session.commit()

    return row_to_dict(todo)



##################################################
#                  controllers                   #
##################################################


todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/', methods=['GET'])
def todos_get():
    return jsonify(get_todos())


@todo_bp.route('/', methods=['POST'])
@requires_auth
def todos_create(current_user=None):
    print(current_user)
    return jsonify(create_todo(data=request.data))


@todo_bp.route('/<id>', methods=['GET'])
def todo_get(id):
    return jsonify(get_todo(id))


@todo_bp.route('/<id>', methods=['PUT'])
def todo_update(id):
    return jsonify(update_todo(data=request.data, id=id))


@todo_bp.route('/<id>', methods=['DELETE'])
def todo_delete(id):
    delete_todo(id)
    res = jsonify(None)
    res.status_code = 204
    return res

@todo_bp.post('/upload')
def upload_file():
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return jsonify({'error': 'No file in request'})
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return jsonify({'error': 'No file was selected'})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(UPLOAD_FOLDER, filename))

            path = url_for('todo.files', filename=filename)
            return jsonify({'message': 'File upload succsessfull','path': path})


@todo_bp.get('/files/<filename>')
def files(filename=None):
    return send_from_directory(UPLOAD_FOLDER, filename)

@todo_bp.errorhandler(404)
def not_found(e):
    response = jsonify({'error': 'not found', 'status_code': 404})
    response.status_code = 404
    return response


@todo_bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response