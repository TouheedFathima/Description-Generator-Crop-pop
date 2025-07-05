import os
import re
import platform
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from description_generator import generate_description, generate_pass_opportunity_description
from flask_cors import CORS
import pytesseract
from PIL import Image
import io
import shutil

if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = os.environ.get('TESSERACT_CMD', '/usr/bin/tesseract')

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(
    app,
    resources={r"/*": {
        "origins": ["https://app.opptiverse.com"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }}
)

@app.before_request
def handle_options_request():
    if request.method == "OPTIONS":
        return '', 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract-text', methods=['POST', 'OPTIONS'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    try:
        if not shutil.which('tesseract'):
            return jsonify({"error": "Tesseract is not installed on this server. Contact support."}), 503
        img = Image.open(io.BytesIO(file.read()))
        extracted_text = pytesseract.image_to_string(img)
        return jsonify({"text": extracted_text.strip()})
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return jsonify({"error": f"Failed to extract text: {str(e)}"}), 500

@app.route('/generate-description', methods=['POST', 'OPTIONS'])
def generate_description_endpoint():
    data = request.json
    print("Received payload for /generate-description:", data)

    # Define mandatory fields with validation rules based on form type
    if data.get("companyType") == "company" and "workMode" in data:
        # "For My Company" form
        mandatory_fields = {
            "companyName": {"field_name": "Company Name"},
            "opportunityTitle": {"field_name": "Opportunity Title"},
            "opportunityType": {"field_name": "Opportunity Type"},
            "location": {"field_name": "Location"},
            "workMode": {"field_name": "Work Mode"},
            "numberOfOpenings": {"field_name": "Number of Openings"},
            "lastDate": {"field_name": "Last Date to Apply"},
            "skillsRequired": {"field_name": "Skills Required", "validate": lambda v: len([s.strip() for s in v.split(",") if s.strip()]) > 0},
            "timeCommitment": {"field_name": "Time Commitment"},
            "salaryMin": {"field_name": "Minimum Salary", "validate": lambda v: v >= 0},
            "salaryMax": {"field_name": "Maximum Salary", "validate": lambda v: v >= 0}
        }
    else:
        # "Individual" form
        mandatory_fields = {
            "postType": {"field_name": "Post Type"},
            "location": {"field_name": "Location"},
            "address": {"field_name": "Address"},
            "title": {"field_name": "Title"},
            "package": {"field_name": "Package"},
            "lastDate": {"field_name": "Last Date"},
            "vacancy": {"field_name": "Vacancy"},
            "skills": {"field_name": "Skills"}
        }

    # Validate mandatory fields
    for field, rule in mandatory_fields.items():
        value = data.get(field)
        field_name = rule["field_name"]
        print(f"Validating {field}: {value} (type: {type(value)})")
        if value is None:
            print(f"Field '{field_name}' is missing, will use default in description_generator.py")
            continue
        if not rule.get("validate") and str(value).strip() == "":
            return jsonify({"error": f"Required field '{field_name}' is empty, please fill it.", "field": field, "value": value}), 400
        if rule.get("validate"):
            try:
               validated_value = float(value)
               if not rule["validate"](validated_value):
                    error_msg = f"Required field '{field_name}' is invalid, please correct it."
                    if field in ["numberOfOpenings", "vacancy"]:
                        error_msg = f"Required field '{field_name}' must be a positive number, please correct it."
                    elif field in ["salaryMin", "salaryMax"]:
                        error_msg = f"Required field '{field_name}' must be a non-negative number, please correct it."
                    return jsonify({"error": error_msg, "field": field, "value": value}), 400
            except (ValueError, TypeError):
              return jsonify({"error": f"Required field '{field_name}' must be a number, please correct it.", "field": field, "value": value}), 400


    # Additional validations for "For My Company" form
    if data.get("companyType") == "company" and "workMode" in data:
        salary_min = float(data.get("salaryMin", 0))
        salary_max = float(data.get("salaryMax", 0))
        if salary_min > salary_max:
            return jsonify({"error": "Maximum salary must be greater than or equal to minimum salary", "field": "salaryMax", "value": salary_max}), 400

        if isinstance(data.get("skillsRequired"), str):
            data["skillsRequired"] = [s.strip() for s in data["skillsRequired"].split(",") if s.strip()]

        salary_option = data.get("salaryOption", "")
        valid_salary_options = ["Negotiable", "Prefer Not to Disclose", ""]
        if salary_option not in valid_salary_options:
            return jsonify({"error": f"Invalid salary option: {salary_option}. Must be one of {valid_salary_options[:-1]} or empty.", "field": "salaryOption", "value": salary_option}), 400
        data["salaryOption"] = salary_option
    else:
        if isinstance(data.get("skills"), str):
            data["skills"] = [s.strip() for s in data["skills"].split(",") if s.strip()]
        if isinstance(data.get("keywords"), str):
            data["keywords"] = [k.strip() for k in data["keywords"].split(",") if k.strip()]
        else:
            data["keywords"] = []

        salary_option = data.get("salaryOption", "")
        valid_salary_options = ["Negotiable", "Prefer Not to Disclose", ""]
        if salary_option not in valid_salary_options:
            return jsonify({"error": f"Invalid salary option: {salary_option}. Must be one of {valid_salary_options[:-1]} or empty.", "field": "salaryOption", "value": salary_option}), 400
        data["salaryOption"] = salary_option

        skills = data.get("skills", [])
        keywords = data.get("keywords", [])
        print(f"Processed skills: {skills}, keywords: {keywords}")
        if len(skills) == 0:
            print("Skills are missing or empty, will use default in description_generator.py")
            data["skills"] = []
        if len(keywords) == 0:
            print("Keywords are missing or empty, will use default in description_generator.py")
            data["keywords"] = []

    # Generate the description
    try:
        response = generate_description(data)
        print("Generated description:", response[:100] + "...")
        return jsonify({'description': response})
    except Exception as e:
        print("Error in /generate-description:", str(e))
        return jsonify({"error": f"Failed to generate description: {str(e)}"}), 500

@app.route('/pass-opportunity', methods=['POST', 'OPTIONS'])
def pass_opportunity():
    data = request.json
    print("Received payload for /pass-opportunity:", data)
    return jsonify({"message": "Opportunity passed successfully!"})

@app.route('/generate-pass-description', methods=['POST', 'OPTIONS'])
def generate_pass_description_endpoint():
    data = request.json
    print("Received payload for /generate-pass-description:", data)

    # Optional fields with defaults
    data["companyName"] = data.get("companyName", "Individual")
    data["location"] = data.get("location", "Not specified")
    data["workMode"] = data.get("workMode", "Not specified")
    data["numberOfOpenings"] = float(data.get("numberOfOpenings", 1))
    data["lastDate"] = data.get("lastDate", "")
    data["educationRequirements"] = data.get("educationRequirements", "Not specified")
    data["industryExpertise"] = data.get("industryExpertise", "")
    data["preferredExperience"] = data.get("preferredExperience", "Not specified")
    data["skillsRequired"] = data.get("skillsRequired", "")
    data["languagePreference"] = data.get("languagePreference", "")
    data["genderPreference"] = data.get("genderPreference", "")
    data["salaryMin"] = float(data.get("salaryMin", 0))
    data["salaryMax"] = float(data.get("salaryMax", 0))
    data["timeCommitment"] = data.get("timeCommitment", "")
    data["recruiterName"] = data.get("recruiterName", "")
    data["phoneNumber"] = data.get("phoneNumber", "")

    # Validate salaryOption
    salary_option = data.get("salaryOption", "")
    valid_salary_options = ["Negotiable", "Prefer Not to Disclose", ""]
    if salary_option not in valid_salary_options:
        return jsonify({"error": f"Invalid salary option: {salary_option}. Must be one of {valid_salary_options[:-1]} or empty.", "field": "salaryOption", "value": salary_option}), 400
    data["salaryOption"] = salary_option

    # Validate optional fields only if provided
    optional_fields = {
        "phoneNumber": {"field_name": "Phone Number", "validate": lambda v: len(re.sub(r"[^0-9]", "", v)) >= 10},
        "emailAddress": {"field_name": "Email Address", "validate": lambda v: bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", v))}
    }
    for field, rule in optional_fields.items():
        value = data.get(field)
        if value and str(value).strip() != "":
            if not rule["validate"](value):
                error_msg = f"Field '{rule['field_name']}' is invalid, please correct it."
                if field == "phoneNumber":
                    error_msg = f"Field '{rule['field_name']}' must be a valid phone number (at least 10 digits), please correct it."
                return jsonify({"error": error_msg, "field": field, "value": value}), 400

    # Validate salary range
    if data["salaryMin"] > data["salaryMax"] and data["salaryMax"] != 0:
        return jsonify({"error": "Maximum salary must be greater than or equal to minimum salary", "field": "salaryMax", "value": data["salaryMax"]}), 400

    # Process skillsRequired if provided
    if isinstance(data.get("skillsRequired"), str) and data["skillsRequired"].strip():
        data["skillsRequired"] = [s.strip() for s in data["skillsRequired"].split(",") if s.strip()]
    else:
        data["skillsRequired"] = []

    try:
        response = generate_pass_opportunity_description(data)
        print("Generated description for /generate-pass-description:", response[:100] + "...")
        return jsonify({'description': response})
    except Exception as e:
        print("Error in /generate-pass-description:", str(e))
        return jsonify({"error": f"Failed to generate description: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port, debug=True)