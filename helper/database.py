from pymongo import MongoClient
from config import Config
from .utils import send_log
import sys

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

async def add_user(user_id, b, u):
    in_db = already_db(user_id)
    if in_db:
        return
    
    users.insert_one({"user_id": str(user_id), "bool_approve": False, "bool_leave": False, 'approve_msg': False, 'leave_msg': False})
    try:
        await send_log(b=b, u=u)
    except Exception as e:
         print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
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
        user = users.find_one({"user_id": str(user_id)}).get('bool_leave')
        return user

def get_bool_approve_msg(user_id):
        user = users.find_one({"user_id": str(user_id)}).get('bool_approve')
        return user

def get_leave_msg(user_id):
      user = users.find_one({'user_id': str(user_id)}).get('leave_msg')
      return user

def get_approve_msg(user_id):
      user = users.find_one({'user_id': str(user_id)}).get('approve_msg')
      return user

def set_leave_msg(user_id, message):
      users.update_one({'user_id': str(user_id)}, {'$set': {'leave_msg': message}})

def set_approve_msg(user_id, message):
      users.update_one({'user_id': str(user_id)}, {'$set': {'approve_msg': message}})

def set_bool_approve_msg(user_id, condition):
      users.update_one({"user_id": str(user_id)}, {'$set': {'bool_approve': condition}})
    
        
def set_bool_leave_msg(user_id, condition):
     users.update_one({"user_id": str(user_id)}, {'$set': {'bool_leave': condition}})
    
