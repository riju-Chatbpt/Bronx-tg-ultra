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
ULTRA_API = "https://god-bronx.onrender.com/ultra"  # NEW Ultra API (Chat ID + Number)
TG_BACKEND = "https://num-tg-info-api.vercel.app/"  # OLD TG Backend
TG_BACKEND_2 = "https://api.subhxcosmo.in/api"  # NEW TG Backend
NUMBER_API = "https://ft-osint-api.duckdns.org/api/number"  # Number Details API

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
            📌 <b>Username → Full Chain:</b><br>
            /tg?key=key&query=@username
        </div>
        <div class="url">
            📌 <b>ID → Full Chain:</b><br>
            /tg?key=key&query=7530266953
        </div>
        
        <footer>Developed by {{ owner }} | GOD LEVEL API v4.0</footer>
    </div>
</body>
</html>
"""

def check_key(api_key):
    if not api_key:
        return False
    return api_key in VALID_KEYS

def is_numeric_id(value):
    clean = value.replace("@", "").strip()
    try:
        int(clean)
        return True
    except:
        return False

def get_ultra_info(query):
    """STEP 1: Ultra API se ID aur Number nikalo"""
    try:
        clean = query.replace("@", "").strip()
        url = f"{ULTRA_API}?q={clean}"
        resp = requests.get(url, timeout=20)
        data = resp.json()
        
        if data.get("status") == "success":
            user_id = data.get("id")
            phone = data.get("phone")
            username = data.get("username")
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")
            premium = data.get("premium", False)
            verified = data.get("verified", False)
            bio = data.get("bio", "")
            online_status = data.get("online_status", "")
            account_age = data.get("account_age")
            profile_photo = data.get("profile_photo")
            language = data.get("language")
            restricted = data.get("restricted", False)
            scam = data.get("scam", False)
            fake = data.get("fake", False)
            stories_count = data.get("stories_count", 0)
            premium_since = data.get("premium_since")
            common_chats = data.get("common_chats_count", 0)
            
            return {
                "success": True,
                "user_id": user_id,
                "phone_number": phone,
                "tg_data": {
                    "basic_info": {
                        "id": user_id,
                        "first_name": first_name,
                        "last_name": last_name,
                        "username": username,
                        "bio": bio,
                        "premium": premium,
                        "verified": verified,
                        "scam": scam,
                        "fake": fake,
                        "restricted": restricted,
                        "language": language
                    },
                    "status_info": {
                        "online_status": online_status,
                        "is_active": True
                    },
                    "activity_info": {
                        "account_age": account_age,
                        "stories_count": stories_count,
                        "premium_since": premium_since,
                        "common_chats": common_chats,
                        "profile_photo": profile_photo
                    },
                    "number_info": {
                        "number": phone,
                        "country_code": "+91" if phone and len(phone) == 10 else None,
                        "country": "India" if phone and len(phone) == 10 else None
                    }
                }
            }
        return {"success": False, "message": "No data from Ultra API"}
    except Exception as e:
        print(f"Ultra API Error: {e}")
        return {"success": False, "message": str(e)}

def get_tg_info_new(query):
    """STEP 1 FALLBACK: NEW TG Backend se Info"""
    try:
        url = f"{TG_BACKEND_2}?key=RACK2&type=tg&term={query}"
        resp = requests.get(url, timeout=20)
        data = resp.json()
        
        if data.get("success") == True:
            result = data.get("result", {})
            phone_number = result.get("number", "")
            
            return {
                "success": True,
                "phone_number": phone_number,
                "user_id": result.get("tg_id", query),
                "tg_data": {
                    "basic_info": {
                        "id": result.get("tg_id", query),
                        "first_name": None,
                        "last_name": None,
                        "username": None,
                        "bio": None
                    },
                    "status_info": {"is_active": True},
                    "activity_info": {},
                    "number_info": {
                        "number": phone_number,
                        "country_code": result.get("country_code", "+91"),
                        "country": result.get("country", "India")
                    }
                }
            }
        return {"success": False, "message": "No TG data found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_number_details_new(phone_number):
    """STEP 2: Number se Full Details"""
    try:
        # Remove country code if present
        clean_num = phone_number.replace("+91", "").replace(" ", "").strip()
        url = f"{NUMBER_API}?key=bronx&num={clean_num}"
        resp = requests.get(url, timeout=20)
        data = resp.json()
        
        if data.get("success") == True:
            results = data.get("results", [])
            cleaned_results = []
            for r in results:
                cleaned_results.append({
                    "name": r.get("name", ""),
                    "fname": r.get("father_name", ""),
                    "address": r.get("address", ""),
                    "circle": r.get("circle", ""),
                    "mobile": r.get("mobile", ""),
                    "alt": r.get("alternate", ""),
                    "aadhar": r.get("aadhar", ""),
                    "email": r.get("email", ""),
                    "truecaller_name": r.get("truecaller_name")
                })
            
            return {
                "success": True,
                "count": data.get("total", len(cleaned_results)),
                "results": cleaned_results
            }
        return {"success": False, "message": "No number data found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.route('/')
def home():
    return render_template_string(DASHBOARD_HTML, host=request.host, owner=OWNER_TAG)

@app.route('/tg')
def god_lookup():
    start_time = time.time()
    
    api_key = request.args.get('key', '').strip()
    
    if not check_key(api_key):
        return jsonify({
            "status": "error",
            "message": "❌ Invalid or Missing API Key! Contact @BRONX_ULTRA",
            "usage": "/tg?key=BRONXop&query=@username"
        }), 403
    
    username = request.args.get('username', '').strip()
    user_id = request.args.get('id', '').strip()
    query = request.args.get('query', '').strip()
    
    if not username and not user_id and not query:
        return jsonify({
            "status": "error",
            "message": "Missing 'username', 'id', or 'query' parameter"
        }), 400
    
    try:
        query_input = username or user_id or query
        clean = query_input.replace("@", "").strip()
        
        # ============================================
        # ✅ FIXED: Better detection
        # ============================================
        tg_result = None
        
        # Always try Ultra API first for usernames
        if not clean.isdigit():
            # It's a username → Ultra API
            tg_result = get_ultra_info(clean)
        else:
            # It's a numeric ID → Try Ultra API, then fallback
            tg_result = get_ultra_info(clean)
            if not tg_result.get("success"):
                tg_result = get_tg_info_new(clean)
        
        # If still no result, try TG Backend 2
        if not tg_result or not tg_result.get("success"):
            tg_result = get_tg_info_new(clean)
        
        if not tg_result or not tg_result.get("success"):
            return jsonify({
                "status": "error",
                "message": f"Could not fetch Telegram info for: @{clean}",
                "credit": CREDIT
            }), 404
        
        phone_number = tg_result.get("phone_number", "")
        
        # ============================================
        # CHAIN STEP 2: Get Number Details
        # ============================================
        number_result = None
        if phone_number and len(str(phone_number)) >= 10:
            number_result = get_number_details_new(phone_number)
        
        # ============================================
        # BUILD FINAL RESPONSE
        # ============================================
        output = {
            "status": "success",
            "credit": CREDIT,
            "developer": DEVELOPER,
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
                "message": "Phone number found but no additional details available",
                "phone": phone_number
            }
        else:
            output["number_details"] = {
                "success": False,
                "message": "No phone number found in Telegram data"
            }
        
        return jsonify(output)
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}", "credit": CREDIT}), 500

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "credit": CREDIT,
        "chain": "Username → Ultra API → Number → Number Details",
        "services": {
            "ultra_api": ULTRA_API,
            "tg_backend_2": TG_BACKEND_2,
            "number_api": NUMBER_API
        }
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
