"""
 _______       _            _     _          ______        _                 _ 
(_______)     (_)       _  (_)   | |        (____  \      (_)               | |
 _______  ____ _  ___ _| |_ _  __| |_____    ____)  ) ____ _ _____ ____   __| |
|  ___  |/ ___) |/___|_   _) |/ _  | ___ |  |  __  ( / ___) (____ |  _ \ / _  |
| |   | | |   | |___ | | |_| ( (_| | ____|  | |__)  ) |   | / ___ | | | ( (_| |
|_|   |_|_|   |_(___/   \__)_|\____|_____)  |______/|_|   |_\_____|_| |_|\____|
    
Auteur: jefferya(jefferya.pro@gmail.com) 
app.py(Ɔ) 2023
Description : Saisissez la description puis « Tab »
Créé le :  lundi 6 novembre 2023 à 7:46:44 
Dernière modification : lundi 6 novembre 2023 à 7:47:52
"""
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your-azure-sql-connection-string'
db = SQLAlchemy(app)

class ITPersonnel(db.Model):
    # Define your model with the appropriate fields

 class ITDepartments(db.Model):
    # Define your model with the appropriate fields
 
  @app.route('/')
  def index():
    personnel = ITPersonnel.query.all()
    departments = ITDepartments.query.all()
    return render_template('index.html', personnel=personnel, departments=departments)

@app.route('/assign-rights', methods=['POST'])
def assign_rights():
    # Extract data from form
    personnel_id = request.form.get('personnel')
    department_id = request.form.get('department')
    # Update database with the new rights
    # ...
    return 'Rights assigned successfully'
