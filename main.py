from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

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

@app.route('/create', methods=["Get", "Post"])
def create_todo():
    form = Form()
    if form.validate_on_submit():
        new_todo = Todos(
            task=form.todo.data
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("form.html", form=form)

@app.route('/')
def home():
    result = db.session.execute(db.select(Todos).order_by(Todos.id.desc()))
    todos = result.scalars()
    return render_template("index.html", all_todos=todos)

if __name__ == "__main__":
    app.run(debug=True)