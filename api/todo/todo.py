import datetime, json
from flask import Blueprint, request, jsonify, app
from models import db, Todo


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

    return jsonify(row_to_dict(todo))


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


todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/', methods=['GET', 'POST'])
def todo_all():
    if request.method == 'GET':
        return jsonify(get_todos())
    if request.method == 'POST':
        return jsonify(create_todo(data=request.data))


@todo_bp.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def todo(id):
    if request.method == 'GET':
        return jsonify(get_todo(id))
    if request.method == 'PUT':
        return jsonify(update_todo(data=request.data, id=id))
    if request.method == 'DELETE':
        delete_todo(id)
        res = jsonify(None)
        res.status_code = 204
        return res


@todo_bp.errorhandler(404)
def not_found(e):
    response = jsonify({'error': 'not found', 'status_code': 404})
    response.status_code = 404
    return response
