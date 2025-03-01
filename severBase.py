from functools import wraps
from flask import Flask,jsonify,render_template,redirect
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


@wraps
def checkLogin(func):  # 装饰器，用于检查用户是否登录,使用cookie
    @wraps(func)
    def wrapper(*args, **kwargs):
        pass
        
def readFile(file_path):
    with open(file_path,"rb") as file:
        return(file.read())

class Sever:
    def __init__(self):
        self.app=Flask(__name__,template_folder=f"{WEBFILEPATH}templates")
        self.app.config["SECRET_KEY"]="SOCITY"
        self.csrf=CSRFProtect(self.app)
        self.userDB=UserDB()
        self.getStatic()
        self.handle_event()
        self.main()
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

    def main(self):

        @self.app.route("/")
        def main():
            return(render_template("index.html"))
        
        #get license
        @self.app.route("/licenses")
        def getLICENSESLIST():
            licenses=[]
            keys=("name","type","url")
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
        
        @self.app.route("/article")
        def getArticlePage():
            return(render_template("article.html"))
        
        @self.app.route("/admin",methods=["GET","POST"])
        def admin():
            #要注意token
            form=AdminLoginForm()
            if(form.validate_on_submit()):
                if(self.userDB.login(form.admin_name.data,form.password.data)):
                    return(redirect("/"))
                else:
                    return(render_template("login.html",form=form,login_errors=["用户名或密码错误"]))
            return(render_template("login.html",form=form))
        
        @self.check_login
        @self.app.route("/admin/logout")
        def logout():
            self.userDB.logout(request.cookies)
            return(redirect("/admin"))
            


    def handle_event(self):
        @wraps
        def check_login(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if(self.userDB.check_longin(request.cookies)):
                    return(f(*args, **kwargs))
                else:
                    return(redirect("/admin"))
            return(decorated_function)
        self.check_login=check_login
    

        
        


        

