from flask import Flask, request, render_template
import os
import traceback
from flask_sqlalchemy import SQLAlchemy
import werkzeug.exceptions

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
    for key, value in request.form.items():
        if key.startswith('privileges_'):
            last_name = key[len('privileges_'):]
            personnel = ITPersonnel.query.get(last_name)
            if personnel:
                personnel.Database_Privileges = value
    db.session.commit()
    return 'Rights assigned successfully'

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, werkzeug.exceptions.HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    app.logger.error(f"Error occurred: {e}\n{traceback.format_exc()}")
    return "An error occurred", 500

if __name__ == '__main__':
    app.debug = True
    port = 5000  # Define the port variable
    app.run(host='0.0.0.0', port=port)