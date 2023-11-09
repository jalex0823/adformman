from flask import Flask, request, render_template
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
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
    try:
        personnel = ITPersonnel.query.all()
        departments = ITDepartments.query.all()
        return render_template('index.html', personnel=personnel, departments=departments)
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return "An error occurred", 500

@app.route('/assign-rights', methods=['POST'])
def assign_rights():
    try:
        for key, value in request.form.items():
            if key.startswith('privileges_'):
                last_name = key[len('privileges_'):]
                personnel = ITPersonnel.query.get(last_name)
                if personnel:
                    personnel.Database_Privileges = value
        db.session.commit()
        return 'Rights assigned successfully'
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return f"An error occurred: {str(e)}", 500
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=port)