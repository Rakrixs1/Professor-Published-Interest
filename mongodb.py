
from pymongo import MongoClient
import pymongo
  
def mongodbconnect():
        conn = MongoClient(host = "mongodb://localhost:27017/")
        return conn['academicworld']





