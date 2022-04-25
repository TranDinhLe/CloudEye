from dataclasses import field
from datetime import datetime
from email.quoprimime import body_check
from turtle import title
from unittest import result
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from test import test as tmtest
from train import fulltrain as tmtrain
from post import sendOpenSignal as Open
from post import sendNotOpenSignal as NotOpen

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/cloudeye'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100))
    body=db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.now)

    def __init__(self, title, body):
        self.title = title
        self.body = body


class infoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')

info_schema = infoSchema()
infos_schema = infoSchema(many=True)

@app.route('/', methods = ['GET'])
def get_default():
    #return jsonify({"hello": "world"})
    all_infos = info.query.all()
    results = infos_schema.dump(all_infos)
    return jsonify(results)

@app.route('/get', methods = ['GET'])
def get_info():
    #return jsonify({"hello": "world"})
    all_infos = info.query.all()
    results = infos_schema.dump(all_infos)
    return jsonify(results)

@app.route('/get/<id>/', methods = ['GET'])
def get_detail_info(id):
    #return jsonify({"hello": "world"})
    info_detail = info.query.get(id)
    return info_schema.jsonify(info_detail)


@app.route('/update/<id>/', methods = ['PUT'])
def update_info(id):
    #return jsonify({"hello": "world"})
    info_detail = info.query.get(id)
    
    title = request.json['title']
    body = request.json['body']
    
    info_detail.title = title
    info_detail.body = body
    
    db.session.commit()
    return info_schema.jsonify(info_detail)


@app.route('/delete/<id>/', methods = ['DELETE'])
def delete_info(id):
    #return jsonify({"hello": "world"})
    info_detail = info.query.get(id)
    
    db.session.delete(info_detail)
    db.session.commit()
    
    return info_schema.jsonify(info_detail)


@app.route('/add', methods = ['POST'])
def add_info():
    title = request.json['title']
    body = request.json['body']
    
    infos = info(title, body)
    db.session.add(infos)
    db.session.commit()
    return info_schema.jsonify(infos)

@app.route('/open')
def open():
    sendOpenSignal()

@app.route('/notopen')
def not_open():
    sendNotOpenSignal()

@app.route('/taketrainpath', methods=['POST'])
def take_train_path():
    global train_path
    request_data = json.loads(request.data)
    train_path = request_data['content']
    
@app.route('/taketestpath', methods=['POST'])
def take_test_path():
    global image_path
    request_data = json.loads(request.data)
    image_path = request_data['content']

@app.route('/test')
def test():
  return tmtest(train_path,image_path)

@app.route('/train')
def train():
  tmtrain(train_path)
    
if __name__ == "main":
    app.run(debug=True)
