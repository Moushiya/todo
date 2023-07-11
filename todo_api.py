from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []
    return tasks


def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)


@app.route('/tasks', methods=['POST'])
def add_task():
    if not request.is_json:
        return jsonify({'error': 'Invalid JSON data'}), 400

    try:
        new_task = request.json['task']
    except KeyError:
        return jsonify({'error': 'Invalid JSON format or missing "task" field'}), 400

    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify({'message': 'Task added successfully'})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    if task_id >= 0 and task_id < len(tasks):
        deleted_task = tasks.pop(task_id)
        save_tasks(tasks)
        return jsonify({'message': f"Task '{deleted_task}' deleted successfully"})
    else:
        return jsonify({'error': 'Invalid task ID'}), 400

if __name__ == '__main__':
    app.run(debug=True)
