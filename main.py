from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretcode"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"

db = SQLAlchemy()
db.init_app(app)

class Todos(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"<Task {self.task}>"


with app.app_context():
    db.create_all()

class Form(FlaskForm):
    todo = StringField("To-do")
    submit = SubmitField("Create")

@app.route('/create')
def create_todo():
    form = Form()
    return render_template("form.html", form=form)

@app.route('/')
def home():
    result = db.session.execute(db.select(Todos))
    todos = result.scalars()
    return render_template("index.html", all_todos=todos)

if __name__ == "__main__":
    app.run(debug=True)