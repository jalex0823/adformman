from flask import Flask, request, render_template, session
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class ITDepartments(db.Model):
    __tablename__ = 'ITDepartments'
    Department = db.Column(db.String(255), primary_key=True)
    Responsibilities = db.Column(db.String(255), nullable=False)
    Assumed_Database_Access = db.Column(db.String(255), nullable=False)
    Remarks = db.Column(db.String(255), nullable=True)
    AG_ID = db.Column(db.String(255), nullable=True)

class ITPersonnel(db.Model):
    __tablename__ = 'ITPersonnel'
    Last_Name = db.Column(db.String(255), primary_key=True)
    First_Name = db.Column(db.String(255), nullable=False)
    Position = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    Database_Privileges = db.Column('Database Privileges', db.String(255), nullable=True)
    Remarks = db.Column(db.String(255), nullable=True)

@app.route('/')
def home():
    personnel = ITPersonnel.query.all()
    departments = ITDepartments.query.all()
    return render_template('index.html', personnel=personnel, departments=departments)

@app.route('/assign-rights', methods=['POST'])
def assign_rights():
    user = request.form.get('user')  # Get the user from the form
    timestamp = datetime.now()  # Get the current timestamp

    for person in ITPersonnel.query.all():
        last_name = person.Last_Name
        privileges = request.form.get(f'privileges_{last_name}')
        remarks = request.form.get(f'remarks_{last_name}')
        if privileges: person.Database_Privileges = privileges
        if remarks:
            person.Remarks = remarks
    db.session.commit()

    print(f'Form submitted by {user} at {timestamp}')  # Print the user and timestamp

    return 'Rights assigned successfully'

if __name__ == '__main__':
    app.run(debug=True)