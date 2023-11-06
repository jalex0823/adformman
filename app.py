from flask import request

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