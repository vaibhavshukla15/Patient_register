from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import pandas as pd
import os

app = Flask(__name__)

# Modified insert_patient function
def insert_patient(patient_data):
    try:
        # PostgreSQL connection
        conn = psycopg2.connect(
            dbname="patient_register",
            user="vaibhav",
            password="72258",
            host="localhost"
        )
        cursor = conn.cursor()

        # Insert patient details into patients table
        cursor.execute("""
            INSERT INTO patients (aadhar_number, patient_name, patient_address, doctor_name, contact_number, email, date_of_injury)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            patient_data['aadhar_number'],
            patient_data['name'],
            patient_data['address'],
            patient_data['doctor_name'],
            patient_data['contact_number'],
            patient_data['email'],
            patient_data['date_of_injury']
        ))
        
        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Append patient data to Excel sheet
        df = pd.DataFrame([patient_data])
        if not os.path.exists('patient_data.xlsx'):
            df.to_excel('patient_data.xlsx', index=False)
        else:
            existing_df = pd.read_excel('patient_data.xlsx')
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_excel('patient_data.xlsx', index=False)

        return True

    except psycopg2.Error as e:
        print("Error inserting patient details:", e)
        return False

# Home Page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        patient_data = {
            'aadhar_number': request.form['aadhar_number'],
            'name': request.form['name'],
            'address': request.form['address'],
            'doctor_name': request.form['doctor_name'],
            'contact_number': request.form['contact_number'],
            'email': request.form['email'],
            'date_of_injury': request.form['date_of_injury']
        }

        # Insert patient data into database and Excel sheet
        success = insert_patient(patient_data)
        if success:
            return redirect(url_for('success_route'))
        else:
            return render_template('error.html', message="Failed to add patient. Please try again.")

    return render_template('index.html')

# Route for handling emergency case
@app.route('/emergency')
def emergency_route():
    # Handle emergency case
    return render_template('emergency.html')

# Route for handling police case
@app.route('/police_case')
def police_case_route():
    # Handle police case
    return render_template('police_case.html')

# Route for displaying success message
@app.route('/success')
def success_route():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
