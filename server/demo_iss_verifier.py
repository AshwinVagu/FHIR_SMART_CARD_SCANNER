import requests
from urllib.parse import urlparse

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

# Example Usage
# iss = "https://accounts.google.com/"
# verify_iss(iss)