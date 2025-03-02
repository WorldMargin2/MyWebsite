import os
from sqlite3 import connect as dbconnect
from sqlite3 import Cursor
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
            
            cs.execute("INSERT INTO Admin VALUES (?,?)",("admin",generate_password_hash("adminadmin")))

            cs.execute("DROP TABLE if exists CONFUSE")
            cs.execute("CREATE TABLE CONFUSE (confuse_key TEXT)")
            
            cs.execute("DROP TABLE if exists LOGIN_LOG")
            cs.execute("CREATE TABLE LOGIN_LOG (admin_name TEXT, time TEXT,IP TEXT)")
            
            cs.execute("DROP TABLE if exists PASSWORD_ERROR_LOG")
            cs.execute("CREATE TABLE PASSWORD_ERROR_LOG (IP TEXT PRIMARY KEY,TIMES INT,LAST_TIME TEXT)")
            
            cs.execute("DROP TABLE if exists CONFIG")
            cs.execute("CREATE TABLE CONFIG (CONFIG_NAME TEXT, CONFIG_VALUE TEXT)")

            cs.execute("INSERT INTO CONFIG VALUES (?,?)",("password_key",os.urandom(6).hex()))
            cs.execute("INSERT INTO CONFIG VALUES (?,?)",("salt","admin"))

            db.commit()



    def get_name_password(self,cookie:dict):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("select config_value from config where config_name='password_key'")
            password_key=cs.fetchone()[0]
            name=cookie.get("admin_name")
            password=cookie.get(password_key)
            return (name,password)
    
    def __summon_confuse(self,cs:Cursor):
        confuse_strs=(
            (os.urandom(6).hex(),)
            for i in range(10)
        )
        cs.executemany("INSERT INTO CONFUSE VALUES (?)",confuse_strs)
        return confuse_strs

    def summon_confuse(self):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            return(self.__summon_confuse(cs))
    
    def __clear_confuse(self,cs:Cursor):
        cs.execute("select confuse_key from CONFUSE")
        confuse_strs=cs.fetchall()
        cs.execute("delete from CONFUSE")
        return confuse_strs
    
    def clear_refuse(self)->list:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            return(self.__clear_confuse(cs))

        
    def __get_config(self,config_name:str,cs:Cursor):
        cs.execute("select config_value from config where config_name=?",(config_name,))
        return cs.fetchone()[0]

    def get_config(self,config_name:str):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            return self.__get_config(config_name,cs)

    def __set_config(self,config_name:str,config_value:str,cs:Cursor):
        old_config_value=self.__get_config(config_name,cs)
        cs.execute("update config set config_value=? where config_name=?",(config_value,config_name))
        return old_config_value

    def set_config(self,config_name:str,config_value:str):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            return self.__set_config(config_name,config_value,cs)


    def login(self,name:str,password:str,ip:str)->dict:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            salt=self.__get_config("salt",cs)
            cs.execute("SELECT * FROM Admin WHERE admin_name=?",(name,))
            data=cs.fetchone()
            if(data==None):
                return (None)
            (_,_password)=data
            if(check_password_hash(_password,password+salt)):
                new_salt=os.urandom(6).hex()
                new_hashed_pwd=generate_password_hash(password+new_salt)
                password_key=os.urandom(6).hex()
                cs.execute("UPDATE Admin SET password=? WHERE admin_name=?",(new_hashed_pwd,name))
                self.__set_config("password_key",password_key,cs)
                self.__set_config("salt",new_salt,cs)
                confuse_strs=self.__summon_confuse(cs)
                res={
                        i:generate_password_hash(os.urandom(6).hex()) for i in confuse_strs
                    }
                res.update({
                    "admin_name":name,
                    password_key:new_hashed_pwd,
                })
                return (
                    res
                )
            else:
                return (None)

    
    def check_longin(self,cookie:dict):
        if cookie==None:
            return False
        admin_name,password=self.get_name_password(cookie)
        if( not (admin_name and password)):
            return False
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("SELECT * FROM Admin WHERE admin_name=?",(admin_name,))
            data=cs.fetchone()
            if(data==None):
                return False
            (_,_password)=data
            if(password==_password):
                return True
            else:
                return False
            


        

