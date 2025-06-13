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
├─createArticle
├─database
│  └─update
├─importLib
├─webfile
   ├─ARTICLES
   │  ├─PREUPLOAD
   │  └─UPLOADED
   ├─CSS
   ├─HTML
   ├─ICON
   ├─JS
   ├─LICENSES
   └─templates
       ├─admin
       ├─article
       └─index

```
## files

```
MYWEBSITE
│  .gitattributes
│  .gitignore
│  choose.txt
│  index.html
│  LICENSE
│  main.py
│  README.md
│  severBase.py
│
├─createArticle
│  │  createArticle.py
├─database
│  │  Admin.db
│  │  article.db
│  │
│  └─update
├─importLib
│  │  const_path.py
│  │  forms.py
│  │  handlers.py
│  │  manageDatabase.py
│  │  version_update.py
│
├─webfile
  ├─ARTICLES
  │  ├─PREUPLOAD
  │  │      .keep
  │  │
  │  └─UPLOADED
  │      │  .keep
  │      
  │
  ├─CSS
  │      --scroll-bar.css
  │      articles.css
  │      clock.css
  │      footer.css
  │      github-markdown.css
  │      header.css
  │      index-maincontent.css
  │      index.css
  │      licenses.css
  │      login.css
  │      markdown.css
  │      markdown_css.css
  │      mdmdt.css
  │      push_article.css
  │      render_article.css
  │      requireSubmit.css
  │
  ├─HTML
  ├─ICON
  │      emblem.png
  │      github.png
  │      head_image.jpg
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
  │      markdown_css.license
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
      │  requireSubmit.html
      │  secret.html
      │
      ├─admin
      │      admin-account-manage.html
      │      admin-logout.html
      │      admin.html
      │      edit_account.html
      │      login.html
      │
      ├─article
      │      articles.html
      │      delete_article.html
      │      edit_article.html
      │      edit_preupload_article.html
      │      manage_article.html
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
