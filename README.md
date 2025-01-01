# Flask-Sheets: A Flask Web App with Google Sheets Integration

This project demonstrates a simple Flask web application that allows users to submit data through a form. The collected data is then automatically written to a designated Google Sheet.

**Key Features:**

* **Flask Web Framework:** Built using the popular Python web framework, Flask.
* **Form Handling:** Includes a basic HTML form for user input.
* **Google Sheets Integration:** Utilizes the `gspread` library to interact with Google Sheets.
* **Data Validation (Optional):** Basic data validation can be implemented to ensure data integrity.
* **User-Friendly Interface:** A simple and intuitive user interface for easy data submission.

**Getting Started:**

1. **Prerequisites:**
   - Python 3.x installed
   - `pip` or `poetry` for package management
   - A Google Cloud Platform project with the Google Sheets API enabled
   - A Google Sheets service account with appropriate permissions

2. **Installation:**
   ```bash
   pip install Flask gspread google-auth
