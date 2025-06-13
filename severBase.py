from functools import wraps
from flask import Flask,jsonify,render_template,redirect,make_response, send_from_directory
from flask import request, session,url_for,abort,send_file,flash,get_flashed_messages
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import base64
import zipfile
import json
from importLib.const_path import *
from importLib.manageDatabase import *
from importLib.version_update import Version
from importLib.forms import *




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
        self.adminDB=AdminDB()
        self.articleDB=ArticleDB()
        self.version=Version(self.adminDB,self.articleDB)
        self.handle_event()
        self.getStatic()
        self.main()
        self.article_url()
        self.admin_url()
        self.start()
  
    def start(self):
        self.app.run("0.0.0.0",80,debug=True,threaded=True)


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
            return(render_template("readLicense.html",license_text=open(f"{LICENSESPATH}{filename}","r",encoding="UTF-8").read()))
        
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
        @self.app.route("/admin/")
        @self.checklogin
        def getAdminPage():
            return(
                render_template(
                    "admin/admin.html",
                    admin_name=request.cookies.get("admin_name")
                )
            )
        
        @self.app.route("/secret")
        @self.app.route("/secret/")
        @self.app.route("/secret/<secret_string>")
        def getSecret(secret_string:str=None):
            # 解密sha256文字
            if(secret_string):
                try:
                    secret_string=base64.b64decode(secret_string).decode("utf-8")
                except:
                    secret_string=None
            else:
                secret_string=None
            return(render_template("secret.html",secret_string=secret_string))

        @self.app.route("/love")
        def getLove():
            if(request.args.get("content")):
                love=request.args.get("content")
                now_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                ip=request.remote_addr
                with open("choose.txt","a",encoding="utf-8") as file:
                    file.write(f"{now_time}:{love}:{ip}\n")
                return(redirect("/love"))
            else:
                with open("choose.txt","r+",encoding="utf-8") as file:
                    log=file.readlines()
                    return("<br/>".join(log))

    def admin_url(self):    
        @self.app.route("/admin/logout", methods=["POST","GET"])
        @self.checklogin
        def admin_logout():
            form=SubmitForm()
            if(request.method=="GET"):
                return(render_template("/requireSubmit.html", submit_form=form,tip="您正在执行",opration="退出登录"))
            if(form.validate_on_submit()):
                response = make_response(redirect("/admin/login"))
                for i in self.adminDB.clear_refuse():
                    response.set_cookie(i[0], "", expires=0)
                response.set_cookie("admin_name", "", expires=0)
                response.set_cookie(self.adminDB.get_config("password_key"), "", expires=0)
                return response
            return(redirect("/404",error="表单验证失败"))
            
        
        @self.app.route("/admin/login",methods=["GET","POST"])
        def admin_login():
            if(self.adminDB.check_longin(request.cookies)):
                return(redirect("/admin"))
            errors = []
            err=request.args.get("error")
            if err:
                errors.append(err)
            form = AdminLoginForm()
            if form.validate_on_submit():
                login_result = self.adminDB.login(form.admin_name.data, form.password.data, request.remote_addr)
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
                    if(name_form.admin_name.data==origin_name):
                        name_errs.append("新用户名与当前用户名相同")
                    elif(name_form.admin_name.data ==""):
                        name_errs.append("用户名不能为空")
                    elif(not validaters.change_name_validater(name_form.admin_name.data)):
                        name_errs.append("用户名不合法")
                    else:
                        response=make_response(render_template("admin/edit_account.html",name_form=name_form,pwd_form=pwd_form,name_errs=name_errs,pwd_errs=pwd_errs))
                        self.adminDB.change_name(origin_name,name_form.admin_name.data)
                        response.set_cookie("admin_name",name_form.admin_name.data,max_age=60 * 60 * 24 * 7)
                        return(response)
                    response=make_response(render_template("admin/edit_account.html",name_form=name_form,pwd_form=pwd_form,name_errs=name_errs,pwd_errs=pwd_errs))
                    return(response)
                elif(pwd_form.validate_on_submit()):
                    if(self.adminDB.check_pwd(origin_name,pwd_form.origin_password.data)):
                        if(pwd_form.password.data==pwd_form.origin_password.data):
                            pwd_errs.append("新密码与当前密码相同")
                        elif(pwd_form.password.data==""):
                            pwd_errs.append("新密码不能为空")
                        else:
                            response=make_response(render_template("admin/edit_account.html",name_form=name_form,pwd_form=pwd_form,name_errs=name_errs,pwd_errs=pwd_errs))
                            for i in self.adminDB.clear_refuse():
                                response.set_cookie(i[0], "", expires=0)
                            res=self.adminDB.change_password(origin_name,pwd_form.password.data)
                            for i in res.items():
                                response.set_cookie(i[0], i[1], max_age=60 * 60 * 24 * 7)
                                return(response)
                        response=make_response(render_template("admin/edit_account.html",name_form=name_form,pwd_form=pwd_form,name_errs=name_errs,pwd_errs=pwd_errs))
                        return(response)
                return(render_template("admin/edit_name_pwd.html",name_form=name_form,pwd_form=pwd_form,name_errs=name_errs,pwd_errs=pwd_errs))


    def redirect_404(self,error=None):
        return(redirect(url_for("notFound",error=error)))

    def handle_event(self):
        def checklogin_decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if(self.adminDB.check_longin(request.cookies)):
                    return(f(*args, **kwargs))
                else:
                    return(redirect(url_for("admin_login",error="未登录")))
            return(decorated_function)
        self.checklogin=checklogin_decorator

    def article_url(self):
        # admin required
        @self.app.route("/admin/article/push_article",methods=["GET","POST"])
        @self.checklogin
        def push_article():
            article_id:int=0
            form = PushArticleForm()
            if(request.method=="GET"):
                return(render_template("article/push_article.html",form=form))
            else:
                if (form.validate_on_submit()):
                    upload_time=time.localtime()
                    article=dict()
                    article["title"]=form.title.data
                    article["upload_time"]=time.localtime()
                    article["topest"]=form.topest.data
                    article["show_weight"]=form.show_weight.data
                    article["publish_now"]=form.publish_now.data
                    article["visible"]=form.visible.data
                    zip_file=request.files["zipfile"]
                    article_id=get_hash_code(article["upload_time"])
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
                        if(zipfile.is_zipfile(file_path)):
                            pass
                        return(self.redirect_404(error="文件格式错误"))
                return(self.redirect_404(error="表单验证失败"))
            
        @self.app.route("/admin/articles/<int:page>")
        @self.app.route("/admin/articles/")
        @self.checklogin
        def manage_articles(page=0):
            articles=self.articleDB.getArticlesInfo(page)
            for i in articles:
                i["folder"]=i["id"]
                with open(os.path.join(UPLOADEDARTICLEPATH,i["folder"],"mainifest.json"),encoding="UTF-8") as f:
                    mainifest=json.load(f)
                    i["head_image"]=mainifest["head_image"]
                    i["short_descript"]=mainifest["short_descript"]
                    i["upload_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i["upload_time"]))
            return(render_template("article/manage_article.html",articles=articles,page=page,reversed=reversed))

        @self.app.route("/admin/edit_article/<id>",methods=["GET","POST"])
        @self.checklogin
        def edit_article(id:str):
            form = EditArticleForm()
            if(request.method=="GET"):
                return(render_template("article/edit_article.html",form=form))
            else:
                if (form.validate_on_submit()):
                    if(not self.articleDB.validateArticleId(id)):
                        return(self.redirect_404(error="未找到文章"))
                    article=dict()
                    article["title"]=form.title.data
                    article["topest"]=form.topest.data
                    article["show_weight"]=form.show_weight.data
                    article["visible"]=form.visible.data
                    zip_file=request.files["zipfile"]
                    self.articleDB.editArticle(id,article=article)
                    folder=article["id"]
                    if(not folder):
                        return(self.redirect_404(error="未找到文章"))
                    if(zipfile.is_zipfile(zip_file)):
                        with open(f"{UPLOADEDARTICLEPATH}{folder}/mainifest.json","r",encoding="UTF-8") as j:
                            old_registed_files=json.load(j)
                        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                            zip_ref.extractall(os.path.abspath(UPLOADEDARTICLEPATH+folder))
                        with open(f"{UPLOADEDARTICLEPATH}{folder}/mainifest.json","w",encoding="UTF-8") as j:
                            new_registed_files=json.load(j)
                        old_registed_files=set(old_registed_files)
                        new_registed_files=set(new_registed_files)
                        for file in old_registed_files-new_registed_files:
                            os.remove(f"{UPLOADEDARTICLEPATH}{folder}/{file}")
                return(redirect("/admin/articles"))




        @self.app.route("/admin/edit_preupload_article")
        @self.checklogin
        def edit_preupload_article():
            return(render_template("article/edit_preupload_article.html"))

        @self.app.route("/admin/delete_preupload_article/<id>")
        @self.checklogin
        def delete_preupload_article(id:str):
            folder=id
            self.articleDB.delete_preuploadArticle(id)
            os.remove(PREUPLOADPATH+folder)
            return(redirect("/admin/article"))

        @self.app.route("/admin/delete_article/<id>",methods=["POST","GET"])
        @self.checklogin
        def delete_article(id:str):
            submit_form=SubmitForm()
            if(request.method=="GET"):
                return(render_template(
                    "article/delete_article.html",
                    id=id,
                    title="删除文章",
                    submit_form=submit_form,
                    tip=f"您正在执行不可逆操作",
                    opration=f"删除文章{id}。"
                ))
            else:
                if(submit_form.validate_on_submit()):
                    folder=id
                    os.remove(UPLOADEDARTICLEPATH+folder)
                    self.articleDB.deleteArticle(id)
                    return(redirect("/admin/articles"))

        # normal
        @self.app.route("/articles")
        @self.app.route("/articles/<int:page>")
        def getArticlesPage(page:int=1):
            articles=self.articleDB.getArticlesInfo(page)
            for i in articles:
                i["folder"]=i["id"]
                with open(os.path.join(UPLOADEDARTICLEPATH,i["folder"],"mainifest.json"),encoding="UTF-8") as f:
                    mainifest=json.load(f)
                    i["head_image"]=mainifest["head_image"]
                    i["short_descript"]=mainifest["short_descript"]
                    i["upload_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i["upload_time"]))
            return(render_template("article/articles.html",articles=articles,page=page,reversed=reversed))
        
        @self.app.route("/article/<id>/<file_name>")
        def getArticle(id:int,file_name:str):
            folder=id
            if(not (self.articleDB.is_article_visible(id))):
                return(self.redirect_404(error="未找到该文章"))
            return(open(f"{UPLOADEDARTICLEPATH}{folder}/{file_name}","rb").read())

        @self.app.route("/article/<id>")
        def getArticlePage(id:str):
            folder=id
            article_info=self.articleDB.getArticleFromId(id)
            if(not article_info):
                return(self.redirect_404(error="未找到该文章"))
            with open(os.path.join(UPLOADEDARTICLEPATH,folder,"main.html"),"r",encoding="UTF-8") as file:
                main_content=file.read()
            if(not (self.articleDB.is_article_visible(id))):
                return(self.redirect_404(error="未找到该文章"))
            article_info["upload_time"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(article_info["upload_time"]))
            return(render_template("article/render_article.html",article_info=article_info,main_content=main_content,article_path=folder))







