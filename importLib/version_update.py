from .manageDatabase import *
import json
class Version:
    ver="1.0"
    def check_version(self):
        ver:tuple
        with dbconnect(ADMINDB) as db:
            cs:Cursor=db.cursor()
            cs.execute("SELECT config_value FROM config where config_name='version'")
            ver=cs.fetchone()
            if(not ver):
                cs.execute("INSERT INTO config (config_name, config_value) VALUES (?, ?)", ('version', self.ver))
            else:
                if(ver[0]!=self.ver):
                    cs.execute("UPDATE config SET version=?",(self.ver,))
        if((not ver)or(ver[0]!=self.ver)):
            self.update()


    def __init__(self,admindb:AdminDB,articledb:ArticleDB):
        self.admindb=admindb
        self.articledb=articledb
        if(not os.path.exists(UPDATEPATH)):
            os.mkdir(UPDATEPATH)
        self.check_version()

    def update(self):
        "update mainifest of articles"
        if(os.path.exists(f"{DATABASEPATH}user.db")):
            os.remove(f"{DATABASEPATH}user.db")
        for i in self.articledb.getAllArticles():
            folder=f"{UPLOADEDARTICLEPATH}{self.articledb.getArticleFolderFromId(i)}"
            resources=[]    #资源文件/在此次更新后每次更新文章将根据mainifest中的文件进行更新（删除更新后mainifest未带的资源文件）
            # 获取文章文件夹下的资源文件并且写入mainifest
            for j in os.listdir(folder):
                if(j!="mainifest.json"):
                    resources.append(j)
            with open(f"{folder}/mainifest.json","r+",encoding="GBK") as f:
                mainifest=json.load(f)
                mainifest["resources"]=resources
            with open(f"{folder}/mainifest.json","w",encoding="GBK") as f:
                json.dump(mainifest,f,ensure_ascii=False,indent=4)
        





