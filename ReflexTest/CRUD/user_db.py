# Trash_logs = [ [item_id, photo_id] , [item_id, photo_id] ]

def add_user(mydb, username, password):
    userdb = mydb["Users"]
    user = {"username": username, "password": password, "points": 0, "trash_logs": []}

    # Insert the user data into the database, if the user does not already exist.
    if not userdb.find_one({"username", username}):
        userdb.insert_one(user)
        return True
    else:
        return False
    
def get_user(mydb, username, password):
    userdb = mydb["Users"]
    return userdb.find_one({"username": username, "password": password})

def add_a_trash(mydb, user, point, trash_id, image_id):
    userdb = mydb["Users"]
    user["points"] += point
    new_log = [trash_id, image_id]
    user["trash_logs"].append(new_log)

    userdb.update_one({"username": user["username"]}, {"$set": {"points": user["points"], "trash_logs": user["trash_logs"]}})
    return user

def delete_a_trash(mydb, user, index):
    userdb = mydb["Users"]
    new_trash_logs = user["trash_logs"].pop(index)
    try:
        userdb.update_one({"username": user["username"]}, {"$set": {"trash_logs": new_trash_logs}})
        return True
    except:
        return False
    