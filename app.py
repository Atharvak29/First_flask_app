from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # where our data base is located
db = SQLAlchemy(app)    #initializing database on the app


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)       #initilize an id colum in the database
    content = db.Column(db.String(200), nullable = False)           #This column will hold each task
    date_created = db.Column(db.DateTime, default = datetime.utcnow) # will store the date and time an task is created

    def __repr__(self):
        return '<task %r>' % self.id


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content = task_content)

        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding a task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() 
        return render_template('index.html', tasks = tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was an issue deleting the task"

    

if __name__ == '__main__':
    app.run(debug = True) # shows us the mistakes in the webpage