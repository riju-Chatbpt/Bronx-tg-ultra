from flask import Flask, request, jsonify, render_template_string
import requests
import time

app = Flask(__name__)

# --- CONFIGURATION ---
OWNER_TAG = "@BRONX_ULTRA"
CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"

# Valid API Keys
VALID_KEYS = [
    "BRONXop",
    "BRONXdemo",
    "BRONX2026"
]

# APIs
CHATID_API = "https://bronx-ultra-api2.onrender.com/chatid"
TG_BACKEND = "https://num-tg-info-api.vercel.app/"
NUMBER_API = "https://dhdh-hshs-dhds-six.vercel.app/api"

# --- DASHBOARD HTML ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BRONX ULTRA GOD API</title>
    <style>
        body { background: #050505; color: #bf00ff; font-family: 'Courier New', Courier, monospace; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 20px; }
        .container { border: 2px solid #bf00ff; padding: 30px; border-radius: 20px; box-shadow: 0 0 30px #bf00ff66; text-align: center; max-width: 750px; background: #0a0a0a; }
        h1 { font-size: 28px; margin-bottom: 10px; background: linear-gradient(135deg, #bf00ff, #ff0066); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .status { color: #fff; background: linear-gradient(135deg, #bf00ff, #ff0066); padding: 5px 15px; border-radius: 30px; font-weight: bold; display: inline-block; }
        .url { background: #111; padding: 15px; border-radius: 10px; color: #00ff88; word-break: break-all; font-size: 13px; border: 1px solid #333; margin: 10px 0; }
        .badge { display: inline-block; background: #333; padding: 3px 10px; border-radius: 20px; font-size: 11px; margin: 3px; color: #ffaa00; }
        footer { margin-top: 20px; font-size: 12px; color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👑 BRONX ULTRA GOD API</h1>
        <span class="status">⚡ GOD MODE ACTIVE</span>
        <p style="color: #ccc; margin: 20px 0;">
            <span class="badge">🔥 TG Info</span>
            <span class="badge">📱 Number Details</span>
            <span class="badge">🎯 Combined Output</span>
        </p>
        
        <div class="url">
            📌 <b>Username → TG Info + Number Details:</b><br>
            /tg?key=key&query=@username
        </div>
        <div class="url">
            📌 <b>ID → TG Info + Number Details:</b><br>
            /tg?key=key&query=7530266953
        </div>
        <div class="url">
            📌 <b>Old Style Username:</b><br>
            /tg?key=key&username=@BRONX_ULTRA
        </div>
        <div class="url">
            📌 <b>Old Style ID:</b><br>
            /tg?key=key&id=7530266953
        </div>
        
        <footer>Developed by {{ owner }} | GOD LEVEL API v2.0</footer>
    </div>
</body>
</html>
"""

def check_key(api_key):
    """Check if API key is valid"""
    if not api_key:
        return False
    return api_key in VALID_KEYS

def is_numeric_id(value):
    """Check if value is numeric ID or username"""
    clean = value.replace("@", "").strip()
    try:
        int(clean)
        return True
    except:
        return False

def get_chat_id_from_username(username):
    """Username se Chat ID nikalo"""
    try:
        clean = username.replace("@", "").strip()
        url = f"{CHATID_API}?username={clean}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        
        if data.get("status") == "success":
            return str(data.get("chat_id"))
        return None
    except Exception as e:
        print(f"Chat ID API Error: {e}")
        return None

def get_tg_info(query):
    """TG Backend se Full Telegram Info"""
    try:
        url = f"{TG_BACKEND}?id={query}"
        resp = requests.get(url, timeout=20)
        data = resp.json()
        
        if data.get("SUCCESS") == True:
            result = data.get("RESULT", {})
            basic = result.get("BASIC_INFO", {})
            status = result.get("STATUS_INFO", {})
            activity = result.get("ACTIVITY_INFO", {})
            number = result.get("NUMBER_INFO", {})
            
            phone_number = number.get("NUMBER", "")
            
            return {
                "success": True,
                "phone_number": phone_number,
                "tg_data": {
                    "basic_info": {
                        "id": basic.get("ID"),
                        "first_name": basic.get("FIRST_NAME"),
                        "last_name": basic.get("LAST_NAME"),
                        "usernames_count": basic.get("USERNAMES_COUNT", 0),
                        "names_count": basic.get("NAMES_COUNT", 0)
                    },
                    "status_info": {
                        "is_bot": status.get("IS_BOT", False),
                        "is_active": status.get("IS_ACTIVE", False)
                    },
                    "activity_info": {
                        "first_msg_date": activity.get("FIRST_MSG_DATE"),
                        "last_msg_date": activity.get("LAST_MSG_DATE"),
                        "total_msg_count": activity.get("TOTAL_MSG_COUNT", 0),
                        "msg_in_groups_count": activity.get("MSG_IN_GROUPS_COUNT", 0),
                        "admin_in_groups": activity.get("ADM_IN_GROUPS", 0),
                        "total_groups": activity.get("TOTAL_GROUPS", 0)
                    },
                    "number_info": {
                        "number": phone_number,
                        "country_code": number.get("COUNTRY_CODE"),
                        "country": number.get("COUNTRY")
                    }
                }
            }
        return {"success": False, "message": "No TG data found"}
    except Exception as e:
        print(f"TG Backend Error: {e}")
        return {"success": False, "message": str(e)}

def get_number_details(phone_number):
    """Phone Number se Full Details nikalo"""
    try:
        url = f"{NUMBER_API}?key=SEXY_BOY&number={phone_number}"
        resp = requests.get(url, timeout=20)
        data = resp.json()
        
        if data.get("success") == True:
            inner_result = data.get("result", {})
            
            # Clean results - remove developer field
            results = inner_result.get("results", [])
            cleaned_results = []
            for r in results:
                cleaned_results.append({
                    "name": r.get("NAME", ""),
                    "fname": r.get("fname", ""),
                    "address": r.get("ADDRESS", ""),
                    "circle": r.get("circle", ""),
                    "mobile": r.get("MOBILE", ""),
                    "alt": r.get("alt", ""),
                    "id": r.get("id"),
                    "email": r.get("email")
                })
            
            return {
                "success": True,
                "count": inner_result.get("count", len(cleaned_results)),
                "results": cleaned_results
            }
        return {"success": False, "message": "No number data found"}
    except Exception as e:
        print(f"Number API Error: {e}")
        return {"success": False, "message": str(e)}

@app.route('/')
def home():
    return render_template_string(DASHBOARD_HTML, host=request.host, owner=OWNER_TAG)

@app.route('/tg')
def god_lookup():
    start_time = time.time()
    
    # Get API Key
    api_key = request.args.get('key', '').strip()
    
    # Check Key FIRST
    if not check_key(api_key):
        return jsonify({
            "status": "error",
            "message": "❌ Invalid or Missing API Key! Contact @BRONX_ULTRA",
            "valid_keys_sample": ["invild", "invilid"],
            "usage": "/tg?key=YOUR_KEY&query=@user OR /tg?key=YOUR_KEY&query=7530266953"
        }), 403
    
    # Get inputs
    username = request.args.get('username', '').strip()
    user_id = request.args.get('id', '').strip()
    query = request.args.get('query', '').strip()
    
    # Agar kuch nahi diya
    if not username and not user_id and not query:
        return jsonify({
            "status": "error",
            "message": "Missing 'username', 'id', or 'query' parameter",
            "example_urls": [
                f"/tg?key={api_key}&query=@BRONX_ULTRA",
                f"/tg?key={api_key}&query=7530266953",
                f"/tg?key={api_key}&username=@BRONX_ULTRA",
                f"/tg?key={api_key}&id=7530266953"
            ],
            "credit": CREDIT
        }), 400
    
    try:
        final_query = None
        method = None
        query_input = None
        
        # CASE 1: COMBINED QUERY parameter
        if query:
            query_input = query
            clean = query.replace("@", "").strip()
            
            if is_numeric_id(clean):
                final_query = clean
                method = "query_direct_id"
            else:
                final_query = get_chat_id_from_username(clean)
                method = "query_username_to_id"
        
        # CASE 2: ID directly provided
        elif user_id:
            query_input = user_id
            clean = user_id.replace("@", "").strip()
            
            if is_numeric_id(clean):
                final_query = clean
                method = "direct_id"
            else:
                final_query = get_chat_id_from_username(clean)
                method = "username_in_id_param"
        
        # CASE 3: Username provided
        elif username:
            query_input = username
            clean = username.replace("@", "").strip()
            
            if is_numeric_id(clean):
                final_query = clean
                method = "id_in_username_param"
            else:
                final_query = get_chat_id_from_username(clean)
                method = "username"
        
        if not final_query:
            return jsonify({
                "status": "error",
                "message": f"Could not resolve: {query_input}",
                "credit": CREDIT
            }), 404
        
        # ============================================
        # STEP 1: Get Telegram Info
        # ============================================
        tg_result = get_tg_info(final_query)
        
        if not tg_result.get("success"):
            return jsonify({
                "status": "error",
                "message": "Could not fetch Telegram info",
                "detail": tg_result.get("message", "Unknown error"),
                "credit": CREDIT
            }), 404
        
        phone_number = tg_result.get("phone_number", "")
        
        # ============================================
        # STEP 2: Get Number Details (if phone found)
        # ============================================
        number_result = None
        if phone_number:
            number_result = get_number_details(phone_number)
        
        # ============================================
        # BUILD COMBINED RESPONSE
        # ============================================
        output = {
            "status": "success",
            "credit": CREDIT,
            "developer": DEVELOPER,
            "method": method,
            "resolved_id": final_query,
            "query_input": query_input,
            "query_time_ms": round((time.time() - start_time) * 1000, 2),
            "telegram_info": tg_result.get("tg_data"),
            "number_details": None
        }
        
        if number_result and number_result.get("success"):
            output["number_details"] = {
                "success": True,
                "count": number_result.get("count", 0),
                "results": number_result.get("results", [])
            }
        elif phone_number:
            output["number_details"] = {
                "success": False,
                "message": "Number found but details not available",
                "phone": phone_number
            }
        else:
            output["number_details"] = {
                "success": False,
                "message": "No phone number found in Telegram data"
            }
        
        return jsonify(output)
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}",
            "credit": CREDIT
        }), 500

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "credit": CREDIT,
        "valid_keys_count": len(VALID_KEYS),
        "services": {
            "chatid_api": CHATID_API,
            "tg_backend": TG_BACKEND,
            "number_api": NUMBER_API
        }
    })

@app.route('/api/tgnum')
def telegram_lookup_alt():
    return god_lookup()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
