from enum import unique
import re
from flask import Flask, render_template, request, redirect, url_for
from flask.scaffold import F
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import backref
from sqlalchemy.sql import select
import json
app = Flask(__name__)
engine = create_engine('sqlite:///:memory:', echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    passw = db.Column(db.String(20))
    tasks=db.relationship('Task',backref='author',lazy=True)
    links=db.relationship('Link',backref='author',lazy=True)
    def __repr__(self) -> str:
        return f"{self.user} - {self.passw}"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50))
    user_id=db.Column(db.Integer,db.ForeignKey('todo.id'),nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.task}"


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(200))
    title = db.Column(db.String(50))
    user_id=db.Column(db.Integer,db.ForeignKey('todo.id'),nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"
    
class index():
    def set(self,ind):
        self.ind=ind
    def get(self):
        return self.ind
pa=index()
pa.set(0)
@app.route("/")
def home():
    if(pa.get()!=0):
        return redirect('/me')
    return render_template("index.html")

@app.route("/signup")
def home10():
    if(pa.get()!=0):
        return redirect('/me')
    return render_template("signup.html")
@app.route("/exit")
def home3():
    pa.set(0)
    return render_template("index.html")
@app.route("/delete/<int:id>")
def delete2(id):
    if(pa.get()==0):
        return redirect('/')
    task=Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect('/me')
@app.route("/delete3/<int:id>")
def delete3(id):
    if(pa.get()==0):
        return redirect('/')
    link=Link.query.filter_by(id=id).first()
    db.session.delete(link)
    db.session.commit()
    return redirect('/me')
@app.route("/sudhir1",methods=['GET','POST'])
def home2():
    if(request.method=='POST'):
        user=(request.form['user'])
        passw=(request.form['passw'])
        find=False
        alltodo=Todo.query.all()
        i=0
        for use in alltodo:
            if use.user==user:
                if use.passw==passw:
                    find=True
                    pa.set(use.id)
                    print("find")
                else:
                    return render_template("index.html")
                break
            i+=1
        if find==False:
            return redirect('./signup')
        else:
            ind=i
    
        
        alltodo=Todo.query.all()
        alltodo=alltodo[pa.get()-1]
        return render_template("sudhir1.html",alltodo=alltodo)
    else:
        return redirect('/')
@app.route("/signed",methods=['GET','POST'])
def home11():
    if(request.method=='POST'):
        user=(request.form['user'])
        passw=(request.form['passw'])
        find=False
        alltodo=Todo.query.all()
        i=0
        for use in alltodo:
            if use.user==user:
                if use.passw==passw:
                    find=True
                    pa.set(use.id)
                    print("find")
                else:
                    return render_template("signup.html")
                break
            i+=1
        if find==False:
            ind=i+1
            ele=Todo(user=user, passw=passw)
            db.session.add(ele)
            db.session.commit()
            for use in alltodo:
                if use.user==user:
                    pa.set(use.id)
                    break
        
    
        
        alltodo=Todo.query.all()
        alltodo=alltodo[pa.get()-1]
        return render_template("sudhir1.html",alltodo=alltodo)
    else:
        return redirect('/')
@app.route("/anshu1",methods=['GET','POST'])
def link2():
    if(pa.get()==0):
        return redirect('/')
    if(request.method=='POST'):
        link=(request.form['addlink'])
        title=(request.form['addtitle'])
        alltodo=Todo.query.all()
        find=False
        for use in alltodo[pa.get()-1].links:
            if use.link==link:
                find=True
                print("find link")
                break
        if find==False:
            link1=Link(link=link,title=title,user_id=(alltodo[pa.get()-1]).id)
            db.session.add(link1)
            db.session.commit()
    alltodo=Todo.query.all()
    alltodo=alltodo[pa.get()-1]
    return render_template("sudhir1.html",alltodo=alltodo)

@app.route("/me",methods=['GET','POST'])
def home9():
    if(pa.get()==0):
        return redirect('/')
    if(request.method=='POST'):
        taski=(request.form['addtask'])
        alltodo=Todo.query.all()
        find=False
        for use in alltodo[pa.get()-1].tasks:
            if use.task==taski:
                find=True
                print("find task")
                break
        if find==False:
            post1=Task(task=taski,user_id=(alltodo[pa.get()-1]).id)
            db.session.add(post1)
            db.session.commit()
    alltodo=Todo.query.all()
    alltodo=alltodo[pa.get()-1]
    return render_template("sudhir1.html",alltodo=alltodo)

@app.route("/jotting")
def home8():
    if(pa.get()==0):
        return redirect('/')
    return render_template("jotting.html")  
@app.route("/texteditor")
def home4():
    if(pa.get()==0):
        return redirect('/')
    return render_template("texteditor.html") 

@app.route("/about")
def home5():
    if(pa.get()==0):
        return redirect('/')
    return render_template("about.html") 

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
