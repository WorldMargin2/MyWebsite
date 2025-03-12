from .manageDatabase import *
import json
class Version:
    ver="1.0"
    def check_version(self):
        ver:tuple
        with dbconnect(USERDB) as db:
            cs:Cursor=db.cursor()
            cs.execute("SELECT version FROM config")
            ver=cs.fetchone()
            if(not ver):
                cs.execute("insert into config(version) values(?)",(ver,))
            else:
                if(ver[0]!=self.ver):
                    cs.execute("UPDATE config SET version=?",(self.ver,))
        if((not ver)or(ver[0]!=self.ver)):
            self.update()


    def __init__(self,userdb:UserDB,articledb:ArticleDB):
        self.userdb=userdb
        self.articledb=articledb
        if(not os.path.exists(UPDATEPATH)):
            os.mkdir(UPDATEPATH)
        self.check_version()

    def update(self):
        "update mainifest of articles"
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





