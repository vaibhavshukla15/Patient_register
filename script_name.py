import psycopg2

# Function to update patient details in the database
def update_patient(email, date_of_injury, patient_name):
    try:
        # PostgreSQL connection
        conn = psycopg2.connect(
            dbname="patient_register",
            user="vaibhav",
            password="72258",
            host="localhost"
        )
        cursor = conn.cursor()

        # Update patient details
        cursor.execute("UPDATE patients SET email = %s, date_of_injury = %s WHERE patient_name = %s",
                       (email, date_of_injury, patient_name))
        
        # Commit changes and close the cursor and connection
        conn.commit()
        cursor.close()
        conn.close()

        print("Patient details updated successfully.")

    except psycopg2.Error as e:
        print("Error updating patient details:", e)

# Update Akshat's details
update_patient('akshat23@gmail.com', '2023-07-15', 'Akshat')

# Update Rohan's details
update_patient('rohan1233@gmail.com', '2024-03-22', 'Rohan')
