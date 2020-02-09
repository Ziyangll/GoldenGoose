import pymongo

users = pymongo.MongoClient("mongodb+srv://DavidJoy:DHJ4clouddb@hackathonapp-6knru.gcp.mongodb.net/test?retryWrites=true&w=majority").test_database.users

for x in users.find({"name":"test"}):
	print(x)
print("breaker")
for x in users.find({"name":"no"}):
	print(x)