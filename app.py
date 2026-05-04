from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"
VALID_KEYS = ["BRONXop", "BRONXdemo", "BRONX2026"]

# APIs
ULTRA_API = "https://god-bronx.onrender.com/ultra"
TG_API = "https://api.subhxcosmo.in/api"
NUMBER_API = "https://ft-osint-api.duckdns.org/api/number"

HTML = """
<h1 style='color:#bf00ff;text-align:center;padding:50px;background:#000;font-family:monospace;'>
👑 BRONX ULTRA GOD API<br>
<small style='color:#888;'>/tg?key=key&query=@username OR /tg?key=key&query=ID</small>
</h1>
"""

@app.route('/')
def home():
    return HTML

@app.route('/tg')
def tg():
    t0 = time.time()
    
    # Check Key
    key = request.args.get('key', '').strip()
    if key not in VALID_KEYS:
        return jsonify({"status": "error", "message": "Invalid API Key", "credit": CREDIT}), 403
    
    # Get Input
    q = request.args.get('query', '') or request.args.get('username', '') or request.args.get('id', '')
    clean = q.strip().replace("@", "")
    
    if not clean:
        return jsonify({"status": "error", "message": "Missing query", "credit": CREDIT}), 400
    
    try:
        # ============================================
        # STEP 1: Get TG Info + User ID
        # ============================================
        tg_info = None
        user_id = None
        
        if clean.isdigit():
            user_id = clean
        else:
            try:
                resp = requests.get(f"{ULTRA_API}?q={clean}", timeout=60)
                data = resp.json()
                if data.get("status") == "success":
                    user_id = str(data.get("id"))
                    tg_info = {
                        "username": data.get("username"),
                        "first_name": data.get("first_name", ""),
                        "last_name": data.get("last_name", ""),
                        "bio": data.get("bio", ""),
                        "premium": data.get("premium", False),
                        "verified": data.get("verified", False),
                        "online_status": data.get("online_status"),
                        "account_age": data.get("account_age"),
                        "profile_photo": data.get("profile_photo")
                    }
            except:
                pass
        
        if not user_id:
            return jsonify({
                "status": "error",
                "message": "User not found",
                "credit": CREDIT
            }), 404
        
        # ============================================
        # STEP 2: Get Phone Number from TG API
        # ============================================
        phone = None
        tg_api_info = None
        
        try:
            resp = requests.get(f"{TG_API}?key=RACK2&type=tg&term={user_id}", timeout=30)
            data = resp.json()
            
            # ✅ TG API FULL INFO
            if data.get("success") and data.get("result"):
                result = data["result"]
                phone = result.get("number")
                tg_api_info = {
                    "success": result.get("success", True),
                    "msg": result.get("msg", "Details fetched"),
                    "tg_id": result.get("tg_id", user_id),
                    "country": result.get("country", "India"),
                    "country_code": result.get("country_code", "+91"),
                    "number": phone
                }
        except:
            pass
        
        if not phone:
            return jsonify({
                "status": "success",
                "credit": CREDIT,
                "developer": DEVELOPER,
                "query": clean,
                "user_id": user_id,
                "tg_info": tg_info,
                "tg_number_info": tg_api_info if tg_api_info else {"success": False, "message": "No Data Found"},
                "phone_info": {"success": False, "message": "No Data Found - Phone number not available"},
                "number_details": {"success": False, "message": "No Data Found - No phone number to lookup"},
                "query_time_ms": round((time.time() - t0) * 1000, 2)
            })
        
        # ============================================
        # STEP 3: Get Number Details
        # ============================================
        number_details = None
        
        try:
            clean_phone = str(phone).replace("+91", "").replace(" ", "").strip()
            resp = requests.get(f"{NUMBER_API}?key=bronx&num={clean_phone}", timeout=30)
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
                        "alternate": r.get("alternate", ""),
                        "aadhar": r.get("aadhar", ""),
                        "email": r.get("email", "")
                    })
                number_details = {"success": True, "count": len(results), "results": results}
            else:
                number_details = {"success": False, "message": "No Data Found - No details available"}
        except:
            number_details = {"success": False, "message": "No Data Found - API error"}
        
        # ============================================
        # FINAL RESPONSE
        # ============================================
        return jsonify({
            "status": "success",
            "credit": CREDIT,
            "developer": DEVELOPER,
            "query": clean,
            "user_id": user_id,
            "tg_info": tg_info if tg_info else {"id": user_id},
            "tg_number_info": tg_api_info,
            "phone_info": {"success": True, "number": phone},
            "number_details": number_details,
            "query_time_ms": round((time.time() - t0) * 1000, 2)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "credit": CREDIT
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
