import os

import pandas as pd
from flask import Flask, render_template, request, url_for

import classify

app = Flask(__name__)



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')
    
@app.route('/productpage')
def productpage():
    bill=classify.runprg()
    df=pd.read_csv('bill.csv')
    df.to_csv('bill.csv',index=None)
    data=pd.read_csv('bill.csv')
    file = 'bill.csv'
    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
    return render_template('productpage.html',tables=[data.to_html()],titles=[''])


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/Admin_login')
def Admin_login():
    return render_template('Admin_login.html') 

if __name__ == "__main__":
    app.run(debug=True)

