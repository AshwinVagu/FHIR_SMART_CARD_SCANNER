from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import base64
import json
import zlib
import requests


# The Flask app object is created here.
app = Flask(__name__)
app.app_context().push()
 
"""
Header Details are updated here.
:return: The updated request header is returned.
"""
@app.after_request
def add_header(r):
    r.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    r.headers["X-Frame-Options"] = "SAMEORIGIN"
    if r.headers.get('Content-Type', '') == 'application/json': 
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return r

@app.route("/hello", methods=["GET"])
def hello():
    return "HELLO" 

@app.route("/qr-decoding", methods=["POST"])
def qr_decoding():
    try:
        payload = request.get_json()
        code = payload['qr_result']
        result = decode_smart_health_card(code)
        try:
            verified = verify_iss(result[1]['iss'])
        except:
            verified = False    
        return jsonify({"result":result,"verified":verified}), 201
    except Exception as error_message:
        return jsonify({"message":error_message}),500  
    

def decode_smart_health_card(shc_data):
    try:
        # Step 1: Remove the "shc:/" prefix
        if shc_data.startswith("shc:/"):
            shc_data = shc_data[5:]

        # Step 2: Convert the numeric string to ASCII
        pairs = [int(shc_data[i:i+2]) + 45 for i in range(0, len(shc_data), 2)]
        jws = ''.join(chr(pair) for pair in pairs)

        print("Decoded JWS String:", jws)  # Debugging: Check the JWS string

        # Step 3: Split the JWS into its components
        if jws.count('.') != 2:
            raise ValueError("Decoded data does not have a valid JWS structure")
        header, payload, signature = jws.split('.')

        # Step 4: Base64-decode the header and payload
        def base64_decode(data):
            """Helper function to decode base64 strings with padding."""
            padding = '=' * (4 - len(data) % 4)  # Add padding if necessary
            return base64.urlsafe_b64decode(data + padding)

        # Decode header
        header_json = json.loads(base64_decode(header).decode('utf-8'))
        print("Decoded Header:", json.dumps(header_json, indent=2))

        # Decode payload
        compressed_payload = base64_decode(payload)
        if header_json.get("zip") == "DEF":
            # Decompress payload if "zip" is "DEF"
            decompressed_payload = zlib.decompress(compressed_payload, wbits=-15)  # Raw DEFLATE
            payload_json = json.loads(decompressed_payload.decode('utf-8'))
        else:
            payload_json = json.loads(compressed_payload.decode('utf-8'))

        print("Decoded Payload:", json.dumps(payload_json, indent=2))
        return header_json, payload_json

    except ValueError as ve:
        print(f"Value Error: {ve}")
        return None
    except Exception as e:
        print(f"Error decoding SMART Health Card: {e}")
        return None 

def verify_iss(iss):
    smart_config_url = f"{iss}/.well-known/smart-configuration"

    # Fetch SMART configuration
    try:
        response = requests.get(smart_config_url)
        response.raise_for_status()
        smart_config = response.json()  
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch SMART configuration: {e}")

    # Validate `iss`
    if smart_config.get("issuer") != iss:
        raise Exception("Issuer validation failed. The 'iss' does not match the SMART configuration's issuer.")

    # Check required endpoints
    required_fields = ["authorization_endpoint", "token_endpoint", "capabilities"]
    for field in required_fields:
        if field not in smart_config:
            raise Exception(f"SMART configuration missing required field: {field}")

    # Ensure HTTPS
    if not iss.startswith("https://"):
        raise Exception("Issuer must use HTTPS.")
    for field in ["authorization_endpoint", "token_endpoint"]:
        if not smart_config.get(field, "").startswith("https://"):
            raise Exception(f"{field} must use HTTPS.")

    print("Issuer verified successfully and SMART configuration is valid.")
    return True       


def verify_iss(iss):
    smart_config_url = f"{iss}/.well-known/smart-configuration"

    # Fetch SMART configuration
    try:
        response = requests.get(smart_config_url)
        response.raise_for_status()
        smart_config = response.json()  
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch SMART configuration: {e}")

    # Validate `iss`
    if smart_config.get("issuer") != iss:
        raise Exception("Issuer validation failed. The 'iss' does not match the SMART configuration's issuer.")

    # Check required endpoints
    required_fields = ["authorization_endpoint", "token_endpoint", "capabilities"]
    for field in required_fields:
        if field not in smart_config:
            raise Exception(f"SMART configuration missing required field: {field}")

    # Ensure HTTPS
    if not iss.startswith("https://"):
        raise Exception("Issuer must use HTTPS.")
    for field in ["authorization_endpoint", "token_endpoint"]:
        if not smart_config.get(field, "").startswith("https://"):
            raise Exception(f"{field} must use HTTPS.")

    print("Issuer verified successfully and SMART configuration is valid.")
    return True

    
if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=10000)
    # app.run()