from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from flask_marshmallow  import Marshmallow

# set variables for class instantiation
db = SQLAlchemy()
ma = Marshmallow()

class MaintenanceTasks(db.Model):
    TaskID = db.Column(db.String, primary_key = True)
    TaskName = db.Column(db.String, nullable = False)
    HouseType = db.Column(db.String, nullable = False)
    MaintenanceType = db.Column(db.String, nullable = False)
    # ContractorID = db.Column(db.Integer, db.ForeignKey('contractor.ContractorID'))
    EstContractorCost = db.Column(db.Integer)
    EstDIYCost = db.Column(db.Integer)
    CostDiff = db.Column(db.Integer)
    DIYVideoLink = db.Column(db.String)
    TaskImageURL = db.Column(db.String)
    TaskLevel = db.Column(db.String)
    Frequency = db.Column(db.String)
    VideoId = db.Column(db.String)

    def __init__(self, TaskName, HouseType, MaintenanceType, EstContractorCost, EstDIYCost, CostDiff, DIYVideoLink, TaskImageURL, TaskLevel, Frequency, VideoId, TaskID=''):
        self.TaskID = self.set_id()
        self.TaskName = TaskName
        self.HouseType = HouseType
        self.MaintenanceType = MaintenanceType
        # self.ContractorID = ContractorID
        self.EstContractorCost = EstContractorCost
        self.EstDIYCost = EstDIYCost
        self.CostDiff = CostDiff
        self.DIYVideoLink = DIYVideoLink
        self.TaskImageURL = TaskImageURL
        self.TaskLevel = TaskLevel
        self.Frequency = Frequency
        self.VideoId = VideoId

    def __repr__(self):
        return f'The following task has been added to the task list: {self.TaskName}'
    
    def set_id(self):
        return str(uuid.uuid4())
    
class TaskSchema(ma.Schema):
    class Meta:
        fields = ['TaskName', 'HouseType', 'MaintenanceType', 'ContractorID', 'EstContractorCost', 'EstDIYCost', 'CostDiff', 'DIYVideoLink', 'TaskImageURL', 'TaskLevel', 'Frequency', 'VideoId', 'TaskID']

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)