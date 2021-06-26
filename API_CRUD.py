import os
from flask import Flask
from flask_restful import Resource , Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from secure_check import authenticate , identity
# from flask_jwt import JWT,jwt_required


app = Flask(__name__)
app.config['secret_key'] = 'secret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app,db)

api = Api(app)
# jwt = JWT(app,authenticate,identity)

# initially we are using list to store record but its getting stored over memory so once python code stop
# data will be lost. so, hence we implemented DB concept.
# Record = []
################################################################
#              DB model class


class Name(db.Model):

    name = db.Column(db.String(80),primary_key=True)

    def __init__(self,name):

        self.name = name

    def json(self):
        return {'name': self.name}

#################################################################

class NameRecord(Resource):

    def get(self,name):

        # for record in Record:
        #     if record['name'] == name:
        #         return record
        record = Name.query.filter_by(name=name).first()
        if record:
            return record.json()
        else:
            return {'name': None},404

    def post(self,name):

        # record = {'name':name}
        # Record.append(record)
        # return record
        record = Name(name=name)
        db.session.add(record)
        db.session.commit()
        return record.json()

    def delete(self,name):

        # for ind,record in enumerate(Record):
        #     if record['name'] == name:
        #         delete_name = Record.pop(ind)
        #         return {'note': 'delete success'}
        record = Name.query.filter_by(name=name).first()
        db.session.delete(record)
        db.session.commit()
        return {'note': 'delete success'}

class AllNames(Resource):

    # @jwt_required()
    def get(self):
        # return {'Record':Record}
        record = Name.query.all()
        return [val.json() for val in record]

api.add_resource(NameRecord,'/record/<string:name>')
api.add_resource(AllNames,'/Record')

if __name__ == '__main__':
    app.run(debug=True)

#####################################################
'''
Important three cmd for db initialize 
set FLASK_APP = current_file.py or if app.py is present then it FLASK_APP will not create any issue
1. flask db init
2. flask db migrate -m "commit msg"
3. flask db upgrade
'''
#####################################################

# import os
# from flask import Flask
# from flask_restful import Resource , Api
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecretkey'
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
#
# db = SQLAlchemy(app)
# Migrate(app,db)
# api = Api(app)
# # Name = []
# ################################################################
#
# class Name(db.Model):
#
#     name = db.Column(db.String(80),primary_key=True)
#
#     def __init__(self,name):
#         self.name = name
#
#     def json(self):
#         return {'name':self.name}
#
# #################################################################
#
# class Family(Resource):
#
#     def get(self,name):
#
#         # for record in Name:
#         #     if record['name'] == name:
#         #         return record
#         record = Name.query.filter_by(name=name).first()
#         if record:
#             return record.json()
#         else:
#             return {'name':None},404
#
#     def post(self,name):
#
#         # record = {'name': name}
#         # Name.append(record)
#         # return record
#         record = Name(name=name)
#         db.session.add(record)
#         db.session.commit()
#         return record.json()
#
#     def delete(self,name):
#
#         # for ind,record in enumerate(Name):
#         #     if record['name'] == name:
#         #         delete_name = Name.pop(ind)
#         #     return {'note': 'success'}
#         record = Name.query.filter_by(name=name).first()
#         db.session.delete(record)
#         db.session.commit()
#
#         return {'note': 'delete success'}
#
# class AllFamily(Resource):
#
#     def get(self):
#         # return {'Name': Name}
#         record = Name.query.all()
#         return [name.json() for name in record]
#
#
# api.add_resource(Family,'/Family/<string:name>')
# api.add_resource(AllFamily,'/All')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)













