from .manageDatabase import *
import json
from .handlers import restart

class Version:
    ver="1.7"
    def check_version(self):
        ver:tuple
        with dbconnect(ADMINDB) as db:
            cs:Cursor=db.cursor()
            cs.execute("SELECT config_value FROM config where config_name='version'")
            ver=cs.fetchone()
            if(not ver):
                try:
                    succ=self.update()
                except Exception as e:
                    succ=False
                    return
                cs.execute("INSERT INTO config (config_name, config_value) VALUES (?, ?)", ('version', self.ver))
            else:
                if(ver[0]!=self.ver):
                    try:
                        succ=self.update()
                    except Exception as e:
                        succ=False
                        return
                    if(not succ):
                        cs.execute("UPDATE config SET config_value=? WHERE config_name='version'",(self.ver,))
                        cs.execute("UPDATE config SET config_value=? WHERE config_name='update_clear'",('1',))


    def __init__(self,admindb:AdminDB,articledb:ArticleDB):
        self.admindb=admindb
        self.articledb=articledb
        if(not os.path.exists(UPDATEPATH)):
            os.mkdir(UPDATEPATH)
        self.check_version()

    def update(self):
        return self.admindb.update_db()


        





