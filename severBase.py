from functools import wraps
from flask import Flask,jsonify,render_template,redirect
from flask import request, session,url_for,abort,send_file,flash,get_flashed_messages
from flask_wtf.csrf import CSRFProtect

WEBFILEPATH="./webfile/"
JSPATH=f"{WEBFILEPATH}JS/"
CSSPATH=f"{WEBFILEPATH}CSS/"
ICONPATH=f"{WEBFILEPATH}ICON/"
IMAGEPATH=f"{WEBFILEPATH}images/"
DATABASEPATH="./database/"
HTMLPATH=f"{WEBFILEPATH}HTML/"


def readFile(file_path):
    with open(file_path,"rb") as file:
        return(file.read())

class Sever:
    def __init__(self):
        self.app=Flask(__name__,template_folder=f"{WEBFILEPATH}templates")
        self.app.config["SECRET_KEY"]="SOCITY"
        self.csrf=CSRFProtect(self.app)
        self.getStatic()
        self.main()
        self.start()
        
    
    def start(self):
        self.app.run("0.0.0.0",80,debug=True)


    def getStatic(self):
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
        
    def main(self):
        @self.app.route("/")
        def main():
            return(render_template("index.html"))
        

