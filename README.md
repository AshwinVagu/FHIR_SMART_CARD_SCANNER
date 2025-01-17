
# SMART Health Card QR Scanner and FHIR Verifier

This project is a Flutter-based mobile application designed to scan SMART Health Card QR codes and retrieve FHIR (Fast Healthcare Interoperability Resources) data. It integrates with a Flask-based API for decoding the QR code, verifying the iss field (issuer), and returning the FHIR bundle details along with verification results.

## Features

### Flutter App
- QR Code Scanning: Scan SMART Health Card QR codes.
- Data Verification: Send the scanned code to a Flask API for validation and decoding.
- Real-Time Feedback: Display the FHIR bundle details and the verification status.
### Flask API
- QR Code Decoding: Decode SMART Health Card QR codes using the SHC standard.
- FHIR Data Validation: Verify the issuer (iss) in the FHIR bundle to ensure legitimacy.
- Response: Return the decoded data and verification status.


### Tech Stack

Mobile Application (Frontend):
1. Language: Dart
2. Framework: Flutter
3. Dependencies:
- flutter_barcode_scanner: For scanning QR codes.
- http: For API communication.
- qr_flutter: For QR code generation (if needed).

Backend API:
1. Language: Python
2. Framework: Flask
3. Dependencies:
- Flask: Core backend framework.
- Flask-Cors: To handle cross-origin resource sharing.
- requests: For external HTTP requests.
4. Additional Modules:
- zlib and base64: For decoding QR code data.


## Installation and Setup

### Prerequisites:- 
Flutter SDK: Installed and configured. Install Flutter
Python: Version 3.8 or higher. Install Python
Package Manager: pip for Python dependencies.

### Frontend (Flutter)
Clone the repository:
git clone <repository-url>
cd <repository-folder>/flutter-app

Install dependencies:
flutter pub get

Run the app:
flutter run


### Backend (Flask)
Navigate to the backend folder:
cd <repository-folder>/flask-api
Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate     # For Windows

Install dependencies:
pip install -r requirements.txt

Start the API server:
python main.py

### API Endpoints

POST /qr-decoding

Description: Decodes and validates the SMART Health Card QR code.
Request Body:
{
  "qr_result": "scanned_qr_code_data"
}

Response:
201: Decoded data and verification status.
500: Error message if decoding or validation fails.


### Workflow

- QR Code Scanning: Use the mobile app to scan a SMART Health Card QR code.
- Data Submission: The scanned data is sent to the Flask API.
- Decoding and Verification:
1. The API decodes the QR code and retrieves the FHIR bundle.
2. It verifies the iss field against SMART Health Card specifications.
3. Response: The decoded data and verification results are sent back to the Flutter app and displayed.


### Example Use Case

- Open the Flutter app and click "Scan QR Code."
- Point the camera at a SMART Health Card QR code.
- View the decoded FHIR data and verification status displayed in the app.
