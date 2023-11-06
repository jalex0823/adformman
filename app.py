from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sqltps1:Disneychannel911!@sql01-tps-dev-scus.database.windows.net:1433/tps_aggroupdb'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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
def index():
    personnel = ITPersonnel.query.all()
    departments = ITDepartments.query.all()
    return render_template('index.html', personnel=personnel, departments=departments)

@app.route('/assign-rights', methods=['POST'])
def assign_rights():
    # Extract form data
    form_data = request.form

    # For each person in the form data
    for key, value in form_data.items():
        if key.startswith('privileges_'):
            # Get the person's last name from the key
            last_name = key[len('privileges_'):]

            # Get the person's record
            personnel = ITPersonnel.query.filter_by(Last_Name=last_name).first()

            if personnel:
                # Update the person's database privileges
                personnel.Database_Privileges = value

                # Update the person's remarks
                remarks_key = 'remarks_' + last_name
                if remarks_key in form_data:
                    personnel.Remarks = form_data[remarks_key]

    # Commit the changes to the database
    db.session.commit()

    return 'Rights assigned successfully'

if __name__ == "__main__":
    app.run(port=5001, debug=True)