/* script.js */

// --- CONFIGURATION ---
const CONFIG = {
    user: "REHAN",          // Username
    pass: "123",            // Password
    expiryDate: "2026-12-30" // YYYY-MM-DD (Expiry Set Karo)
};

// --- LOGIN CHECK ---
function checkLogin() {
    const isLogged = localStorage.getItem("isLogged");
    const expiry = new Date(CONFIG.expiryDate);
    const now = new Date();

    if (!isLogged) {
        window.location.href = "index.html";
    } else if (now > expiry) {
        alert("⛔ ACCOUNT EXPIRED! Contact Admin.");
        logout();
    }
}

function doLogin() {
    const u = document.getElementById('usr').value;
    const p = document.getElementById('pwd').value;
    const msg = document.getElementById('msg');

    if (u === CONFIG.user && p === CONFIG.pass) {
        const now = new Date();
        const expiry = new Date(CONFIG.expiryDate);
        if (now > expiry) {
            msg.innerText = "⛔ ID EXPIRED on " + CONFIG.expiryDate;
            msg.style.color = "red";
            return;
        }
        localStorage.setItem("isLogged", "true");
        window.location.href = "dashboard.html";
    } else {
        msg.innerText = "❌ WRONG PASSWORD";
        msg.style.color = "red";
    }
}

function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}

// --- COPY FUNCTION ---
function copyText() {
    const txt = document.getElementById('resultArea').innerText;
    navigator.clipboard.writeText(txt).then(() => alert("✅ COPIED!"));
}

// ================= API FUNCTIONS =================

// 1. NUMBER INFO (Blue Theme)
async function fetchNumber() {
    const num = document.getElementById('inp').value;
    const resBox = document.getElementById('resultArea');
    const btn = document.getElementById('sBtn');
    
    if(!num) return alert("Enter Number!");
    
    btn.innerText = "SEARCHING...";
    resBox.style.display = "block";
    resBox.innerHTML = "🔍 Scanning Database...";

    try {
        const req = await fetch(`https://bronx-api-sable.vercel.app/search?num=${num}&key=bronx-api`);
        const data = await req.json();

        // FORMAT
        const txt = `
🔍...... 𝗥𝗘𝗖𝗢𝗥𝗗 
├─ 👤 𝗡𝗮𝗺𝗲: ${data.name || "N/A"}
├─ 📱 𝗠𝗼𝗯𝗶𝗹𝗲: ${data.mobile || num}
├─ 🧑‍🦳 𝗙𝗮𝘁𝗵𝗲𝗿: ${data.fname || "N/A"}
├─ 🏠 𝗔𝗱𝗱𝗿𝗲𝘀𝘀: ${data.address || "N/A"}
├─ 🌍 𝗖𝗶𝗿𝗰𝗹𝗲: ${data.circle || "N/A"}
├─ 🆔 𝗜𝗗: ${data.id || "N/A"}
└─ 📧 𝗘𝗺𝗮𝗶𝗹: ${data.email || "N/A"}
`;
        resBox.innerText = txt;
        document.getElementById('cpBtn').style.display = "block";
    } catch (e) { resBox.innerText = "❌ Error or Not Found"; }
    btn.innerText = "SEARCH 🔍";
}

// 2. VEHICLE INFO (Red Theme)
async function fetchVehicle() {
    const rc = document.getElementById('inp').value;
    const resBox = document.getElementById('resultArea');
    const btn = document.getElementById('sBtn');
    
    if(!rc) return alert("Enter RC Number!");
    
    btn.innerText = "CONNECTING...";
    resBox.style.display = "block";
    resBox.innerHTML = "🛰️ Connecting to Satellite...";

    try {
        const req = await fetch(`https://bronx-rc-api.vercel.app/?rc_number=${rc}`);
        const json = await req.json();
        
        if(json.status === "success" && json.details) {
            const d = json.details;
            const txt = `
◤━━━━━━━━━━━━━━━━━━━━◥
      🏎️ 𝗩𝗘𝗛𝗜𝗖𝗟𝗘 𝗜𝗡𝗙𝗢 𝗩𝗜𝗣 ⚡
◢◤◢◤◢◤◢◤◢◤◢◤◢◤
╔══════════════════════╗
  🎯 Target RC: ${json.rc_number || rc}
╚══════════════════════╝

 ⭐ OWNER DETAILS ⭐
👤 Owner: ${d["Owner Name"] || ""}
🧑‍🦳 Father: ${d["Father's Name"] || ""}
📱 Phone: ${d["Phone"] || ""}
🏠 Address: ${d["Address"] || ""}
📍 City: ${d["City Name"] || ""}
🔢 Serial: ${d["Owner Serial No"] || ""}

 ⭐ VEHICLE SPECS ⭐
🚘 Maker: ${d["Maker Model"] || ""}
🚜 Class: ${d["Vehicle Class"] || ""}
⛽ Fuel: ${d["Fuel Type"] || ""}
🗓️ Reg Date: ${d["Registration Date"] || ""}
🏛️ RTO: ${d["Registered RTO"] || ""}

 ⭐ LEGAL & VALIDITY ⭐
🏥 Insurer: ${d["Insurance Company"] || ""}
📅 Ins. Upto: ${d["Insurance Upto"] || ""}
💨 PUC Upto: ${d["PUC Upto"] || ""}
🛠️ Fitness: ${d["Fitness Upto"] || ""}
💸 Tax Upto: ${d["Tax Upto"] || ""}
━━━━━━━━━━━━━━━━━━━━`;
            resBox.innerText = txt;
            document.getElementById('cpBtn').style.display = "block";
        } else { resBox.innerText = "❌ No Data Found"; }
    } catch (e) { resBox.innerText = "❌ API Error"; }
    btn.innerText = "SEARCH 🔍";
}

// 3. ADHAR INFO (Green Theme)
async function fetchAdhar() {
    const uid = document.getElementById('inp').value;
    const resBox = document.getElementById('resultArea');
    const btn = document.getElementById('sBtn');

    if(!uid) return alert("Enter Adhar Number!");

    btn.innerText = "WAIT...";
    resBox.style.display = "block";
    resBox.innerHTML = "🔄 Fetching UIDAI Data...";

    try {
        // Assuming API URL structure based on your input
        const req = await fetch(`https://bronx-adhar-api.vercel.app/aadhar=${uid}`);
        const data = await req.json();

        const txt = `
├─ 🆔 𝗜𝗗: ${data.id || uid}
├─ 👤 𝗡𝗮𝗺𝗲: ${data.name || "N/A"}
├─ 🧑‍🦳 𝗙𝗮𝘁𝗵𝗲𝗿: ${data.fname || "N/A"}
├─ 📱 𝗠𝗼𝗯𝗶𝗹𝗲: ${data.mobile || "N/A"}
├─ 🏠 𝗔𝗱𝗱𝗿𝗲𝘀𝘀: ${data.address || "N/A"}
├─ 📧 𝗘𝗺𝗮𝗶𝗹: ${data.email || "N/A"}
└─ 🔄 𝗔𝗹𝘁 𝗡𝘂𝗺: ${data.alt || "N/A"}
`;
        resBox.innerText = txt;
        document.getElementById('cpBtn').style.display = "block";
    } catch (e) { resBox.innerText = "❌ Error: API Down or Invalid ID"; }
    btn.innerText = "SEARCH 🔍";
}

// 4. MAIL INFO (Gold Theme)
async function fetchMail() {
    const mail = document.getElementById('inp').value;
    const resBox = document.getElementById('resultArea');
    const btn = document.getElementById('sBtn');

    if(!mail) return alert("Enter Email!");

    btn.innerText = "HACKING...";
    resBox.style.display = "block";
    resBox.innerHTML = "📂 Opening Mail Database...";

    try {
        const req = await fetch(`https://bronx-mail-api.vercel.app/mail=${mail}`);
        const json = await req.json();
        
        // Handling Array response
        const data = (json.results && json.results[0]) ? json.results[0] : {};

        const txt = `
├─ 📧 𝗘𝗺𝗮𝗶𝗹: ${data.email || mail}
├─ 👤 𝗡𝗮𝗺𝗲: ${data.name || "N/A"}
├─ 🧑‍🦳 𝗙𝗮𝘁𝗵𝗲𝗿: ${data.fname || "N/A"}
├─ 📱 𝗠𝗼𝗯𝗶𝗹𝗲: ${data.mobile || "N/A"}
├─ 🆔 𝗜𝗗: ${data.id || "N/A"}
├─ 🏠 𝗔𝗱𝗱𝗿𝗲𝘀𝘀: ${data.address || "N/A"}
└─ 🔄 𝗔𝗹𝘁 𝗡𝘂𝗺: ${data.alt || "N/A"}
`;
        resBox.innerText = txt;
        document.getElementById('cpBtn').style.display = "block";
    } catch (e) { resBox.innerText = "❌ No Record Found"; }
    btn.innerText = "SEARCH 🔍";
}
