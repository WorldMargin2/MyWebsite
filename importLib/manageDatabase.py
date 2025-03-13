import os
from sqlite3 import connect as dbconnect
from sqlite3 import Cursor
import time
import random
from flask import Request
from werkzeug.security import generate_password_hash,check_password_hash
from .const_path import *






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

class ArticleDB(Database):
    db=ARTICLEDB

    def __init__(self):
        super().__init__()
    
    def init_db(self):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("DROP TABLE if exists ARTICLE")
            cs.execute(
                "CREATE TABLE ARTICLE ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "title TEXT,"
                    "upload_time TEXT,"
                    "visible INTEGER,"
                    "show_weight INT,"
                    "topest INTEGER"
                ")"
            )

            cs.execute("DROP TABLE if exists PREUPLOAD")
            cs.execute(
                "CREATE TABLE PREUPLOAD ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT ,"
                    "title TEXT,"
                    "upload_time TEXT,"
                    "show_weight INT,"
                    "topest INTERGER"
                ")"
            )

    def _fetch_freeID(self,cs:Cursor):
        cs.execute(
            "select MIN(id+1)"
            " from ARTICLE AS T1"
            " where not exists( select * from ARTICLE where id=T1.id+1)"
        )
        return(cs.fetchone()[0])
    
    def fetch_free_ID(self):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            return(self._fetch_freeID(cs))
    
    def publishArticle(self,article):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "INSERT INTO ARTICLE VALUES (?,?,?,?,?,?)",
                (
                    int(article["id"]),
                    article["title"],
                    article["upload_time"],
                    article["visible"],
                    article["show_weight"],
                    article["topest"]
                )
            )
            db.commit()

    def editArticle(self,id:int,article:dict):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "UPDATE ARTICLE SET "
                    "title=?,"
                    "visible=?,"
                    "show_weight=?,"
                    "topest=?"
                " WHERE id=?",
                (
                    article["title"],
                    article["visible"],
                    article["show_weight"],
                    article["topest"],
                    id
                )
            )
            db.commit()

    def deleteArticle(self,id):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "DELETE FROM ARTICLE WHERE id=?",
                (id,)
            )
            db.commit()
        
    def delete_preuploadArticle(self,id:int):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "DELETE FROM PREUPLOAD WHERE id=?",
                (id,)
            )
            db.commit()

    def preuploadArticle(self,article):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "INSERT INTO PREUPLOAD VALUES (?,?,?,?,?)",
                (
                    int(article["id"]),
                    article["title"],
                    article["upload_time"],
                    article["show_weight"],
                    article["topest"]
                )
            )
            db.commit()

    def is_article_visible(self,id:int):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "select visible from ARTICLE where id=?",
                (id,)
            )
            res=cs.fetchone()
            if(res):
                return(res[0])
            return(None)
        
    def admin_getArticles(self,page:int=1)->list[int]:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "SELECT id FROM ARTICLE "
                "ORDER BY show_weight DESC, upload_time DESC, topest DESC "
                "LIMIT ? OFFSET ?",
                (10, (page-1) * 10)
            )
            return(cs.fetchall())
    
    def getAllArticle(self)->list[int]:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "SELECT id FROM ARTICLE "
                "ORDER BY show_weight DESC, upload_time DESC, topest DESC "
            )
            return(cs.fetchall())

    def getArticles(self,page:int=1)->list[int]:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "SELECT id FROM ARTICLE WHERE visible=1 "
                "ORDER BY show_weight DESC, upload_time DESC, topest DESC "
                "LIMIT ? OFFSET ?",
                (10, (page-1) * 10)
            )
            return(cs.fetchall())
    
    def getArticlesInfo(self,page:int=1)->list[dict]:
        articles_id=self.getArticles(page)
        with dbconnect(self.db) as db:
            cs=db.cursor()
            res=[]
            for i in articles_id:
                cs.execute(
                    "SELECT id, title, upload_time, show_weight, topest FROM ARTICLE WHERE id = ?",
                    (i[0],)
                )
                tmp=cs.fetchone()
                print(tmp)
                res.append(dict(zip(("id", "title", "upload_time", "show_weight", "topest"), tmp)))
            return res

    def getArticleFolderFromId(self,id:int)->str:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "select id from ARTICLE where id=?",
                (id,)
            )
            res=cs.fetchone()
            if(res):
                return("%05d"%(res[0],))
            return(None)

    def getArticleFromId(self,id:int)->dict:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "select title,upload_time,topest from ARTICLE where id=?",
                (id,)
            )
            res=cs.fetchone()
            if(res):
                return(
                    dict(
                        zip(
                            ("title","upload_time","topest"),
                            res
                        )
                    )
                )
            return(None)
    
    def getPreuploadFolderFromId(self,id:int)->str:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "select id from PREUPLOAD where id=?",
                (id,)
            )
            res=cs.fetchone()
            if(res):
                return("%05d"%(res[0],))
            return(None)

    def getPreuploadArticleFromId(self,id:int)->dict:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "select title,upload_time,topest from PREUPLOAD where id=?",
                (id,)
            )
            res=cs.fetchone()
            if(res):
                return(
                    dict(
                        zip(
                            ("title","upload_time","topest"),
                            res
                        )
                    )
                )
            return(None)

class AdminDB(Database):
    db=ADMINDB
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
        
    def change_name(self,origin_name,name):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("update admin set admin_name=? where admin_name=?",(name,origin_name))
            db.commit()
            return True

    def change_password(self,admin_name,pwd):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            new_salt=os.urandom(6).hex()
            new_hashed_pwd=generate_password_hash(pwd+new_salt)
            password_key=os.urandom(6).hex()
            cs.execute("UPDATE Admin SET password=? WHERE admin_name=?",(new_hashed_pwd,admin_name))
            self.__set_config("password_key",password_key,cs)
            self.__set_config("salt",new_salt,cs)
            confuse_strs=self.__summon_confuse(cs)
            res={
                    i:generate_password_hash(os.urandom(6).hex()) for i in confuse_strs
                }
            res.update({
                "admin_name":admin_name,
                password_key:new_hashed_pwd,
            })
            return (
                res
            )


    def check_pwd(self,name,pwd:str):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            salt=self.__get_config("salt",cs)
            cs.execute("SELECT * FROM Admin WHERE admin_name=?",(name,))
            data=cs.fetchone()
            if(data==None):
                return (None)
            (_,_password)=data
            if(check_password_hash(_password,pwd+salt)):
                return True
            else:
                return False

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
            


        

