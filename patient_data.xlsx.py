import pandas as pd

# Create a DataFrame with headers
columns = ['Aadhar Number', 'Patient Name', 'Address', 'Doctor Name', 'Contact Number', 'Email', 'Date of Injury']
df = pd.DataFrame(columns=columns)

# Save the DataFrame to Excel
df.to_excel('patient_data.xlsx', index=False)

print("Excel file 'patient_data.xlsx' created successfully.")
