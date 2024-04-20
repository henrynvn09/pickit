import pymongo

def get_db_instance():
    myclient = pymongo.MongoClient("mongodb+srv://henryvn09:EvRzQmZWb7oa4uLT@cluster0.lpqwcjb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    mydb = myclient["mydatabase"]
    return mydb