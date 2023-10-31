from pymongo import MongoClient
from config import Config

client = MongoClient(Config.DB_URL)

users = client['main']['users']
groups = client['main']['groups']

def already_db(user_id):
        user = users.find_one({"user_id" : str(user_id)})
        if not user:
            return False
        return True

def already_dbg(chat_id):
        group = groups.find_one({"chat_id" : str(chat_id)})
        if not group:
            return False
        return True

def add_user(user_id):
    in_db = already_db(user_id)
    if in_db:
        return
    return users.insert_one({"user_id": str(user_id), "bool_approve": False, "bool_leave": False})

def remove_user(user_id):
    in_db = already_db(user_id)
    if not in_db:
        return 
    return users.delete_one({"user_id": str(user_id)})
    
def add_group(chat_id):
    in_db = already_dbg(chat_id)
    if in_db:
        return
    return groups.insert_one({"chat_id": str(chat_id)})

def all_users():
    user = users.find({})
    usrs = len(list(user))
    return usrs

def all_groups():
    group = groups.find({})
    grps = len(list(group))
    return grps

def get_bool_leave_msg(user_id):
        user = users.find_one({"user_id": str(user_id)})
        return user

def get_bool_approve_msg(user_id):
        user = users.find_one({"user_id": str(user_id)})
        return user

def set_bool_approve(user_id, condition):
        users.update_one({"user_id": str(user_id), "bool_approve": condition})
        
def set_bool_leave(user_id, condition):
        users.update_one({"user_id": str(user_id), "bool_leave": condition})
