from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# --- CONFIGURATION ---
CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"

VALID_KEYS = ["BRONXop", "BRONXdemo", "BRONX2026"]

# ✅ WORKING APIs ONLY
ULTRA_API = "https://god-bronx.onrender.com/ultra"
TG_API = "https://api.subhxcosmo.io/api"
NUMBER_API = "https://ft-osint-api.duckdns.org/api/number"

HTML = """
<h1 style='color:#bf00ff;text-align:center;padding:50px;background:#000;font-family:monospace;'>
👑 BRONX ULTRA GOD API<br>
<small style='color:#888;'>/tg?key=BRONXop&query=@username</small>
</h1>
"""

def get_phone_from_tg(query):
    """Get phone from TG API"""
    try:
        url = f"{TG_API}?key=RACK2&type=tg&term={query}"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if data.get("success") and data.get("result", {}).get("number"):
            return data["result"]["number"]
    except:
        pass
    return None

def get_number_details(phone):
    """Get full details from number"""
    try:
        clean = str(phone).replace("+91", "").replace(" ", "").strip()
        url = f"{NUMBER_API}?key=bronx&num={clean}"
        resp = requests.get(url, timeout=20)
        data = resp.json()
        if data.get("success") and data.get("results"):
            results = []
            for r in data["results"]:
                results.append({
                    "name": r.get("name", ""),
                    "father": r.get("father_name", ""),
                    "address": r.get("address", ""),
                    "circle": r.get("circle", ""),
                    "mobile": r.get("mobile", ""),
                    "alt": r.get("alternate", ""),
                    "aadhar": r.get("aadhar", ""),
                    "email": r.get("email", "")
                })
            return {"success": True, "count": len(results), "results": results}
    except:
        pass
    return {"success": False, "message": "No details found"}

@app.route('/')
def home():
    return HTML

@app.route('/tg')
def tg():
    t0 = time.time()
    
    # Check key
    key = request.args.get('key', '').strip()
    if key not in VALID_KEYS:
        return jsonify({"status": "error", "message": "Invalid API Key", "credit": CREDIT}), 403
    
    # Get input
    q = request.args.get('query', '') or request.args.get('username', '') or request.args.get('id', '')
    clean = q.strip().replace("@", "")
    
    if not clean:
        return jsonify({"status": "error", "message": "Missing query", "credit": CREDIT}), 400
    
    try:
        # STEP 1: Ultra API → User ID + Profile
        ultra_resp = requests.get(f"{ULTRA_API}?q={clean}", timeout=20)
        ultra = ultra_resp.json()
        
        if ultra.get("status") != "success":
            return jsonify({"status": "error", "message": f"User not found: {clean}", "credit": CREDIT}), 404
        
        user_id = ultra.get("id")
        
        # STEP 2: Phone Number
        phone = ultra.get("phone")  # Ultra se try
        
        if not phone:
            phone = get_phone_from_tg(user_id)  # TG API with ID
        
        if not phone:
            phone = get_phone_from_tg(clean)  # TG API with username
        
        # STEP 3: Number Details
        number_details = None
        if phone:
            number_details = get_number_details(phone)
        
        # BUILD RESPONSE
        result = {
            "status": "success",
            "credit": CREDIT,
            "developer": DEVELOPER,
            "query": clean,
            "query_time_ms": round((time.time() - t0) * 1000, 2),
            "user_info": {
                "id": user_id,
                "username": ultra.get("username"),
                "first_name": ultra.get("first_name", ""),
                "last_name": ultra.get("last_name", ""),
                "bio": ultra.get("bio", ""),
                "premium": ultra.get("premium", False),
                "verified": ultra.get("verified", False),
                "online_status": ultra.get("online_status"),
                "account_age": ultra.get("account_age"),
                "profile_photo": ultra.get("profile_photo")
            },
            "phone_info": {
                "success": phone is not None,
                "number": phone
            } if phone else {"success": False, "message": "No phone number found"},
            "number_details": number_details if number_details else {"success": False, "message": "No phone number available"}
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "credit": CREDIT}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
