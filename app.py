from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"
VALID_KEYS = ["BRONXop", "BRONXdemo", "BRONX2026"]

# ✅ UPDATED APIs
ULTRA_API = "https://bronx-god-id-info.onrender.com/chatid"
TG_API = "https://shivm-ultra-api.vercel.app/tg"
TG_KEY = "Y"
NUMBER_API = "https://num-bala-api-ha-babujiiii.vercel.app/api/number"

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
    
    key = request.args.get('key', '').strip()
    if key not in VALID_KEYS:
        return jsonify({"status": "error", "message": "Invalid API Key", "credit": CREDIT}), 403
    
    q = request.args.get('query', '') or request.args.get('username', '') or request.args.get('id', '')
    clean = q.strip().replace("@", "")
    
    if not clean:
        return jsonify({"status": "error", "message": "Missing query", "credit": CREDIT}), 400
    
    try:
        # STEP 1: Get TG Info + User ID
        tg_info = None
        user_id = None
        
        if clean.isdigit():
            user_id = clean
        else:
            try:
                resp = requests.get(f"{ULTRA_API}?username={clean}", timeout=60)
                data = resp.json()
                if data.get("status") == "success":
                    user_id = str(data.get("chat_id"))
                    tg_info = {
                        "username": f"@{data.get('username', clean)}",
                        "first_name": data.get("first_name", ""),
                        "last_name": data.get("last_name", ""),
                        "type": data.get("type", "user")
                    }
            except:
                pass
        
        if not user_id:
            return jsonify({"status": "error", "message": "User not found", "credit": CREDIT}), 404
        
        # STEP 2: Get Phone Number from NEW TG API
        phone = None
        tg_api_info = None
        
        try:
            url = f"{TG_API}?key={TG_KEY}&id={user_id}"
            resp = requests.get(url, timeout=30)
            data = resp.json()
            
            if data.get("success") and data.get("data"):
                inner = data["data"]
                phone = inner.get("number")
                # ✅ ONLY these 3 fields - Hide owner/powered_by
                tg_api_info = {
                    "country": inner.get("country", "India"),
                    "country_code": inner.get("country_code", "+91"),
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
                "phone_info": {"success": False, "message": "No Data Found"},
                "number_details": {"success": False, "message": "No Data Found"},
                "query_time_ms": round((time.time() - t0) * 1000, 2)
            })
        
        # STEP 3: Get Number Details
        number_details = None
        
        try:
            clean_phone = str(phone).replace("+91", "").replace(" ", "").strip()
            resp = requests.get(f"{NUMBER_API}?num={clean_phone}", timeout=30)
            data = resp.json()
            
            if data:
                cleaned_data = {}
                for k, v in data.items():
                    if k not in ["by", "channel", "developer", "owner", "credit", "BUY", "DEVELOPER", "powered_by"]:
                        cleaned_data[k] = v
                
                number_details = {"success": True, "data": cleaned_data}
            else:
                number_details = {"success": False, "message": "No Data Found"}
        except:
            number_details = {"success": False, "message": "API error"}
        
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
        return jsonify({"status": "error", "message": str(e), "credit": CREDIT}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
