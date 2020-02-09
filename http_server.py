from threading import Thread
from flask import Flask,request,jsonify
from flask_cors import CORS
import pymongo
from hashlib import sha256
from yahoo_fin import stock_info as si
import pandas

app = Flask('')
CORS(app)

username=None

users = pymongo.MongoClient("mongodb+srv://DavidJoy:DHJ4clouddb@hackathonapp-6knru.gcp.mongodb.net/test?retryWrites=true&w=majority").test_database.users

def format_money(innum):
	neg=innum<0
	innum=abs(innum)
	return ("-" if neg else "")+"$"+str(innum//100)+"."+("0"+str(innum%100) if innum%100<10 else str(innum%100))

def process(in_amt):
	in_amt=str(in_amt+0.005)
	return in_amt[0:in_amt.index(".")+3]

@app.route('/graph/',methods=["POST"])
def get_graph_data():
	args = request.get_json(force=True)
	try:
		raw_data = si.get_data(args["ticker"], "1/9/2020", "2/9/2020")
		return "|".join([process(i) for i in raw_data["close"].tolist()])
	except:
		return ("5.0|"*21)[:-1]

@app.route('/watch/',methods=["POST"])
def watch_stock():
	global username
	args = request.get_json(force=True)
	try:
		si.get_live_price(args["ticker"])
	except:
		return "That ticker symbol does not exist"
	watch_set=users.find_one({"username":username})["watch"]
	watch_set.add(args["ticker"])
	username.update_one({"username":username},{"$set":{"watch",watch_set}})
	return "Added to watch list"

@app.route('/owned/',methods=["POST"])
def get_stock_data():
	global username
	args = request.get_json(force=True)
	outstr=""
	stocks=users.find_one({"username":username})["stocks"]
	i=0
	for s in stocks:
		price=int(100*si.get_live_price(s)+0.5)
		outstr+=s+"|"+format_money(price)+"|"+str(stocks[s])+"|"+format_money(price*stocks[s])+"|"+format_money(0)+"|"
		i+=1
		if(i==5):
			break;
	return outstr+(max(0,5-i)*" | | | | |")

@app.route('/buy/',methods=["POST"])
def buy_stock():
	global username
	args = request.get_json(force=True)
	print(args)
	args["ticker"]=args["ticker"].upper()
	args["quantity"]=int(args["quantity"])
	if(username==None):
		return "You are not logged in"
	try:
		totalPrice=args["quantity"]*int(100*si.get_live_price(args["ticker"])+0.5)
	except:
		return "That ticker does not exist"
	u=users.find_one({"username":username})
	if(totalPrice>u["money"]):
		return "You do not have enough money.  The total price is "+format_money(totalPrice)
	s=u["stocks"]
	if(args["ticker"] in s):
		s[args["ticker"]]+=args["quantity"]
	else:
		s[args["ticker"]]=args["quantity"]
	users.update_one({"username":username},{"$set":{"stocks":s,"money":u["money"]-totalPrice}})
	return "Successfully bought!"

@app.route('/sell/',methods=["POST"])
def sell_stock():
	global username
	args = request.get_json(force=True)
	print(args)
	args["ticker"]=args["ticker"].upper()
	args["quantity"]=int(args["quantity"])
	if(username==None):
		return "You are not logged in"
	u=users.find_one({"username":username})
	if(args["ticker"] not in u["stocks"]):
		return "You do not own that stock."
	if(args["quantity"]>u["stocks"][args["ticker"]]):
		return "You only own "+str(u["stocks"][args["ticker"]])+" of that stock."
	totalValue=args["quantity"]*int(100*si.get_live_price(args["ticker"])+0.5)
	s=u["stocks"]
	if(s[args["ticker"]]==args["quantity"]):
		s.pop(args["ticker"])
	else:
		s[args["ticker"]]-=args["quantity"]
	users.update_one({"username":username},{"$set":{"stocks":s,"money":u["money"]+totalValue}})
	return "Successfully sold!"

@app.route('/create/',methods=["POST"])
def create_account():
	args = request.get_json(force=True)
	print("create POST: "+str(args))
	if(users.find_one({"username":args["username"]})!=None):
		return "Error: That username already exists.  Please choose a new username."
	users.insert_one({"username":args["username"],"password_hash":sha256(args["password"].encode()).hexdigest(),"stocks":dict(),"watch":set(),"money":100000000,"xp":0,"trades_count":0})
	return "Successfully created your account.  You may now login."

@app.route('/login/', methods=["POST"])
def login():
	global username
	args = request.get_json(force=True)
	if(users.find_one({"username":args["username"],"password_hash":sha256(args["password"].encode()).hexdigest()})==None):
		return "Incorrect username or password"
	username=args["username"]
	return "y"

@app.route('/')
def home():
	return "hello world!"

def run():
  app.run(host='127.0.0.1',port=8080)

def keep_alive():
	t = Thread(target=run)
	t.start()

keep_alive()