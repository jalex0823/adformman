from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pymssql
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sqltps1:Disneychannel911!@privatelink-database-windows-net:1433/tps_aggroupdb'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class ITDepartments(db.Model):
    # ... your model definition ...

class ITPersonnel(db.Model):
    # ... your model definition ...

@app.route('/')
def index():
    try:
        personnel = ITPersonnel.query.all()
        departments = ITDepartments.query.all()
        return render_template('index.html', personnel=personnel, departments=departments)
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"An error occurred: {e}", 500

@app.route('/assign-rights', methods=['POST'])
def assign_rights():
    try:
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
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"An error occurred: {e}", 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
