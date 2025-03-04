from functools import wraps
from flask import Flask,jsonify,render_template,redirect,make_response, send_from_directory
from flask import request, session,url_for,abort,send_file,flash,get_flashed_messages
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from importLib.manageDatabase import *
from importLib.forms import *
import zipfile

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


        
def readFile(file_path):
    with open(file_path,"rb") as file:
        return(file.read())

class Sever:
    def __init__(self):
        self.app=Flask(__name__,template_folder=f"{WEBFILEPATH}templates")
        self.app.config["SECRET_KEY"]="SOCITY"
        self.csrf=CSRFProtect(self.app)
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
            # return(render_template("readLicense.html",license_text=open(f"{LICENSESPATH}{filename}","r").read()))
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
            return(render_template("404.html", errors=errs, redirect=redirect))

        @self.app.route("/")
        def main():
            return(render_template("index.html"))

        @self.app.route("/admin")
        @self.checklogin
        def getAdminPage():
            return(
                render_template(
                    "admin.html",
                    admin_name=request.cookies.get("admin_name")
                )
            )

    def admin_url(self):    
        @self.app.route("/admin/logout", methods=["POST","GET"])
        @self.checklogin
        def admin_logout():
            form=AdminLogoutForm()
            if(request.method=="GET"):
                return(render_template("admin-logout.html", form=form))
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
                        print(key, value)
                        response.set_cookie(key, value, max_age=60 * 60 * 24 * 7)
                    return response
                else:
                    errors.append("用户名或密码错误")
            return render_template("login.html", form=form, errors=errors)


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
        @self.app.route("/admin/push_article")
        @self.checklogin
        def push_article():
            article_id:int=0
            form = PushArticleForm()
            if(request.method=="GET"):
                pass
            else:
                if (form.validate_on_submit()):
                    article=dict()
                    article["title"]=form.title.data
                    article["upload_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    article["topest"]=form.topest.data
                    article["publish_now"]=form.publish_now.data
                    zip_file=form.zipfile.data
                    file_name=secure_filename(zip_file.filename)
                    article["folder"]=file_name
                    file_path=os.path.join(PREUPLOADPATH+file_name)
                    zip_file.save(file_path)
                    if(form.publish_now.data):
                        article_id=self.articleDB.publishArticle(article)
                        if(zipfile.is_zipfile(file_path)):
                            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                                zip_ref.extractall(os.path.abspath(file_path))
                        return(redirect(f"/article/{article_id}"))
                    else:
                        article_id=self.articleDB.preuploadArticle(article)
            return(render_template("push_article.html"))


        @self.app.route("/admin/delete_preupload_article/<id>")
        @self.checklogin
        def delete_preupload_article(id:int):
            self.articleDB.delete_preuploadArticle(id)
            return(redirect("/admin/article"))

        @self.app.route("/admin/delete_article/<id>")
        @self.checklogin
        def delete_article(id:int):
            folder=self.articleDB.getArticleFolderFromId(id)
            self.articleDB.deleteArticle(id)
            os.remove(PREUPLOADPATH+folder)
            return(redirect("/admin/article"))


        @self.app.route("/article")
        def getArticlesPage():
            return(render_template("article.html"))
        
        @self.app.route("/article/<id>/<file_name>")
        def getArticle(id:int,file_name:str):
            return(send_from_directory(f"{ARTICLEPATH}{self.articleDB.getArticleFolderFromId(id)}",file_name))

        @self.app.route("/article/<id>")
        @self.checklogin
        def getArticlePage(id:int):
            return(render_template("article.html",id=id))







