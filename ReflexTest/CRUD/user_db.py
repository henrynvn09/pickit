import pymongo
import reflex as rx
from ReflexTest.classes.user import User
from ReflexTest.pages.index import UserState

def add_user(mydb, username, password):
    userdb = mydb["Users"]
    user:User = User(username, password)

    # Insert the user data into the database, if the user does not already exist.
    if not userdb.find_one({"username": username}):
        userdb.insert_one(user.__dict__)
        return True
    else:
        return False
    
def get_user(mydb, username, password) -> User:
    userdb = mydb["Users"]
    user_dict = userdb.find_one({"username": username, "password": password})
    if user_dict:
        return User.init_from_dict(user_dict)
    else:
        return None


def get_user_without_password(mydb, username) -> User:
    userdb = mydb["Users"]
    user_dict = userdb.find_one({"username": username})
    if user_dict:
        return User.init_from_dict(user_dict)
    else:
        return None

def add_a_trash(mydb, user_name, point, trash_name, image_id):
    userdb = mydb["Users"]

    user:User = get_user_without_password(mydb, user_name)

    user.add_points(point)
    
    new_log = {"name": trash_name, "point": point, "img": image_id}
    user.add_trash_log(new_log)

    print(user)
    userdb.update_one({"username": user.get_username()}, {"$set": {"points": user.get_points(), "trash_logs": user.get_trash_logs()}})
    

def delete_a_trash(mydb, user, index):
    userdb = mydb["Users"]
    user.remove_trash_log(index)

# if __name__ == "__main__":
#     print("This is a module file. Please import this module to use the functions.")
    
#     myclient = pymongo.MongoClient("")
#     mydb = myclient["mydatabase"]
    
#     print(add_user(mydb, "test", "test"))
