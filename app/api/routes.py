from flask import Blueprint, request, jsonify, render_template
from models import db, MaintenanceTasks, task_schema, tasks_schema
from sqlalchemy import or_

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
    Frequency = request.json['Frequency']

    task = MaintenanceTasks(TaskName, HouseType, MaintenanceType, EstContractorCost, EstDIYCost, CostDiff, DIYVideoLink, TaskImageURL, TaskLevel, Frequency)

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
    task.Frequency = request.json['Frequency']

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

    return jsonify({'message': 'Data received and inserted successfully'}), 200

@api.route('/list', methods=['POST'])
def get_task_list():
    data = request.json
    house_type = data.get('homeType')
    washer = data.get('washer')
    dryer = data.get('dryer')
    dishwasher = data.get('dishwasher')
    carpet = data.get('carpet')
    yard = data.get('yard')
    garbage_disposal = data.get('disposal')

    query = MaintenanceTasks.query.filter(MaintenanceTasks.HouseType.like(f'%{house_type}%'))

    filter_conditions = []

    if washer:
        filter_conditions.append(MaintenanceTasks.TaskName.like('%Washing%'))
    if dryer:
        filter_conditions.append(MaintenanceTasks.TaskName.like('%Dryer%'))
    if dishwasher:
        filter_conditions.append(MaintenanceTasks.TaskName.like('%Dishwasher%'))
    if carpet:
        filter_conditions.append(MaintenanceTasks.TaskName.like('%Carpet%'))
    if yard:
        filter_conditions.append(MaintenanceTasks.TaskName.like('%Lawn%'))
    if garbage_disposal:
        filter_conditions.append(MaintenanceTasks.TaskName.like('%Garbage%'))

    if filter_conditions:
        query = query.filter(or_(*filter_conditions))

    # Query to get tasks associated with the house type and true boolean values
    tasks_with_bools = query.all()

    # Query to get unassociated tasks that match the house type
    unassociated_tasks = MaintenanceTasks.query.filter(
        MaintenanceTasks.HouseType.like(f'%{house_type}%'),
        ~MaintenanceTasks.TaskName.like('%Washing%'),
        ~MaintenanceTasks.TaskName.like('%Dryer%'),
        ~MaintenanceTasks.TaskName.like('%Dishwasher%'),
        ~MaintenanceTasks.TaskName.like('%Carpet%'),
        ~MaintenanceTasks.TaskName.like('%Lawn%'),
        ~MaintenanceTasks.TaskName.like('%Garbage%')
    ).all()

    # Combine the results of both queries while removing duplicates
    unique_tasks = set(tasks_with_bools + unassociated_tasks)

    response = tasks_schema.dump(unique_tasks)
    return jsonify(response)