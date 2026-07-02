from flask import Flask, request, jsonify
import requests
import time
import json

app = Flask(__name__)

CREDIT = "BRONX_ULTRA"
DEVELOPER = "BRONX_ULTRA"
VALID_KEYS = ["BRONXop", "BRONXdemo", "BRONX2026"]

# ✅ UPDATED APIs
USERNAME_TO_ID_API = "https://www.gettg.id/api/search"
TG_ID_TO_NUM_API = "https://tgid2num.suryajasoos.workers.dev/"
NUMBER_DETAILS_API = "https://bronx-web-api.onrender.com/api/key-bronx/number"
NUMBER_API_KEY = "op"

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
        # STEP 1: Get User ID from username
        tg_info = None
        user_id = None
        
        if clean.isdigit():
            user_id = clean
        else:
            try:
                resp = requests.get(f"{USERNAME_TO_ID_API}?username={clean}", timeout=60)
                data = resp.json()
                
                if data.get("status") == "success":
                    user_data_str = data.get("data")
                    if user_data_str:
                        user_data = json.loads(user_data_str)
                        user_id = str(user_data.get("id"))
                        
                        # ✅ CLEAN TG INFO - Sirf important fields
                        tg_info = {
                            "id": user_data.get("id"),
                            "username": f"@{user_data.get('username', clean)}",
                            "first_name": user_data.get("first_name", ""),
                            "last_name": user_data.get("last_name", ""),
                            "verified": user_data.get("verified", False),
                            "premium": user_data.get("premium", False),
                            "bot": user_data.get("bot", False)
                        }
            except Exception as e:
                print(f"Username to ID API error: {e}")
                pass
        
        if not user_id:
            return jsonify({"status": "error", "message": "User not found", "credit": CREDIT}), 404
        
        # STEP 2: Get Phone Number
        phone = None
        tg_api_info = None
        
        try:
            url = f"{TG_ID_TO_NUM_API}?q={user_id}"
            resp = requests.get(url, timeout=30)
            data = resp.json()
            
            if data.get("status") == True and data.get("data"):
                source1 = data["data"].get("source1", {})
                records = source1.get("records", [])
                
                if records and len(records) > 0:
                    record = records[0]
                    phone = record.get("phone")
                    tg_api_info = {
                        "country": record.get("country", "India"),
                        "country_code": record.get("country_code", "+91"),
                        "number": phone
                    }
        except Exception as e:
            print(f"TG ID to Number API Error: {e}")
            pass
        
        if not phone:
            return jsonify({
                "status": "success",
                "credit": CREDIT,
                "developer": DEVELOPER,
                "query": clean,
                "user_id": user_id,
                "tg_info": tg_info,
                "tg_number_info": {"success": False, "message": "No Data Found"},
                "phone_info": {"success": False, "message": "No Data Found"},
                "number_details": {"success": False, "message": "No Data Found"},
                "query_time_ms": round((time.time() - t0) * 1000, 2)
            })
        
        # STEP 3: Get Number Details
        number_details = None
        
        try:
            clean_phone = str(phone).replace("+91", "").replace(" ", "").strip()
            url = f"{NUMBER_DETAILS_API}?key={NUMBER_API_KEY}&num={clean_phone}"
            
            resp = requests.get(url, timeout=30)
            data = resp.json()
            
            if data.get("success") and data.get("results"):
                # ✅ CLEAN RESULTS - Sirf important fields
                cleaned_results = []
                for result in data.get("results", [])[:5]:  # Sirf top 5
                    cleaned_result = {}
                    # Sirf yeh fields lo
                    for k in ["mobile", "name", "address", "circle", "email", "truecaller_name"]:
                        if k in result:
                            cleaned_result[k] = result[k]
                    cleaned_results.append(cleaned_result)
                
                number_details = {
                    "success": True,
                    "total": data.get("total", 0),
                    "results": cleaned_results
                }
            else:
                number_details = {"success": False, "message": "No Data Found"}
        except Exception as e:
            print(f"Number details API error: {e}")
            number_details = {"success": False, "message": "API error"}
        
        # ✅ FINAL RESPONSE - Clean aur organized
        response = {
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
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "credit": CREDIT}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
