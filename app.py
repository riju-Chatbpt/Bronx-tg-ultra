from flask import Flask, request, jsonify, render_template_string
import requests
import time

app = Flask(__name__)

# --- CONFIGURATION ---
OWNER_TAG = "@BRONX_ULTRA"
CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"

# APIs
CHATID_API = "https://bronx-ultra-api2.onrender.com/chatid"  # Tumhari Render API
TG_BACKEND = "http://45.91.248.51:3000/api/tgnum"  # Hidden OSINT API

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
        .badge { display: inline-block; background: #333; padding: 3px 10px; border-radius: 20px; font-size: 11px; margin: 5px; }
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
            /tg?username=@BRONX_ULTRA
        </div>
        <div class="url">
            📌 <b>ID Se:</b><br>
            /tg?id=7530266953
        </div>
        
        <p>
            <span class="badge">🔥 Chat ID</span>
            <span class="badge">📱 Phone</span>
            <span class="badge">💬 Messages</span>
            <span class="badge">👥 Groups</span>
            <span class="badge">⭐ Premium</span>
        </p>
        
        <footer>Developed by {{ owner }} | GOD LEVEL API</footer>
    </div>
</body>
</html>
"""

def get_chat_id_from_username(username):
    """Username se Chat ID nikalo"""
    try:
        clean = username.replace("@", "").strip()
        url = f"{CHATID_API}?username={clean}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        
        if data.get("status") == "success":
            return data.get("chat_id")
        return None
    except:
        return None

def get_full_info_from_id(user_id):
    """ID se Full OSINT nikalo"""
    try:
        url = f"{TG_BACKEND}?id={user_id}"
        resp = requests.get(url, timeout=20)
        data = resp.json()
        
        if data.get("SUCCESS") == True:
            result = data.get("RESULT", {})
            basic = result.get("BASIC_INFO", {})
            status = result.get("STATUS_INFO", {})
            activity = result.get("ACTIVITY_INFO", {})
            number = result.get("NUMBER_INFO", {})
            
            return {
                "status": "success",
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
        return None
    except:
        return None

@app.route('/')
def home():
    return render_template_string(DASHBOARD_HTML, host=request.host, owner=OWNER_TAG)

@app.route('/tg')
def god_lookup():
    start_time = time.time()
    
    # Check input
    username = request.args.get('username', '').strip()
    user_id = request.args.get('id', '').strip()
    
    # Determine what we have
    if not username and not user_id:
        return jsonify({
            "status": "error",
            "message": "Missing 'username' or 'id' parameter",
            "credit": CREDIT
        }), 400
    
    try:
        final_id = None
        method = None
        
        # If ID directly provided
        if user_id:
            # Clean ID (remove @ if accidentally added)
            final_id = user_id.replace("@", "").strip()
            method = "direct_id"
        
        # If username provided, get Chat ID first
        elif username:
            final_id = get_chat_id_from_username(username)
            if not final_id:
                return jsonify({
                    "status": "error",
                    "message": f"Could not find Chat ID for: {username}",
                    "credit": CREDIT
                }), 404
            method = "username_to_id"
        
        # Now get full info using ID
        if final_id:
            full_info = get_full_info_from_id(final_id)
            
            if full_info:
                return jsonify({
                    "status": "success",
                    "credit": CREDIT,
                    "developer": DEVELOPER,
                    "method": method,
                    "query_id": final_id,
                    "query_time_ms": round((time.time() - start_time) * 1000, 2),
                    "data": full_info
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": f"No OSINT data found for ID: {final_id}",
                    "credit": CREDIT
                }), 404
        else:
            return jsonify({
                "status": "error",
                "message": "Could not process request",
                "credit": CREDIT
            }), 500
            
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
        "chatid_api": CHATID_API,
        "backend_api": TG_BACKEND
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
