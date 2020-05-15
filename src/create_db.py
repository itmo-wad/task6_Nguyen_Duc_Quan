from pymongo import MongoClient
import pprint
myclient = MongoClient('localhost',27017)
mydb = myclient["mydb"]
mydb = myclient["lab4"]
mycol = mydb["accounts"]

mycol.insert_one({ "username": "admin", "password": "admin" })



