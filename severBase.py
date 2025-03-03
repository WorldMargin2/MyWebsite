from functools import wraps
from flask import Flask,jsonify,render_template,redirect,make_response
from flask import request, session,url_for,abort,send_file,flash,get_flashed_messages
from flask_wtf.csrf import CSRFProtect
from importLib.manageDatabase import *
from importLib.forms import *

WEBFILEPATH="./webfile/"
JSPATH=f"{WEBFILEPATH}JS/"
CSSPATH=f"{WEBFILEPATH}CSS/"
ICONPATH=f"{WEBFILEPATH}ICON/"
IMAGEPATH=f"{WEBFILEPATH}images/"
DATABASEPATH="./database/"
HTMLPATH=f"{WEBFILEPATH}HTML/"
LICENSESPATH=f"{WEBFILEPATH}LICENSES/"
ARTICLEPATH=f"{WEBFILEPATH}ARTICLES/"


        
def readFile(file_path):
    with open(file_path,"rb") as file:
        return(file.read())

class Sever:
    def __init__(self):
        self.app=Flask(__name__,template_folder=f"{WEBFILEPATH}templates")
        self.app.config["SECRET_KEY"]="SOCITY"
        self.csrf=CSRFProtect(self.app)
        self.userDB=UserDB()
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
        def notFound():
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
        @self.app.route("/article")
        def getArticlePage():
            return(render_template("article.html"))






