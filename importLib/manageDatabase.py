import os
from sqlite3 import connect as dbconnect
from sqlite3 import Cursor
import time
import random
from flask import Request
from werkzeug.security import generate_password_hash,check_password_hash
from .const_path import *
from .handlers import get_hash_code
from .ip2Region import Ip2Region






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
        pass
    
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
    max_log_count=99999
    max_pass_error_count=5

    cache={
        "config": {},
        "administs": { #max :50
            # $admin_name:{ "tokens":{$token:$ip}}
        },
    }

    def __init__(self):
        super().__init__()

    def init_db(self):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("DROP TABLE if exists Admin")
            #token : $token:$ip_address;...
            cs.execute("CREATE TABLE Admin (admin_name TEXT, password TEXT , tokens TEXT, PRIMARY KEY(admin_name))")
            
            cs.execute("INSERT INTO Admin VALUES (?,?)",("admin",generate_password_hash("adminadmin")))
            
            cs.execute("DROP TABLE if exists LOGIN_LOG")
            cs.execute("CREATE TABLE LOGIN_LOG (id PRIMARY KEY AUTOINCREMENT,admin_name TEXT, time INTERGER,IP TEXT,IP_REGION TEXT)")
            
            cs.execute("DROP TABLE if exists PASSWORD_ERROR_LOG")
            cs.execute("CREATE TABLE PASSWORD_ERROR_LOG (IP TEXT PRIMARY KEY,TIMES INT,LAST_TIME TEXT)")
            
            cs.execute("DROP TABLE if exists CONFIG")
            cs.execute("CREATE TABLE CONFIG (CONFIG_NAME TEXT, CONFIG_VALUE TEXT)")

            cs.close()
            db.commit()

    def update_db(self):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("DROP TABLE if exists Confuse")
            cs.execute("select * from Admin")
            info=["admin",self.get_hash_pwd("admin"),""]
            cs.execute("DROP TABLE if exists ADMIN")
            cs.execute("CREATE TABLE Admin (admin_name TEXT, password TEXT ,tokens TEXT, PRIMARY KEY(admin_name))")
            cs.execute("INSERT INTO Admin VALUES (?,?,?)",info)
            cs.execute("delete from config where config_name='password_key'")
            cs.execute("delete from config where config_name='salt'")
            cs.close()
            db.commit()

            

    # ==========================================LOGIN LOG========================================


    def insert_login_log(self,admin_name:str,login_time:int,ip:str):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            self._insert_login_log(cs,admin_name,login_time,ip)
            cs.close()
            db.commit()

    def _insert_login_log(self,cs:Cursor,admin_name:str,login_time:int,ip:str):
        searcher=Ip2Region(IP2REGIONDB)
        ip_region=searcher.memorySearch(ip).get("region",b"Unknown").decode("utf-8")
        searcher.close()
        cs.execute("INSERT INTO LOGIN_LOG(admin_name,time,ip,IP_REGION) VALUES(?,?,?,?)",(admin_name,login_time,ip,ip_region))
        cs.execute("select count(*) from LOGIN_LOG")
        log_count=cs.fetchone()[0]
        if(log_count>self.max_log_count):
            cs.execute("delete from LOGIN_LOG where id in (select id from LOGIN_LOG order by time limit ?)",(log_count-self.max_log_count,))

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
                    "SELECT id,admin_name,time,IP,IP_REGION FROM LOGIN_LOG WHERE time >= ? AND time <= ? ORDER BY time DESC LIMIT ? OFFSET ?",
                    (time_range[0],time_range[1],numPerPage,(page-1)*numPerPage)
                )
            else:
                cs.execute(
                    "SELECT id,admin_name,time,IP,IP_REGION FROM LOGIN_LOG ORDER BY time DESC LIMIT ? OFFSET ?",
                    (numPerPage,(page-1)*numPerPage)
                )
            temp=cs.fetchall()
            cs.close()
            res=[]
            for i in temp:
                res.append(dict(zip(("id","admin_name","login_time","ip_address","region"),i)))
            return(res)
        
    # ==========================================PASSWORD========================================


    

        
    def __get_config(self,config_name:str,cs:Cursor):
        if (config_name in self.cache["config"]):
            return self.cache["config"][config_name]
        cs.execute("select config_value from config where config_name=?",(config_name,))
        res=cs.fetchone()
        if res is None:
            res = None
        else:
            res = res[0]
        self.cache["config"][config_name]=res
        return res

    def get_config(self,config_name:str):
        if (config_name in self.cache["config"]):
            return self.cache["config"][config_name]

        with dbconnect(self.db) as db:
            cs=db.cursor()
            res=self.__get_config(config_name,cs)
            cs.close()
            return res

    def __set_config(self,config_name:str,config_value:str,cs:Cursor):
        self.cache["config"][config_name]=config_value
        old_config_value=self.__get_config(config_name,cs)
        cs.execute("update config set config_value=? where config_name=?",(config_value,config_name))
        return old_config_value

    def set_config(self,config_name:str,config_value:str):
        if ("config" not in self.cache):
            self.cache["config"]=dict()
            
        with dbconnect(self.db) as db:
            cs=db.cursor()
            res=self.__get_config(config_name,config_value,cs)
            cs.close()
            db.commit()
            return res
        
    def change_name(self,origin_name,name):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("select count(*) from admin where admin_name=?",(name,))
            if(cs.fetchone()[0]>0):
                return False
            cs.execute("update admin set admin_name=? where admin_name=?",(name,origin_name))
            cs.execute("UPDATE LOGIN_LOG SET admin_name=? WHERE admin_name=?", (name, origin_name))
            cs.close()
            db.commit()
            return True
        

    def get_custuom_encrypt_pwd(self,pwd:str)->str:
        last_char=pwd[-1]
        secret_value=ord(last_char) % len(pwd)
        res=""
        for i,c in enumerate(pwd):
            if i % 2 == 0:
                res+= chr(ord(c) | secret_value)
            else:
                res+= chr(ord(c) & secret_value)
        return res

    def get_hash_pwd(self,pwd:str)->str:
        return generate_password_hash(self.get_custuom_encrypt_pwd(pwd))
    
    def delete_token(self,name:str,token:str):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("SELECT tokens FROM Admin WHERE admin_name=?",(name,))
            data=cs.fetchone()
            if data is None:
                return False
            tokens=data[0].split(";")
            temp=dict()
            new_tokens=""
            for i in tokens:
                if i=="":
                    continue
                (t,ip)=i.split(":")
                if t!=token:
                    new_tokens+=f"{t}:{ip};"
                    temp[t]=ip
            self.cache["administs"][name]={
                "tokens":temp
            }
            cs.execute("UPDATE Admin SET tokens=? WHERE admin_name=?", (new_tokens,name))
            cs.close()
            db.commit()
        return True
    
    def __summon_token(self,name:str,ip_address:str,cs:Cursor):
        token=os.urandom(10).hex()
        if name not in self.cache["administs"]:
            self.cache["administs"][name]={
                "tokens":{token:ip_address}
            }
        self.cache["administs"][name]["tokens"][token]=ip_address
        if(len(self.cache["administs"])>50):
            self.cache["administs"].popitem(last=False)
        if(len(self.cache["administs"][name]["tokens"])>5):
            self.cache["administs"][name]["tokens"].popitem(last=False)
        temp=""
        for i in self.cache["administs"][name]["tokens"]:
            temp+=f"{i}:{self.cache['administs'][name]['tokens'][i]};"
        cs.execute("update admin set tokens=? where admin_name=?",(temp,name))
        return token
    
    def summon_token(self,name:str,ip_address:str)->str:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            res=self.__summon_token(name,ip_address,cs)
            db.commit()
            return res

    def get_tokens(self,name:str)->str:
        if name in self.cache["administs"]:
            return self.cache["administs"][name]["tokens"]
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("select tokens from admin where admin_name=?",(name,))
            res=cs.fetchone()
            if res:
                return res[0]
            else:
                return None
    
    def check_token(self,name:str,token:str)->bool:
        if name in self.cache["administs"]:
            if token in self.cache["administs"][name]["tokens"]:
                return True
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("SELECT tokens FROM Admin WHERE admin_name=?",(name,))
            data=cs.fetchone()

            if data is None:
                return False
            tokens=data[0].split(";")
            self.cache["administs"][name]={
                "tokens":{}
            }
            for i in tokens:
                if i=="":
                    continue
                (token,ip)=i.split(":")
                self.cache["administs"][name]["tokens"][token]=ip
                if token==token:
                    return True
            return False


    def change_password(self,admin_name,pwd,ip_address:str="255.255.255.255"):
        with dbconnect(self.db) as db:
            cs=db.cursor()

            new_hashed_pwd=self.get_hash_pwd(pwd)
            token=self.__summon_token(admin_name,ip_address,cs)
            cs.execute("UPDATE Admin SET password=? WHERE admin_name=?",(new_hashed_pwd,admin_name))
            cs.execute("UPDATE Admin SET tokens=? WHERE admin_name=?", (f"{token}:{ip_address};",admin_name))

            cs.close()
            db.commit()
            res={
                "admin_name":admin_name,
                "token":token,
            }
            return (
                res
            )


    def check_pwd(self,name,pwd:str):
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("SELECT password FROM Admin WHERE admin_name=?",(name,))
            data=cs.fetchone()
            cs.close()
            if(data==None):
                return (None)
            _password=data[0]
            if(check_password_hash(_password,self.get_custuom_encrypt_pwd(pwd))):
                return True
            else:
                return False

    def login(self,name:str,password:str,ip:str)->dict:
        with dbconnect(self.db) as db:
            cs=db.cursor()
            cs.execute("SELECT password FROM Admin WHERE admin_name=?",(name,))
            data=cs.fetchone()
            if(data==None):
                return (None)
            _password=data[0]
            if(check_password_hash(_password,self.get_custuom_encrypt_pwd(password))):
                login_time=time.time()
                self._insert_login_log(cs,name,login_time,ip)
                token=self.__summon_token(name,ip,cs)
                cs.close()
                db.commit()
                res={
                    "admin_name":name,
                    "token":token,
                }
                return (
                    res
                )
            else:
                return (None)

    
    def check_longin(self,cookie:dict):
        if cookie==None:
            return False
        admin_name,token= cookie.get("admin_name"),cookie.get("token")
        if( not (admin_name and token)):
            return False
        if(self.check_token(admin_name, token)):
            return True





