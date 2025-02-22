# MyWebsite
 
 this is a personal website setup by flask.
 the "index.html" in root is only redirect to "index.html" in "templates" folder.
 the project is based on "https://github.com/WorldMargin2/flaskSeverBase"

## Description

here are some exciting features of this project:

- [] clock
- [] the text have a transition effect when you visit the website.from transparent to opaque and 3D rotate,and translate up
  
- [] a trapezoid moves into the screen from the right side
- [] the text will move to top-left and scale down when you scroll down,and the clock will move to top-right and scale down when you scroll down .

## Project Structure

```
<!-- webfile/(HTML,CSS/(clock.css,index.css),JS/(clock.js,index.js),templates/(index.html),ICON) -->
MyWebsite
├── severBase.py
├── main.py
└── webfile
    ├── HTML
    │   ├── clock.html
    │   └── index.html
    ├── CSS
    │   ├── clock.css
    │   └── index.css
    ├── JS
    │   ├── clock.js
    │   └── index.js
    ├── templates
    │   └── index.html
    └── ICON
```


## Usage

1. install flask
2. install flask-wtf
