from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sqltps1:Disneychannel911!@sql01-tps-dev-scus.database.windows.net/tps_aggroupdb'
db = SQLAlchemy(app)

class Personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    role = db.Column(db.String(50))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/personnel')
def personnel():
    personnel = Personnel.query.all()
    return render_template('personnel.html', personnel=personnel)

@app.route('/update_role', methods=['POST'])
def update_role():
    personnel_id = request.form.get('personnel_id')
    new_role = request.form.get('new_role')
    personnel = Personnel.query.get(personnel_id)
    personnel.role = new_role
    db.session.commit()
    return redirect(url_for('personnel'))

if __name__ == '__main__':
    app.run(debug=True)