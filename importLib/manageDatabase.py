import os
from sqlite3 import connect as dbconnect
import time
import random
from flask import Request
from werkzeug.security import generate_password_hash,check_password_hash




DATABASEPATH="./database/"

USERDB=f"{DATABASEPATH}user.db"
ARTICLEDB=f"{DATABASEPATH}article.db"


class Database:
    db=""
    def init_db(self):
        pass
    def __init__(self):
        if(not os.path.exists(DATABASEPATH)):
            os.mkdir(DATABASEPATH)
        if(not os.path.exists(self.db)):
            with dbconnect(self.db,timeout=10) as db:
                pass
        self.init_db()

class UserDB(Database):
    db=USERDB
    max_salt_count=10
    max_log_count=50
    max_pass_error_count=5

    def __init__(self):
        super().__init__()

    def init_db(self):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("DROP TABLE if exists Admin")
            cs.execute("CREATE TABLE Admin (admin_name TEXT, password TEXT)")
            
            cs.execute("INSERT INTO Admin VALUES (?,?)",("admin",generate_password_hash("admin")))
            
            cs.execute("DROP TABLE if exists LOGIN_LOG")
            cs.execute("CREATE TABLE LOGIN_LOG (admin_name TEXT, time TEXT,IP TEXT)")
            
            cs.execute("DROP TABLE if exists PASSWORD_ERROR_LOG")
            cs.execute("CREATE TABLE PASSWORD_ERROR_LOG (IP TEXT PRIMARY KEY,TIMES INT,LAST_TIME TEXT)")
            
            cs.execute("DROP TABLE if exists CONFIG")
            cs.execute("CREATE TABLE CONFIG (CONFIG_NAME TEXT, CONFIG_VALUE TEXT)")
            db.commit()

    def login(self,user,password):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("SELECT * FROM Admin WHERE admin_name=?",(user,))
            data=cs.fetchone()
            if(data==None):
                return (None)
            (_,_password)=data
            if(check_password_hash(_password,password)):
                return (generate_password_hash(_password))
            else:
                return (None)

    
    def check_longin(self,cookie:dict):
        if cookie==None:
            return False
        admin_name=cookie.get("admin_name")
        password=cookie.get("password")
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("SELECT * FROM Admin WHERE admin_name=?",(admin_name,))
            data=cs.fetchone()
            if(data==None):
                return False
            (_,_password)=data
            if(check_password_hash(password,_password)):
                return True
            else:
                return False
            
    def logout(self,cookie:dict):
        cookie.clear()
        

