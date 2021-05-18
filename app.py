from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/studentinformation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enroll = db.Column(db.String(100))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    address = db.Column(db.String(100))

    def __init__(self, enroll, name, email, gender, phone, address):
        self.enroll = enroll
        self.name = name
        self.email = email
        self.gender = gender
        self.phone = phone
        self.address = address


@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template("index.html", students = all_data)



@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        enroll = request.form['enroll']
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']

        my_data = Data(enroll, name, email, gender, phone, address)
        db.session.add(my_data)
        db.session.commit()

        flash("Student Added Successfully!!!")

        return redirect(url_for('index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.enroll = request.form['enroll']
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.gender = request.form['gender']
        my_data.phone = request.form['phone']
        my_data.address = request.form['address']

        db.session.commit()
        flash("Student Information Updated Successfully!!!")

        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Information Deleted Successfully!!!")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
