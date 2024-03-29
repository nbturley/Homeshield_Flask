from flask import Blueprint, request, jsonify, render_template
from models import db, MaintenanceTasks, task_schema, tasks_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/maintenance-tasks', methods = ['POST'])
def  create_task():
    TaskName = request.json['TaskName']
    HouseType = request.json['HouseType']
    MaintenanceType = request.json['MaintenanceType']
    EstContractorCost = request.json['EstContractorCost']
    EstDIYCost = request.json['EstDIYCost']
    CostDiff = request.json['CostDiff']
    DIYVideoLink = request.json['DIYVideoLink']
    TaskImageURL = request.json['TaskImageURL']
    TaskLevel = request.json['TaskLevel']

    task = MaintenanceTasks(TaskName, HouseType, MaintenanceType, EstContractorCost, EstDIYCost, CostDiff, DIYVideoLink, TaskImageURL, TaskLevel)

    db.session.add(task)
    db.session.commit()

    response = task_schema.dump(task)
    return jsonify(response)

@api.route('/maintenance-tasks', methods = ['GET'])
def get_tasks():
    tasks = MaintenanceTasks.query.all()
    response = tasks_schema.dump(tasks)
    return jsonify(response)

@api.route('/maintenance-tasks/<taskId>', methods = ['POST', 'PUT'])
def update_task(taskId):
    task = MaintenanceTasks.query.get(taskId)
    task.TaskName = request.json['TaskName']
    task.HouseType = request.json['HouseType']
    task.MaintenanceType = request.json['MaintenanceType']
    task.EstContractorCost = request.json['EstContractorCost']
    task.EstDIYCost = request.json['EstDIYCost']
    task.CostDiff = request.json['CostDiff']
    task.DIYVideoLink = request.json['DIYVideoLink']
    task.TaskImageURL = request.json['TaskImageURL']
    task.TaskLevel = request.json['TaskLevel']

    db.session.commit()
    response = task_schema.dump(task)
    return jsonify(response)

@api.route('/maintenance-tasks/<taskId>', methods = ['DELETE'])
def delete_task(taskId):
    task = MaintenanceTasks.query.get(taskId)
    db.session.delete(task)
    db.session.commit()
    response = task_schema.dump(task)
    return jsonify(response)

@api.route('/maintenance-tasks/data', methods = ['POST', 'PUT'])
def handle_data():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({'error': 'Data must be a list of JSON objects'}), 400
    
    try:
        for item in data:
            task = MaintenanceTasks(**item)
            db.session.add(task)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

    return jsonify({'message': 'Data reveived and inserted successfully'}), 200
