from flask import Flask, request, render_template, session
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

# Your model definitions go here

@app.route('/')
def home():
    # Your home route code goes here

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

    # Send email
    msg = MIMEMultipart()
    msg['From'] = 'jalex0823@gmail.com'
    msg['To'] = 'jefferya@texaspipe.com'
    msg['Subject'] = 'Information Submitted to AD Databases'
    body = f'The user {user} has submitted information to the AD Databases at {timestamp}.'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('jalex0823@gmail.com', 'Disneychannel911!')
    text = msg.as_string()
    server.sendmail('jalex0823@gmail.com', 'jefferya@texaspipe.com', text)
    server.quit()

    return 'Rights assigned successfully'

if __name__ == '__main__':
    app.run(debug=True)