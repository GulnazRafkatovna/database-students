from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjgchfdxlkjhjg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'students217.db'
db=SQLAlchemy(app)

class students217(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    patronym = db.Column(db.String(80))
    group = db.Column(db.String(80))

    def __repr__(self):
        return '<students217 %r>' % self.id


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route("/add", methods=['GET', 'POST'])
def add():
    lastname=request.form.get('LASTNAME')
    firstname=request.form.get('FIRSTNAME')
    patronym=request.form.get('PATRONYM')
    group=request.form.get('GROUP')

    studentrecord=students217(lastname=lastname, firstname=firstname, patronym=patronym, group=group)
    db.session.add(studentrecord) #запрос на добавление новой записи в нашу БД
    db.session.commit() #подтверждение

    sl=students217.query.all()
    return render_template('studentslist.html',sl=sl)

@app.route("/view")
def view():
    studentlist=students217.query.order_by(students217.id)
    return render_template('view.html', studentlist=studentlist)

@app.route("/studentslist.html", methods=['POST', 'GET'])
def studentslist():
    sl=students217.query.all()
    return render_template('studentslist.html',sl=sl)

@app.route("/info/<student_id>", methods=['POST', 'GET'])
def info(student_id):
    student=students217.query.filter_by(id=student_id).first()
    return render_template('info.html', student=student)

if __name__ == "__main__":
    app.run(debug=True)
