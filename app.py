import os
from flask import Flask, request, redirect, url_for, render_template, flash
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_wtf.csrf import CSRFProtect
import base64

# ✅ Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ Google Sheets API Setup
try:
    # Fetch environment variables
    credentials_path = os.getenv('CREDENTIALS_FILE')  # Path to credentials.json
    SHEET_KEY = os.getenv('GOOGLE_SHEET_KEY')  # Google Sheet Key
    
    if not credentials_path or not SHEET_KEY:
        raise EnvironmentError("Environment variables 'CREDENTIALS_FILE' or 'GOOGLE_SHEET_KEY' are not set.")
    
    # Google Sheets API Authorization
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
    CREDS = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, SCOPE)
    CLIENT = gspread.authorize(CREDS)
    SHEET = CLIENT.open_by_key(SHEET_KEY).sheet1
    
    print("✅ Google Sheets connected successfully!")
except Exception as e:
    print(f"❌ Google Sheets Connection Error: {e}")
    SHEET = None

# ✅ Initialize CSRF Protection
csrf = CSRFProtect(app)

# ✅ Route for Transport Form Submission
@app.route('/', methods=['GET', 'POST'])
def transport_form():
    if request.method == 'POST':
        try:
            if not SHEET:
                flash('❌ Google Sheets is not connected.', 'danger')
                return redirect(url_for('transport_form'))
            
            # Collect data from the form
            date = request.form.get('date')
            driver_name = request.form.get('driver_name')
            vehicle_plate = request.form.get('vehicle_plate')
            start_time = request.form.get('start_time')
            arrival_time = request.form.get('arrival_time')
            location = request.form.get('location')
            odometer_start = request.form.get('odometer_start')
            odometer_end = request.form.get('odometer_end')
            notes = request.form.get('notes')
            signature_data = request.form.get('signature')  # Get signature data

            # Validate essential fields
            if not all([date, driver_name, vehicle_plate, start_time, arrival_time, location, odometer_start, odometer_end, notes, signature_data]):
                flash('❌ All fields are required.', 'danger')
                return redirect(url_for('transport_form'))
            
            # Process and validate the signature data (Base64)
            if not signature_data.startswith('data:image/png;base64,'):
                flash('❌ Invalid signature data.', 'danger')
                return redirect(url_for('transport_form'))
            
            # Append data to Google Sheets
            SHEET.append_row([
                date, driver_name, vehicle_plate, start_time, arrival_time,
                location, odometer_start, odometer_end, notes, signature_data
            ])
            flash('✅ Data added to Google Sheets successfully!', 'success')
        
        except Exception as e:
            flash(f'❌ Error adding data: {e}', 'danger')
        
        return redirect(url_for('transport_form'))
    
    return render_template('form.html')

# ✅ Run App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
