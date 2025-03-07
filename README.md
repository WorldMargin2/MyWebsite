# MyWebsite

 this is a personal website setup by flask.
 the "index.html" in root is only redirect to "index.html" in "templates" folder.
 the project is based on "https://github.com/WorldMargin2/flaskSeverBase"

## Description

here are some exciting features of this project:

- [x] clock
- [x] the text have a transition effect when you visit the website.from transparent to opaque and 3D rotate,and translate up
- [x] a trapezoid moves into the screen from the right side
- [x] the text will move to top-left and scale down when you scroll down,and the clock will move to top-right and scale down when you scroll down .

## Project Structure

```
MYWEBSITE
│  index.html
│  LICENSE
│  main.py
│  README.md
│  severBase.py
│
├─database
│      
│      
│
├─importLib
│     forms.py
│     manageDatabase.py
│  
│
└─webfile
   ├─ARTICLES
   │  ├─PREUPLOAD
   │  │      
   │  │
   │  └─UPLOADED
   │
   ├─CSS
   │      --scroll-bar.css
   │      clock.css
   │      footer.css
   │      github-markdown.css
   │      header.css
   │      index-maincontent.css
   │      index.css
   │      licenses.css
   │      login.css
   │      markdown.css
   │      mdmdt.css
   │      render_article.css
   │
   ├─HTML
   ├─ICON
   │      github.png
   │      WorldMargin.ico
   │      WorldMargin.png
   │      WorldMargin.svg
   │
   ├─JS
   │      clipboard.js
   │      clock.js
   │      extend-marked.js
   │      firework-init.js
   │      firework.js
   │      index.js
   │      jquery-ui.js
   │      jquery.js
   │      marked.min.js
   │
   ├─LICENSES
   │      clipboard.license
   │      clock-js.license
   │      firework.license
   │      flaskseverbase.license
   │      jquery-ui.license
   │      jquery.license
   │      licenses.list
   │      markdown-css.license
   │      markedjs.license
   │      mdmdt.license
   │
   └─templates
       │  404.html
       │  clock.html
       │  footer.html
       │  header.html
       │  licenses.html
       │  readLicense.html
       │
       ├─admin
       │      admin-account-manage.html
       │      admin-logout.html
       │      admin.html
       │      edit_account.html
       │      login.html
       │
       ├─article
       │      article.html
       │      edit_preupload_article.html
       │      push_article.html
       │      render_article.html
       │
       └─index
               index-main-content.html
               index.html
 

```

## Usage

1. install flask
2. install flask-wtf

# demo video

![Sample Video](https://github.com/user-attachments/assets/5705207f-ac28-4c93-8797-849c37b00f25)
<video><resource src="https://github.com/user-attachments/assets/5705207f-ac28-4c93-8797-849c37b00f25"></resource></video>
