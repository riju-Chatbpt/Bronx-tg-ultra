from flask import Flask, request, jsonify, render_template_string
import requests
import time

app = Flask(__name__)

# --- CONFIGURATION ---
OWNER_TAG = "@BRONX_ULTRA"
CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"

# Telegram OSINT Backend API
BACKEND_API = "http://45.91.248.51:3000/api/tgnum"

# --- DASHBOARD HTML ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BRONX ULTRA TELEGRAM API</title>
    <style>
        body { background: #050505; color: #0088cc; font-family: 'Courier New', Courier, monospace; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .container { border: 1px solid #0088cc; padding: 30px; border-radius: 10px; box-shadow: 0 0 15px #0088cc; text-align: center; max-width: 600px; }
        h1 { font-size: 24px; margin-bottom: 10px; color: #0088cc; }
        .status { color: #fff; background: #0088cc; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
        .info { color: #ccc; font-size: 14px; margin: 20px 0; }
        .url { background: #111; padding: 10px; border-radius: 5px; color: #00aaff; word-break: break-all; font-size: 13px; }
        footer { margin-top: 20px; font-size: 12px; color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 BRONX ULTRA TELEGRAM OSINT API</h1>
        <span class="status">Status: ONLINE ✅</span>
        <p class="info">Fastest Telegram User Lookup API</p>
        <div class="url">
            📌 <b>How to Use:</b><br>
            https://{{ host }}/tg?id=7530266953
        </div>
        <footer>Developed by {{ owner }} | Privacy Protected ✅</footer>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(DASHBOARD_HTML, host=request.host, owner=OWNER_TAG)

@app.route('/tg')
def telegram_lookup():
    user_id = request.args.get('id')
    
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Missing 'id' parameter",
            "credit": CREDIT
        }), 400

    try:
        backend_url = f"{BACKEND_API}?id={user_id}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        resp = requests.get(backend_url, headers=headers, timeout=15)
        raw_data = resp.json()
        
        if raw_data.get("SUCCESS") == True:
            result = raw_data.get("RESULT", {})
            
            # Extract data and format with BRONX_ULTRA branding
            basic_info = result.get("BASIC_INFO", {})
            status_info = result.get("STATUS_INFO", {})
            activity_info = result.get("ACTIVITY_INFO", {})
            number_info = result.get("NUMBER_INFO", {})
            
            output = {
                "status": "success",
                "credit": CREDIT,
                "developer": DEVELOPER,
                "data": {
                    "basic_info": {
                        "id": basic_info.get("ID"),
                        "first_name": basic_info.get("FIRST_NAME"),
                        "last_name": basic_info.get("LAST_NAME"),
                        "usernames_count": basic_info.get("USERNAMES_COUNT", 0),
                        "names_count": basic_info.get("NAMES_COUNT", 0)
                    },
                    "status_info": {
                        "is_bot": status_info.get("IS_BOT", False),
                        "is_active": status_info.get("IS_ACTIVE", False)
                    },
                    "activity_info": {
                        "first_msg_date": activity_info.get("FIRST_MSG_DATE"),
                        "last_msg_date": activity_info.get("LAST_MSG_DATE"),
                        "total_msg_count": activity_info.get("TOTAL_MSG_COUNT", 0),
                        "msg_in_groups_count": activity_info.get("MSG_IN_GROUPS_COUNT", 0),
                        "admin_in_groups": activity_info.get("ADM_IN_GROUPS", 0),
                        "total_groups": activity_info.get("TOTAL_GROUPS", 0)
                    },
                    "number_info": {
                        "number": number_info.get("NUMBER"),
                        "country_code": number_info.get("COUNTRY_CODE"),
                        "country": number_info.get("COUNTRY")
                    }
                }
            }
            
            return jsonify(output)
        else:
            return jsonify({
                "status": "error",
                "message": "No data found for this Telegram ID",
                "credit": CREDIT
            }), 404
        
    except requests.exceptions.Timeout:
        return jsonify({
            "status": "error",
            "message": "Request timeout",
            "credit": CREDIT
        }), 504
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}",
            "credit": CREDIT
        }), 500

# Alternative route for /api/tgnum
@app.route('/api/tgnum')
def telegram_lookup_alt():
    return telegram_lookup()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
