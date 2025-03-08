from functools import wraps
from flask import Flask,jsonify,render_template,redirect,make_response, send_from_directory
from flask import request, session,url_for,abort,send_file,flash,get_flashed_messages
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from importLib.manageDatabase import *
from importLib.forms import *
import zipfile
import json

WEBFILEPATH="./webfile/"
JSPATH=f"{WEBFILEPATH}JS/"
CSSPATH=f"{WEBFILEPATH}CSS/"
ICONPATH=f"{WEBFILEPATH}ICON/"
IMAGEPATH=f"{WEBFILEPATH}images/"
DATABASEPATH="./database/"
HTMLPATH=f"{WEBFILEPATH}HTML/"
LICENSESPATH=f"{WEBFILEPATH}LICENSES/"
ARTICLEPATH=f"{WEBFILEPATH}ARTICLES/"
UPLOADEDARTICLEPATH=f"{ARTICLEPATH}UPLOADED/"
PREUPLOADPATH=f"{ARTICLEPATH}PREUPLOAD/"



def init_folder():
    if not os.path.exists(DATABASEPATH):
        os.mkdir(DATABASEPATH)
    if not os.path.exists(ARTICLEPATH):
        os.mkdir(ARTICLEPATH)
    if not os.path.exists(UPLOADEDARTICLEPATH):
        os.mkdir(UPLOADEDARTICLEPATH)
    if not os.path.exists(PREUPLOADPATH):
        os.mkdir(PREUPLOADPATH)
        
def readFile(file_path):
    with open(file_path,"rb") as file:
        return(file.read())

class Sever:
    def __init__(self):
        self.app=Flask(__name__,template_folder=f"{WEBFILEPATH}templates")
        self.app.config["SECRET_KEY"]="SOCITY"
        self.csrf=CSRFProtect(self.app)
        init_folder()
        self.userDB=UserDB()
        self.articleDB=ArticleDB()
        self.handle_event()
        self.getStatic()
        self.main()
        self.article_url()
        self.admin_url()
        self.start()
        
    
    def start(self):
        self.app.run("0.0.0.0",80,debug=True)


    def getStatic(self):
        @self.app.route("/favicon.ico")
        def getfavicon():
            return(readFile(f"{ICONPATH}WorldMargin.ico"))

        @self.app.route("/WebFile/JS/<filename>")
        @self.app.route("/JS/<filename>")
        def getJS(filename):
            return(readFile(f"{JSPATH}{filename}"))
        
        @self.app.route("/WebFile/CSS/<filename>")
        @self.app.route("/CSS/<filename>")
        def getCSS(filename):
            return(readFile(f"{CSSPATH}{filename}"))
        
        @self.app.route("/WebFile/IMAGE/<filename>")
        @self.app.route("/IMAGE/<filename>")
        def getIMAGE(filename):
            return(readFile(f"{IMAGEPATH}{filename}"))
        
        @self.app.route("/WebFile/ICON/<filename>")
        @self.app.route("/ICON/<filename>")
        def getICON(filename):
            return(readFile(f"{ICONPATH}{filename}"))
        
        @self.app.route("/WebFile/HTML/<filename>")
        @self.app.route("/HTML/<filename>")
        def getHTML(filename):
            return(readFile(f"{HTMLPATH}{filename}"))
        
        @self.app.route("/WebFile/LICENSES/<filename>")
        @self.app.route("/LICENSES/<filename>")
        def getLICENSES(filename):
            return(render_template("readLicense.html",license_text=open(f"{LICENSESPATH}{filename}","r").read()))
        
        @self.app.route("/WebFile/LICENSES/<filename>/download")
        @self.app.route("/LICENSES/<filename>/download")
        def downloadLICENSES(filename):
            return(open(f"{LICENSESPATH}{filename}","r").read())        
        
        @self.app.route("/licenses")
        def getLICENSESLIST():
            licenses=[]
            keys=("name","type","url","open_source_url")
            with open(f"{LICENSESPATH}licenses.list") as file:
                for i in file.readlines():
                    i=i.strip("\n")
                    if(not i.startswith("#")and(i!="")):
                        licenses.append(
                            dict(zip(
                                keys,tuple(i.split("===="))
                            ))
                        )
            return(render_template("licenses.html",licenses=licenses))

    def main(self):

        @self.app.errorhandler(404)
        @self.app.route("/404")
        def notFound(error=None):
            errs=request.args.get("error","")
            redirect=request.args.get("redirect","/")
            if(errs==""):
                errs=["404 Not Found"]
            else:
                errs=errs.split("|")
            if(error):
                errs.append(error)
            return(render_template("404.html", errors=errs, redirect=redirect))

        @self.app.route("/")
        def main():
            return(render_template("index/index.html"))

        @self.app.route("/admin")
        @self.checklogin
        def getAdminPage():
            return(
                render_template(
                    "admin/admin.html",
                    admin_name=request.cookies.get("admin_name")
                )
            )

    def admin_url(self):    
        @self.app.route("/admin/logout", methods=["POST","GET"])
        @self.checklogin
        def admin_logout():
            form=AdminLogoutForm()
            if(request.method=="GET"):
                return(render_template("admin/admin-logout.html", form=form))
            if(form.validate_on_submit()):
                response = make_response(redirect("/admin/login"))
                for i in self.userDB.clear_refuse():
                    response.set_cookie(i[0], "", expires=0)
                response.set_cookie("admin_name", "", expires=0)
                response.set_cookie(self.userDB.get_config("password_key"), "", expires=0)
                return response
            return(redirect("/404",error="表单验证失败"))
            
        
        @self.app.route("/admin/login",methods=["GET","POST"])
        def admin_login():
            if(self.userDB.check_longin(request.cookies)):
                return(redirect("/admin"))
            errors = []
            err=request.args.get("error")
            if err:
                errors.append(err)
            form = AdminLoginForm()
            if form.validate_on_submit():
                login_result = self.userDB.login(form.admin_name.data, form.password.data, request.remote_addr)
                if login_result:
                    response = make_response(redirect("/admin"))
                    for key, value in login_result.items():
                        response.set_cookie(key, value, max_age=60 * 60 * 24 * 7)
                    return response
                else:
                    errors.append("用户名或密码错误")
            return render_template("admin/login.html", form=form, errors=errors)

        @self.app.route("/admin/edit_account",methods=["GET","POST"])
        @self.checklogin
        def edit_account():
            name_form=AdminNameEditForm()
            pwd_form=AdminPasswordEditForm()
            name_errs=[]
            pwd_errs=[]
            if(request.method=="GET"):
                return(render_template("admin/edit_account.html",name_form=name_form,pwd_form=pwd_form))
            else:
                origin_name=request.cookies.get("admin_name")
                if(name_form.validate_on_submit()):
                    self.userDB.change_name(origin_name,name_form.data)
                    response=make_response(redirect("/admin"))
                    response.set_cookie("admin_name",name_form.data,max_age=60 * 60 * 24 * 7)
                    return(response)
                elif(pwd_form.validate_on_submit()):
                    if(self.userDB.check_pwd(origin_name,pwd_form.origin_password.data)):
                        response=make_response(redirect("/admin"))
                        for i in self.userDB.clear_refuse():
                            response.set_cookie(i[0], "", expires=0)
                        res=self.userDB.change_password(origin_name,pwd_form.password.data)
                        for i in res.items():
                            response.set_cookie(i[0], i[1], max_age=60 * 60 * 24 * 7)
                        return(response)
                return(render_template("admin/edit_name_pwd.html",name_form=name_form,pwd_form=pwd_form,name_errs=name_errs,pwd_errs=pwd_errs))




    def redirect_404(self,error=None):
        return(redirect(url_for("notFound",error=error)))

    def handle_event(self):
        def checklogin_decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if(self.userDB.check_longin(request.cookies)):
                    return(f(*args, **kwargs))
                else:
                    return(redirect(url_for("admin_login",error="未登录")))
            return(decorated_function)
        self.checklogin=checklogin_decorator



    def article_url(self):
        # admin required
        @self.app.route("/admin/push_article",methods=["GET","POST"])
        @self.checklogin
        def push_article():
            article_id:int=0
            form = PushArticleForm()
            if(request.method=="GET"):
                return(render_template("article/push_article.html",form=form))
            else:
                if (form.validate_on_submit()):
                    article=dict()
                    article["title"]=form.title.data
                    article["upload_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    article["topest"]=form.topest.data
                    article["show_weight"]=form.show_weight.data
                    article["publish_now"]=form.publish_now.data
                    article["visible"]=form.visible.data
                    zip_file=request.files["zipfile"]
                    article_id="%05d"%(self.articleDB.fetch_free_ID() or 1 ,)
                    article["id"]=article_id
                    file_path=os.path.join(PREUPLOADPATH,article_id)
                    zip_file.save(file_path)
                    if(form.publish_now.data):
                        if(zipfile.is_zipfile(file_path)):
                            extra_path=os.path.join(UPLOADEDARTICLEPATH,article_id)
                            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                                zip_ref.extractall(os.path.abspath(extra_path))
                            self.articleDB.publishArticle(article)
                            os.remove(file_path)
                            return(redirect(f"/article/{article_id}"))
                        else:
                            os.remove(file_path)
                            return(self.redirect_404(error="文件格式错误"))
                    else:
                        article_id=self.articleDB.fetch_free_ID()
                        if(zipfile.is_zipfile(file_path)):
                            pass
                        return(self.redirect_404(error="文件格式错误"))
                return(self.redirect_404(error="表单验证失败"))
            
        
        

        @self.app.route("/admin/edit_preupload_article")
        @self.checklogin
        def edit_preupload_article():
            return(render_template("article/edit_preupload_article.html"))

        @self.app.route("/admin/delete_preupload_article/<id>")
        @self.checklogin
        def delete_preupload_article(id:int):
            folder=self.articleDB.getPreuploadFolderFromId(id)
            self.articleDB.delete_preuploadArticle(id)
            os.remove(PREUPLOADPATH+folder)
            return(redirect("/admin/article"))

        @self.app.route("/admin/delete_article/<id>")
        @self.checklogin
        def delete_article(id:int):
            folder=self.articleDB.getArticleFolderFromId(id)
            self.articleDB.deleteArticle(id)
            os.remove(UPLOADEDARTICLEPATH+folder)
            return(redirect("/admin/article"))

        # normal
        @self.app.route("/article")
        def getArticlesPage(page:int=1):
            articles=self.articleDB.getArticlesInfo(page)
            for i in articles:
                i["folder"]="%05d"%(i["id"],)
                with open(os.path.join(UPLOADEDARTICLEPATH,i["folder"],"mainifest.json")) as f:
                    mainifest=json.load(f)
                    i["head_image"]=mainifest["head_image"]
                    i["short_descript"]=mainifest["short_descript"]
            return(render_template("article/article.html",articles=articles,page=page,reversed=reversed))
        
        @self.app.route("/article/<int:id>/<file_name>")
        def getArticle(id:int,file_name:str):
            id=int(id)
            article_path=self.articleDB.getArticleFolderFromId(id)
            if(not (article_path and self.articleDB.is_article_visible(id))):
                return(self.redirect_404(error="未找到该文章"))
            return(open(f"{UPLOADEDARTICLEPATH}{article_path}/{file_name}","rb").read())

        @self.app.route("/article/<int:id>")
        def getArticlePage(id:int):
            id=int(id)
            article_path=self.articleDB.getArticleFolderFromId(id)
            article_info=self.articleDB.getArticleFromId(id)
            with open(os.path.join(UPLOADEDARTICLEPATH,article_path,"main.html"),"r",encoding="GBK") as file:
                main_content=file.read()
            if(not (article_path and self.articleDB.is_article_visible(id))):
                return(self.redirect_404(error="未找到该文章"))
            return(render_template("article/render_article.html",article_info=article_info,main_content=main_content,article_path=article_path))







