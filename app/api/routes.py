from flask import Blueprint, request, jsonify, render_template

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/maintenance-tasks', methods = ['POST'])
def  create_task():
    TaskName = request.json['TaskName']