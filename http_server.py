from flask import Flask,request,jsonify
from flask_cors import CORS

import pymongo
from hashlib import sha256

app = Flask('')
CORS(app)

users = pymongo.MongoClient("mongodb+srv://DavidJoy:DHJ4clouddb@hackathonapp-6knru.gcp.mongodb.net/test?retryWrites=true&w=majority").test_database.users

@app.route('/create/',methods=["POST"])
def create_account():
	args = request.get_json(force=True)
	if(users.find_one({"username":args["username"]})!=None):
		return "Error: That username already exists.  Please choose a new username."
	users.insert_one({"username":args["username"],"password_hash":sha256(args["password"].encode()).hexdigest(),"stocks":dict(),"watch":list(),"money":100000000,"xp":0,"trades_count":0})
	return "Successfully created your account.  You may now login."

@app.route('/login/', methods=["POST"])
def data_transfer():
	print(request.get_json(force=True))
	return "yooo"

@app.route('/', methods=["GET"])
def home():
	return "hello world!"

app.run(host='127.0.0.1',port=8080)