#!flask/bin/python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:piano6186@localhost:3306/iwswebrequest'
db = SQLAlchemy(app)

class FeatureRequest(db.Model):
	feature_request_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	description = db.Column(db.String(500))
	target_date = db.Column(db.DateTime)
	product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.product_area_id'))
	client_features = db.relationship('ClientFeature', backref='feature_request', lazy='dynamic')
	
	def __init__(self, title, description, target_date, product_area_id):
		self.title = title
		self.description = description
		self.target_date = target_date
		self.product_area_id = product_area_id
		
	def __repr__(self):
		return '<Title %r>' % self.title

class ProductArea(db.Model):
	product_area_id = db.Column(db.Integer, primary_key=True)
	product_area_name = db.Column(db.String(255))

	def __init__(self, product_area_name):
		self.product_area_name = product_area_name
	
	def __repr__(self):
		return '<Product Area Name %r>' % self.product_area_name
	
class Client(db.Model):
	client_id = db.Column(db.Integer, primary_key=True)
	client_name = db.Column(db.String(255))
	
	def __init__(self, client_name):
		self.client_name = client_name
		
	def __repr__(self):
		return '<Client Name %r>' % self.client_name
	
class ClientFeature(db.Model):
	client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), primary_key=True)
	feature_id = db.Column(db.Integer, db.ForeignKey('feature_request.feature_request_id'), primary_key=True)
	priority = db.Column(db.Integer)
	
	def __init__(self, client_id, feature_id, priority):
		self.client_id = client_id
		self.feature_id = feature_id
		self.priority = priority
		
	def __repr__(self):
		return '<Client Feature %r>' % self.client_id
	
@app.route('/iwswebrequest/api/v1.0/features/<int:id>', methods=['GET'])
def get_feature(id):
	feature = FeatureRequest.query.filter_by(feature_request_id = id).first()
	productArea = ProductArea.query.filter_by(product_area_id = feature.product_area_id).first()

	return jsonify({'feature': {
		'title': feature.title,
		'id': feature.feature_request_id,
		'description': feature.description,
		'target_date': feature.target_date,
		'product_area_id': feature.product_area_id,
		'product_area': productArea.product_area_name,
		'client_id': feature.client_features.first().client_id,
		'client': Client.query.filter_by(client_id = feature.client_features.first().client_id).first().client_name}})

@app.route('/iwswebrequest/api/v1.0/clients/', methods=['GET'])
def get_clients():
	clientsJson = {'clients':[]}
	for client in db.session.query(Client):
		clientsJson['clients'].append({client.client_id: client.client_name})
	return jsonify(clientsJson)
	
@app.route('/iwswebrequest/api/v1.0/productAreas/', methods=['GET'])
def get_product_areas():
	productAreasJson = {'productAreas':[]}
	for productArea in db.session.query(ProductArea):
		productAreasJson['productAreas'].append({productArea.product_area_id: productArea.product_area_name})
	return jsonify(productAreasJson)	
	
@app.route('/iwswebrequest/api/v1.0/features/create/', methods=['POST'])
def create_feature():
	feature = FeatureRequest(
		request.json['title'],
		request.json['description'],
		request.json['target_date'],
		request.json['product_area_id'])
	db.session.add(feature)
	db.session.commit()
	client_feature = ClientFeature(
			request.json['clientId'],
			feature.feature_id,
			request.json['priority']
		)
	session.add(client_feature)
	db.session.commit()
	return jsonify({'feature':'added'})

@app.route('/iwswebrequest/api/v1.0/features/addFeatureClient/', methods=['POST'])
def add_feature_client():
	client_feature = ClientFeature(
			request.json['clientId'],
			request.json['featureId'],
			request.json['priority']
		)
	db.session.add(client_feature)
	db.session.commit()
	return jsonify({'client feature': 'added'})
	
if __name__ == '__main__':
	app.run(debug=True)