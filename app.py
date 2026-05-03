from flask import Flask, request, jsonify, render_template_string
import requests
import time

app = Flask(__name__)

# --- CONFIGURATION ---
OWNER_TAG = "@BRONX_ULTRA"
CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"

# Valid API Keys
VALID_KEYS = ["BRONXop", "BRONXdemo", "BRONX2026"]

# APIs
ULTRA_API = "https://god-bronx.onrender.com/ultra"  # For ID + Profile
TG_NUMBER_API_1 = "https://api.subhxcosmo.in/api"  # For Phone Number
TG_NUMBER_API_2 = "https://num-tg-info-api.vercel.app/"  # Backup Phone
NUMBER_API = "https://ft-osint-api.duckdns.org/api/number"  # Full Details

# --- HTML ---
HTML = """
<!DOCTYPE html><html><head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1.0'>
<title>BRONX ULTRA GOD API</title>
<style>
body{background:#000;color:#bf00ff;font-family:monospace;text-align:center;padding:30px}
h1{font-size:2em;background:linear-gradient(135deg,#bf00ff,#f06);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.url{background:#111;padding:15px;border-radius:10px;color:#0f0;margin:10px 0;font-size:13px}
</style></head><body>
<h1>👑 BRONX ULTRA GOD API</h1>
<p style='color:#ccc'>Username → ID → Number → Full Details</p>
<div class='url'>/tg?key=KEY&query=@username</div>
<div class='url'>/tg?key=KEY&query=ID</div>
<p style='color:#555;margin-top:30px'>@BRONX_ULTRA | v5.0</p>
</body></html>
"""

# ============================================
# STEP 1: Get ID from Ultra API
# ============================================
def get_user_id(username):
    try:
        clean = username.replace("@", "").strip()
        resp = requests.get(f"{ULTRA_API}?q={clean}", timeout=15)
        data = resp.json()
        if data.get("status") == "success" and data.get("id"):
            return {
                "success": True,
                "user_id": str(data["id"]),
                "username": data.get("username"),
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "bio": data.get("bio", ""),
                "premium": data.get("premium", False),
                "verified": data.get("verified", False),
                "account_age": data.get("account_age"),
                "online_status": data.get("online_status"),
                "profile_photo": data.get("profile_photo"),
                "phone": data.get("phone")  # May be null
            }
        return {"success": False}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============================================
# STEP 2: Get Phone Number from TG APIs
# ============================================
def get_phone_number(query):
    """Try multiple APIs to get phone number"""
    
    # Try API 1: subhxcosmo
    try:
        resp = requests.get(f"{TG_NUMBER_API_1}?key=RACK2&type=tg&term={query}", timeout=15)
        data = resp.json()
        if data.get("success") and data.get("result", {}).get("number"):
            return {
                "success": True,
                "number": data["result"]["number"],
                "country_code": data["result"].get("country_code", "+91"),
                "country": data["result"].get("country", "India"),
                "source": "api1"
            }
    except:
        pass
    
    # Try API 2: num-tg-info
    try:
        resp = requests.get(f"https://num-tg-info-api.vercel.app/?id={query}", timeout=15)
        data = resp.json()
        if data.get("SUCCESS") and data.get("RESULT", {}).get("NUMBER_INFO", {}).get("NUMBER"):
            return {
                "success": True,
                "number": data["RESULT"]["NUMBER_INFO"]["NUMBER"],
                "country_code": data["RESULT"]["NUMBER_INFO"].get("COUNTRY_CODE", "+91"),
                "country": data["RESULT"]["NUMBER_INFO"].get("COUNTRY", "India"),
                "source": "api2"
            }
    except:
        pass
    
    return {"success": False, "message": "No phone number found"}

# ============================================
# STEP 3: Get Full Details from Number
# ============================================
def get_number_details(phone):
    try:
        clean = str(phone).replace("+91", "").replace(" ", "").strip()
        resp = requests.get(f"{NUMBER_API}?key=bronx&num={clean}", timeout=20)
        data = resp.json()
        
        if data.get("success") and data.get("results"):
            results = []
            for r in data["results"]:
                results.append({
                    "name": r.get("name", ""),
                    "father_name": r.get("father_name", ""),
                    "address": r.get("address", ""),
                    "circle": r.get("circle", ""),
                    "mobile": r.get("mobile", ""),
                    "alternate": r.get("alternate", ""),
                    "aadhar": r.get("aadhar", ""),
                    "email": r.get("email", "")
                })
            return {"success": True, "count": data.get("total", len(results)), "results": results}
        return {"success": False, "message": "No details found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

# ============================================
# ROUTES
# ============================================
@app.route('/')
def home():
    return HTML

@app.route('/tg')
def tg_lookup():
    t0 = time.time()
    
    # Check Key
    key = request.args.get('key', '').strip()
    if key not in VALID_KEYS:
        return jsonify({"status": "error", "message": "Invalid API Key"}), 403
    
    # Get Query
    q = request.args.get('query', '') or request.args.get('username', '') or request.args.get('id', '')
    q = q.strip().replace("@", "")
    
    if not q:
        return jsonify({"status": "error", "message": "Missing query"}), 400
    
    # ============================================
    # CHAIN START
    # ============================================
    result = {
        "status": "success",
        "credit": CREDIT,
        "developer": DEVELOPER,
        "query": q
    }
    
    # STEP 1: Get User ID + Profile
    ultra = get_user_id(q)
    
    if not ultra.get("success"):
        return jsonify({"status": "error", "message": f"User not found: {q}"}), 404
    
    user_id = ultra["user_id"]
    
    result["user_info"] = {
        "id": user_id,
        "username": ultra.get("username"),
        "first_name": ultra.get("first_name"),
        "last_name": ultra.get("last_name"),
        "bio": ultra.get("bio"),
        "premium": ultra.get("premium"),
        "verified": ultra.get("verified"),
        "online_status": ultra.get("online_status"),
        "account_age": ultra.get("account_age"),
        "profile_photo": ultra.get("profile_photo")
    }
    
    # STEP 2: Get Phone Number
    phone = ultra.get("phone")
    phone_result = None
    
    if not phone:
        # Try with user ID
        phone_result = get_phone_number(user_id)
        # Also try with username
        if not phone_result.get("success"):
            phone_result = get_phone_number(q)
    else:
        phone_result = {"success": True, "number": phone, "source": "ultra_api"}
    
    if phone_result.get("success"):
        phone_number = phone_result["number"]
        result["phone_info"] = {
            "number": phone_number,
            "country_code": phone_result.get("country_code", "+91"),
            "country": phone_result.get("country", "India"),
            "source": phone_result.get("source", "unknown")
        }
        
        # STEP 3: Get Full Details
        details = get_number_details(phone_number)
        if details.get("success"):
            result["number_details"] = {
                "success": True,
                "count": details["count"],
                "results": details["results"]
            }
        else:
            result["number_details"] = {
                "success": False,
                "message": details.get("message", "No details found"),
                "phone": phone_number
            }
    else:
        result["phone_info"] = {"success": False, "message": "No phone number found"}
        result["number_details"] = {"success": False, "message": "No phone number available"}
    
    result["query_time_ms"] = round((time.time() - t0) * 1000, 2)
    
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "credit": CREDIT})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
