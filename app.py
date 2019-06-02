from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if(request.method == 'POST'):
        taskConetent = request.form['content']
        newTask = Todo(content=taskConetent)
        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong'
    else:
        tasks = Todo.query.order_by(Todo.created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    taskToDelete = Todo.query.get_or_404(id)
    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Something went wrong'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
