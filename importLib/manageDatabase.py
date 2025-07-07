import os
from sqlite3 import connect as dbconnect
from sqlite3 import Cursor
import time
import random
from flask import Request
from werkzeug.security import generate_password_hash,check_password_hash
from .const_path import *
from .handlers import get_hash_code






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

    def update_db(self):
        """
        get_hash_code(t:time.time())-> str:
        将原先的int型id换成时间戳的sha256值
        创建articledb.db.update
        该文件用于更新数据库并且迁移数据
        原有的文章:
            将"%Y-%m-%d %H:%M:%S"格式的时间转换为时间戳
            将id转换为sha256的hash值

        """
        new_db_path = ARTICLEDB + ".update"
        with dbconnect(new_db_path) as new_db:
            cs=new_db.cursor()
            cs.execute("DROP TABLE if exists ARTICLE")
            cs.execute(
                "CREATE TABLE ARTICLE ("
                    "id TEXT PRIMARY KEY,"
                    "title TEXT,"
                    "upload_time INTEGER,"
                    "visible INTEGER,"
                    "show_weight INT,"
                    "topest INTEGER"
                ")"
            )
            with dbconnect(self.db) as db:
                old_cs=db.cursor()
                old_cs.execute("SELECT * FROM ARTICLE")
                for row in old_cs.fetchall():
                    new_id = get_hash_code(row[0])
                    upload_time = int(time.mktime(time.strptime(row[2], "%Y-%m-%d %H:%M:%S")))
                    cs.execute(
                        "INSERT INTO ARTICLE VALUES (?,?,?,?,?,?)",
                        (new_id, row[1], upload_time, row[3], row[4], row[5])
                    )
                    os.rename(f"{UPLOADEDARTICLEPATH}/{'%05d'%(row[0],)}", f"{UPLOADEDARTICLEPATH}/{new_id}")
                old_cs.close()
            cs.close()
            new_db.commit()
            
        import gc
        from sqlite3 import Connection
        gc.collect()
        Connection.close(db)
        Connection.close(new_db)
        if os.path.exists(self.db) and os.path.exists(self.db + ".update"):
            os.remove(self.db)
            os.rename(self.db + ".update", self.db)
    
    def init_db(self):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("DROP TABLE if exists ARTICLE")
            cs.execute(
                "CREATE TABLE ARTICLE ("
                    "id TEXT PRIMARY KEY,"
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
                    "id TEXT PRIMARY KEY,"
                    "title TEXT,"
                    "upload_time TEXT,"
                    "show_weight INT,"
                    "topest INTERGER"
                ")"
            )
            cs.close()


    def validateArticleId(self,id:str)->bool:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("SELECT * FROM ARTICLE WHERE id=?", (id,))
            res=cs.fetchone() is not None
            cs.close()
            return  res
    
    def validatePreuploadId(self,id:str)->bool:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("SELECT * FROM PREUPLOAD WHERE id=?", (id,))
            res= cs.fetchone() is not None
            cs.close()
            return res


    
    def publishArticle(self,article):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "INSERT INTO ARTICLE VALUES (?,?,?,?,?,?)",
                (
                    article["id"],
                    article["title"],
                    int(time.mktime(article["upload_time"])),
                    article["visible"],
                    article["show_weight"],
                    article["topest"]
                )
            )
            cs.close()
            db.commit()


    def editArticle(self,id:str,article:dict):
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
            cs.close()
            db.commit()

    def deleteArticle(self,id:str):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "DELETE FROM ARTICLE WHERE id=?",
                (id,)
            )
            cs.close()
            db.commit()
        
    def delete_preuploadArticle(self,id:str):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "DELETE FROM PREUPLOAD WHERE id=?",
                (id,)
            )
            cs.close()
            db.commit()

    def preuploadArticle(self,article):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "INSERT INTO PREUPLOAD VALUES (?,?,?,?,?)",
                (
                    article["id"],
                    article["title"],
                    article["upload_time"],
                    article["show_weight"],
                    article["topest"]
                )
            )
            cs.close()
            db.commit()

    def is_article_visible(self,id:str)->bool:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "select visible from ARTICLE where id=?",
                (id,)
            )
            res=cs.fetchone()
            cs.close()
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
            res=cs.fetchall()
            cs.close()
            return(res)
    
    def getAllArticle(self)->list[int]:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "SELECT id FROM ARTICLE "
                "ORDER BY show_weight DESC, upload_time DESC, topest DESC "
            )
            res=cs.fetchall()
            cs.close()
            return(res)

    def getArticles(self,page:int=1)->list[int]:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "SELECT id FROM ARTICLE WHERE visible=1 "
                "ORDER BY show_weight DESC, upload_time DESC, topest DESC "
                "LIMIT ? OFFSET ?",
                (10, (page-1) * 10)
            )
            res=cs.fetchall()
            cs.close()
            return(res)
    
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
                res.append(dict(zip(("id", "title", "upload_time", "show_weight", "topest"), tmp)))
            cs.close()
            return res

    def getArticleFromId(self,id:str)->dict:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "select title,upload_time,topest from ARTICLE where id=?",
                (id,)
            )
            res=cs.fetchone()
            cs.close()
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
    


    def getPreuploadArticleFromId(self,id:str)->dict:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute(
                "select title,upload_time,topest from PREUPLOAD where id=?",
                (id,)
            )
            res=cs.fetchone()
            cs.close()
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
            cs.execute("CREATE TABLE LOGIN_LOG (admin_name TEXT, time INTERGER,IP TEXT)")
            
            cs.execute("DROP TABLE if exists PASSWORD_ERROR_LOG")
            cs.execute("CREATE TABLE PASSWORD_ERROR_LOG (IP TEXT PRIMARY KEY,TIMES INT,LAST_TIME TEXT)")
            
            cs.execute("DROP TABLE if exists CONFIG")
            cs.execute("CREATE TABLE CONFIG (CONFIG_NAME TEXT, CONFIG_VALUE TEXT)")

            cs.execute("INSERT INTO CONFIG VALUES (?,?)",("password_key",os.urandom(6).hex()))
            cs.execute("INSERT INTO CONFIG VALUES (?,?)",("salt","admin"))
            cs.close()
            db.commit()

    def update_db(self):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("DROP TABLE if exists login_log")
            cs.execute("create table login_log(admin_name text,time integer,ip text)")
            cs.close()

    def get_login_logs_length(self,time_range=(0,0))->int:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            if(time_range[0] != 0):
                cs.execute(
                    "SELECT count(*) FROM LOGIN_LOG WHERE time >= ? AND time <= ?",
                    time_range
                )
            else:
                cs.execute("SELECT count(*) FROM LOGIN_LOG")
            res=cs.fetchone()[0]
            cs.close()
            return(res)
    
    def get_login_logs_pages(self,time_range=(0,0),numPerpage=50)->int:
        total=self.get_login_logs_length(time_range)
        return (total//numPerpage)+(total%numPerpage>0)

    def get_login_logs(self,page=1,time_range=(0,0),numPerPage=50)->list[dict]:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            if(time_range[0] !=  0):
                cs.execute(
                    "SELECT admin_name,time,IP FROM LOGIN_LOG WHERE time >= ? AND time <= ? ORDER BY time DESC LIMIT ? OFFSET ?",
                    (time_range[0],time_range[1],numPerPage,(page-1)*numPerPage)
                )
            else:
                cs.execute(
                    "SELECT admin_name,time,IP FROM LOGIN_LOG ORDER BY time DESC LIMIT ? OFFSET ?",
                    (numPerPage,(page-1)*numPerPage)
                )
            temp=cs.fetchall()
            cs.close()
            res=[]
            for i in temp:
                res.append(dict(zip(("admin_name","login_time","ip_address"),i)))
            return(res)

    def get_name_password(self,cookie:dict):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("select config_value from config where config_name='password_key'")
            password_key=cs.fetchone()[0]
            cs.close()
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
            res=self.__summon_confuse(cs)
            cs.close()
            db.commit()
            return(res)
    
    def __clear_confuse(self,cs:Cursor):
        cs.execute("select confuse_key from CONFUSE")
        confuse_strs=cs.fetchall()
        cs.execute("delete from CONFUSE")
        return confuse_strs
    
    def clear_refuse(self)->list:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            res=self.__clear_confuse(cs)
            cs.close()
            db.commit()
            return(res)

        
    def __get_config(self,config_name:str,cs:Cursor):
        cs.execute("select config_value from config where config_name=?",(config_name,))
        res=cs.fetchone()[0]
        return res

    def get_config(self,config_name:str):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            res=self.__get_config(config_name,cs)
            cs.close()
            return res

    def __set_config(self,config_name:str,config_value:str,cs:Cursor):
        old_config_value=self.__get_config(config_name,cs)[0]
        cs.execute("update config set config_value=? where config_name=?",(config_value,config_name))
        return old_config_value

    def set_config(self,config_name:str,config_value:str):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            res=self.__get_config(config_name,cs)
            cs.close()
            db.commit()
            return res
        
    def change_name(self,origin_name,name):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("update admin set admin_name=? where admin_name=?",(name,origin_name))
            cs.execute("UPDATE LOGIN_LOG SET admin_name=? WHERE admin_name=?", (name, origin_name))
            cs.close()
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
            cs.close()
            db.commit()
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
            cs.close()
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
                login_time=time.time()
                cs.execute("INSERT INTO LOGIN_LOG(admin_name,time,ip) VALUES(?,?,?)",(name,login_time,ip))
                cs.close()
                db.commit()
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
            cs.close()
            if(data==None):
                return False
            (_,_password)=data
            if(password==_password):
                return True
            else:
                return False





