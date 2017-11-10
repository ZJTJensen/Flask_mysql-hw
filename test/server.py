# from __future__ import print_function
# import sys
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    print "hello"
    # print ("hello", file=sys.stderr)
    return render_template("index.html")
app.run(debug=True)