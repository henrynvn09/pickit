
def get_trash(mydb, trash_name):
    trashdb = mydb["Trash"]
    trash = trashdb.find_one({"name": trash_name})
    
    if not trash:
        #TODO: ask gemini to generate a new the trash here
        new_trash = {"name": trash_name, "point": 1, "cartoon_img": "relative img path"}

        # add the generated point to the database
        trashdb.insert_one(new_trash)
        return new_trash
    
    return trash