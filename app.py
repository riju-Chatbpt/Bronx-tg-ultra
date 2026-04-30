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
TG_BACKEND_NEW = "https://num-tg-info-api.vercel.app/"

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
        .container { border: 2px solid #bf00ff; padding: 30px; border-radius: 20px; box-shadow: 0 0 30px #bf00ff66; text-align: center; max-width: 700px; background: #0a0a0a; }
        h1 { font-size: 28px; margin-bottom: 10px; background: linear-gradient(135deg, #bf00ff, #ff0066); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .status { color: #fff; background: linear-gradient(135deg, #bf00ff, #ff0066); padding: 5px 15px; border-radius: 30px; font-weight: bold; display: inline-block; }
        .info { color: #ccc; font-size: 14px; margin: 20px 0; }
        .url { background: #111; padding: 15px; border-radius: 10px; color: #00ff88; word-break: break-all; font-size: 13px; border: 1px solid #333; margin: 10px 0; }
        footer { margin-top: 20px; font-size: 12px; color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👑 BRONX ULTRA GOD API</h1>
        <span class="status">⚡ GOD MODE ACTIVE</span>
        <p class="info">Username ya ID Dono Se Full OSINT!</p>
        
        <div class="url">
            📌 <b>Username Se:</b><br>
            /tg?key=yourkey&username=@BRONX_ULTRA
        </div>
        <div class="url">
            📌 <b>ID Se:</b><br>
            /tg?key=yourkey&id=7530266953
        </div>
        <div class="url">
            📌 <b>Combined:</b><br>
            /tg?key=yourkey&query=@BRONX_ULTRA<br>
            /tg?key=yourkey&query=7530266953
        </div>
        
        <footer>Developed by {{ owner }} | GOD LEVEL API</footer>
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

def get_full_info_from_backend(query):
    """Backend se Full OSINT"""
    try:
        url = f"{TG_BACKEND_NEW}?id={query}"
        resp = requests.get(url, timeout=20)
        data = resp.json()
        
        if data.get("SUCCESS") == True:
            result = data.get("RESULT", {})
            basic = result.get("BASIC_INFO", {})
            status = result.get("STATUS_INFO", {})
            activity = result.get("ACTIVITY_INFO", {})
            number = result.get("NUMBER_INFO", {})
            
            return {
                "success": True,
                "data": {
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
                        "number": number.get("NUMBER"),
                        "country_code": number.get("COUNTRY_CODE"),
                        "country": number.get("COUNTRY")
                    }
                }
            }
        return {"success": False, "message": "No data found"}
    except Exception as e:
        print(f"Backend Error: {e}")
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
            "valid_keys": ["yourkey", "yourkey"],
            "usage": "/tg?key=YOUR_KEY&username=@user OR /tg?key=YOUR_KEY&query=@user"
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
                f"/tg?key={api_key}&username=@BRONX_ULTRA",
                f"/tg?key={api_key}&id=7530266953",
                f"/tg?key={api_key}&query=@BRONX_ULTRA",
                f"/tg?key={api_key}&query=7530266953"
            ],
            "credit": CREDIT
        }), 400
    
    try:
        final_query = None
        method = None
        query_input = None
        
        # CASE 1: COMBINED QUERY parameter (NEW!)
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
        
        # Get full info from backend
        backend_result = get_full_info_from_backend(final_query)
        
        if backend_result.get("success"):
            return jsonify({
                "status": "success",
                "credit": CREDIT,
                "developer": DEVELOPER,
                "method": method,
                "resolved_id": final_query,
                "query_input": query_input,
                "query_time_ms": round((time.time() - start_time) * 1000, 2),
                "data": backend_result.get("data")
            })
        else:
            return jsonify({
                "status": "error",
                "message": backend_result.get("message", "No OSINT data found"),
                "resolved_id": final_query,
                "credit": CREDIT
            }), 404
            
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
        "valid_keys_count": len(VALID_KEYS)
    })

@app.route('/api/tgnum')
def telegram_lookup_alt():
    return god_lookup()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
