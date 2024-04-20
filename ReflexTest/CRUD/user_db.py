from ReflexTest.classes.user import User

def add_user(mydb, username, password):
    userdb = mydb["Users"]
    user:User = User(username, password)

    # Insert the user data into the database, if the user does not already exist.
    if not userdb.find_one({"username", username}):
        userdb.insert_one(user.__dict__)
        return True
    else:
        return False
    
def get_user(mydb, username, password):
    userdb = mydb["Users"]
    user_dict = userdb.find_one({"username": username, "password": password})
    if user_dict:
        return User.init_from_dict(user_dict)
    else:
        return None

def add_a_trash(mydb, user:User, point, trash_name, image_id):
    userdb = mydb["Users"]  

    user.add_points(point)
    
    new_log = {"trash_name": trash_name, "image": image_id}
    user.add_trash_log(new_log)


    userdb.update_one({"username": user.get_username()}, {"$set": {"points": user.get_points(), "trash_logs": user.get_trash_logs()}})
    return user

def delete_a_trash(mydb, user, index):
    userdb = mydb["Users"]
    user.remove_trash_log(index)
