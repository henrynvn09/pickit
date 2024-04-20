# {"username": username, "password": password, "points": 0, "trash_logs": []}

class User():
    def __init__(self, username, password, avatar="default_avatar.png"):
        self.username = username
        self.password = password
        self.avatar = avatar
        self.points = 0
        self.trash_logs = []

    def __init__(self, user_dict:dict):
        self.username = user_dict["username"]
        self.password = user_dict["password"]
        self.avatar = user_dict["avatar"]
        self.points = user_dict["points"]
        self.trash_logs = user_dict["trash_logs"]

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password
    
    def get_avatar(self):
        return self.avatar

    def get_points(self):
        return self.points

    def get_trash_logs(self):
        return self.trash_logs

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_avatar(self, avatar):
        self.avatar = avatar

    def add_points(self, points):
        self.points += points

    def set_trash_logs(self, trash_logs):
        self.trash_logs = trash_logs

    def add_trash_log(self, trash_log):
        self.trash_logs.append(trash_log)
    
    def remove_trash_log(self, index:int):
        self.trash_logs.pop(index)

    def __str__(self):
        return f"username: {self.username}, password: {self.password}, points: {self.points}, trash_logs: {self.trash_logs}"