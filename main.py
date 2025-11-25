import os
from flask import Flask, render_template, request, jsonify
import requests
import json 
from typing import List, Optional

app = Flask(__name__)
app.secret_key = 'your_super_secret_key' 

# CRITICAL: Replace with your actual n8n webhook URL
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/ocr" 

def process_ocr_text_to_table(raw_text: str) -> List[List[str]]:
    """
    Converts a single, comma-separated 'TITLE:DATA' string 
    into a list of lists: [['TITLE', 'DATA'], ...], which is required 
    by the index.html template's table generation function.
    """
    table_data = []
    
    # 1. Strip leading/trailing whitespace and split the entire text by the main separator: ', '
    # This handles the comma-space separation rule from your prompt.
    key_value_pairs = [pair.strip() for pair in raw_text.strip().split(',')]
    
    for pair in key_value_pairs:
        # 2. Split each pair by the internal separator: ':'
        # We use .split(':', 1) to ensure only the first colon separates the title and data,
        # protecting against data fields that might contain a colon (e.g., a URL or time).
        parts = [p.strip() for p in pair.split(':', 1)]
        
        # 3. Validation: Ensure we have at least a title and a value
        if len(parts) == 2 and parts[0] and parts[1]:
            table_data.append(parts)
        elif len(parts) == 1 and parts[0]:
            # Handle cases where the data might be just a standalone title (unlikely, but safe)
             table_data.append([parts[0], ''])

    return table_data

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if "image" not in request.files:
        return jsonify({"error": "No file uploaded. Please select or capture an image."}), 400
    
    file = request.files["image"]
    files = {"file": (file.filename, file.stream, file.mimetype)}

    try:
        response = requests.post(N8N_WEBHOOK_URL, files=files, timeout=60)
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network Error communicating with OCR service: {e}"}), 503 

    if response.status_code == 200:
        try:
            data = response.json()
            raw_ocr_text = data.get("ocr_result", "") 
            
            # Use the updated processing function
            ocr_table_data = process_ocr_text_to_table(raw_ocr_text)
            
            return jsonify({
                "ocr_table_data": ocr_table_data,
                "success": True
            })
            
        except json.JSONDecodeError:
            return jsonify({"error": f"JSON Decode Error. Raw response: {response.text[:100]}..."}), 500
        
    else:
        error_message = f"Error from OCR service (Status {response.status_code}): {response.text}"
        return jsonify({"error": error_message}), response.status_code

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)