from flask import Flask, jsonify, request
import requests
import json
import re

app = Flask(__name__)

# --- 🛑 ASLI FIX: Flask ko keys sort karne se rokna ---
app.config['JSON_SORT_KEYS'] = False
try:
    app.json.sort_keys = False
except AttributeError:
    pass

# --- 🚀 LANDING PAGE (CUSTOM MESSAGE) ---
@app.route('/')
def home():
    welcome_msg = f"""
    🚀 Welcome to Ultimate Mail Info API
    Status: ONLINE ✅

    Duniya ki sabse fast Mail API, processing 10.2 Billion records.

    📌 How to Use:
    https://{request.host}/mail=hardik.kotak@gmail.com

    Developed by @BRONX_ULTRA | Privacy Protected ✅
    """
    return welcome_msg, 200, {'Content-Type': 'text/plain; charset=utf-8'}

# --- 🔍 REAL-TIME MAIL SEARCH ENGINE ---
@app.route('/mail=<email_id>')
def get_mail_info(email_id):
    source_url = f"https://trial-info-api.vercel.app/email/{email_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(source_url, headers=headers, timeout=15)
        raw_text = response.text

        # 1. Regex se Results wala part [ ... ] nikalna
        json_match = re.search(r'Results:\s*(\[.*\])', raw_text, re.DOTALL)

        if json_match:
            json_string = json_match.group(1)
            raw_results = json.loads(json_string)
            
            # 2. EXACT LINE-BY-LINE ORDERING (Aapke sequence ke hisaab se)
            ordered_results = []
            for item in raw_results:
                record = {
                    "email": item.get("email", ""),
                    "name": item.get("name", ""),
                    "fname": item.get("fname", ""),
                    "mobile": item.get("mobile", ""),
                    "id": item.get("id", ""),
                    "address": item.get("address", ""),
                    "alt": item.get("alt", "")
                }
                ordered_results.append(record)
            
            # 3. Final Result setup
            final_response = {
                "developer": "@BRONX_ULTRA",
                "status": "success",
                "total_found": len(ordered_results),
                "results": ordered_results
            }
            
            return jsonify(final_response)
        
        else:
            return jsonify({
                "status": "error", 
                "message": "No data found for this Email", 
                "developer": "@BRONX_ULTRA"
            }), 404

    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": "System Fault", 
            "details": str(e), 
            "developer": "@BRONX_ULTRA"
        }), 500
