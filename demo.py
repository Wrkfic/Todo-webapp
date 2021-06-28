from datetime import datetime
from sys import meta_path
from flask import Flask, render_template, request, redirect, flash
from flask.helpers import flash
from flask.templating import render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)
app.secret_key = 'random string'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
@app.route('/', methods=['GET', 'POST'])
def Index():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title)==0:
            flash("Please fill above field!")
        else:
            todo = ToDo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()

    alltodo = ToDo.query.all()
    return render_template('Index.html', alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title)==0:
            flash("Please update above field!")
        else:
            todo = ToDo.query.filter_by(sno=sno).first()
            todo.title = title
            todo.desc = desc
            db.session.add(todo)
            db.session.commit()
            return redirect('/')

    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/About')
def about():
    return render_template('About.html')

if __name__=='__main__':
    app.run(debug=True)