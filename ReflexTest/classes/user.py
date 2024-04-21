# {"username": username, "password": password, "points": 0, "trash_logs": []}
import reflex as rx

class User():
    username: str
    password: str
    avatar: str
    points: int
    trash_logs: list

    def __init__(self, username="", password:str="", avatar="default_avatar.png"):
        self.username = username
        self.password = password
        self.avatar = avatar
        self.points = 0
        self.trash_logs = []
    
    def __init_from_dict(self, user_dict: dict):
        self.username = user_dict.get("username", "")
        self.password = user_dict.get("password", "")
        self.avatar = user_dict.get("avatar", "default_avatar.png")
        self.points = user_dict.get("points", 0)
        self.trash_logs = user_dict.get("trash_logs", [])
        
    @classmethod
    def init_from_dict(cls, user_dict: dict):
        instance = cls()
        instance.__init_from_dict(user_dict)
        return instance

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
    