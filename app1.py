from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# Function to fetch patient details from the database
def fetch_patient(aadhar_number):
    try:
        # PostgreSQL connection
        conn = psycopg2.connect(
            dbname="patient_register",
            user="vaibhav",
            password="72258",
            host="localhost"
        )
        cursor = conn.cursor()

        # Fetch patient details based on Aadhar number
        cursor.execute("SELECT patient_name, patient_address, doctor_name, contact_number, email, date_of_injury FROM patients WHERE aadhar_number = %s", (aadhar_number,))
        patient = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return patient

    except psycopg2.Error as e:
        print("Error connecting to database:", e)
        return None

# Home Page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        aadhar_number = request.form.get('aadhar_number')
        if not aadhar_number:
            return render_template('error.html', message="Please provide Aadhar number.")

        patient = fetch_patient(aadhar_number)

        if patient:
            # Render patient_details.html with patient details
            return render_template('patient_details.html', patient=patient)
        else:
            return render_template('error.html', message="Patient details not found.")

    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
