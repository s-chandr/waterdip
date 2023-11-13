from flask import Flask, jsonify, request, abort
from pymongo import MongoClient
import os
app = Flask(__name__)

# Connect to MongoDB
app.config["MONGO_URI"] =  "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/"
mongo_client = MongoClient(app.config["MONGO_URI"])
db = mongo_client['task_manager']
tasks_collection = db['tasks']


def get_task_by_id(task_id):
    return tasks_collection.find_one({'id': task_id}, {'_id': 0})


def generate_task_id():
    if tasks_collection.count_documents({}):
        return tasks_collection.find().sort('id', -1).limit(1)[0]['id'] + 1
    else:
        return 1


@app.route('/v1/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)  # Bad Request

    new_task = {
        'id': generate_task_id(),
        'title': request.json['title'],
        'is_completed': False
    }

    tasks_collection.insert_one(new_task)
    return jsonify({'id': new_task['id']}), 201  # Created


@app.route('/v1/tasks', methods=['GET'])
def list_tasks():
    tasks = list(tasks_collection.find({}, {'_id': 0}))
    return jsonify({'tasks': tasks}), 200  # OK


@app.route('/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = get_task_by_id(task_id)
    if task:
        return jsonify(task), 200  # OK
    else:
        return jsonify({'error': 'There is no task at that id'}), 404  # Not Found


@app.route('/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = tasks_collection.delete_one({'id': task_id})
    if result.deleted_count > 0:
        return '', 204  # No Content
        # return jsonify({'Success': 'Task Deleted'}), 204  # Testing Postman
    else:
        return jsonify({'error': 'There is no task at that id'}), 404  # Not Found


@app.route('/v1/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    task = get_task_by_id(task_id)
    if task:
        if 'title' in request.json:
            task['title'] = request.json['title']
        if 'is_completed' in request.json:
            task['is_completed'] = request.json['is_completed']

        tasks_collection.replace_one({'id': task_id}, task)
        return '', 204  # No Content
        # return jsonify({'Success': 'Task Updated'}), 204  # Testing Postman
    else:
        return jsonify({'error': 'There is no task at that id'}), 404  # Not Found


# Extra Credit: Bulk add tasks
@app.route('/v1/tasks/bulk', methods=['POST'])
def bulk_add_tasks():
    if not request.json or 'tasks' not in request.json:
        abort(400)  # Bad Request

    new_task_ids = []
    for task_data in request.json['tasks']:
        new_task = {
            'id': generate_task_id(),
            'title': task_data['title'],
            'is_completed': task_data.get('is_completed', False)
        }
        tasks_collection.insert_one(new_task)
        new_task_ids.append({'id': new_task['id']})

    return jsonify({'tasks': new_task_ids}), 201  # Created


# Extra Credit: Bulk delete tasks
@app.route('/v1/tasks/bulk', methods=['DELETE'])
def bulk_delete_tasks():
    if not request.json or 'tasks' not in request.json:
        abort(400)  # Bad Request

    for task_data in request.json['tasks']:
        result = tasks_collection.delete_one({'id': task_data['id']})
        if result.deleted_count == 0:
            return jsonify({'error': f'Task with id {task_data["id"]} not found'}), 404  # Not Found

    return '', 204  # No Content


if __name__ == '__main__':
    app.run(debug=True)
