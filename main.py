import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import threading
import time

# ─────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="INSIGHT-X | Insider Threat Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar always visible fix
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    min-width: 270px !important;
    max-width: 270px !important;
    transform: translateX(0) !important;
    visibility: visible !important;
    display: block !important;
}
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
}
button[data-testid="baseButton-header"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg-primary:   #0a0c10;
    --bg-card:      #0f1218;
    --bg-card2:     #131720;
    --accent:       #00e5ff;
    --accent2:      #ff4c6a;
    --accent3:      #a78bfa;
    --text-primary: #e8eaf0;
    --text-muted:   #6b7280;
    --border:       rgba(0,229,255,0.12);
    --glow:         rgba(0,229,255,0.18);
    --red-glow:     rgba(255,76,106,0.18);
    --font-mono:    'Space Mono', monospace;
    --font-display: 'Syne', sans-serif;
}

html, body, .stApp {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
}

header[data-testid="stHeader"],
.stDeployButton, #MainMenu, footer,
[data-testid="stToolbar"], .stAppDeployButton {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

.stApp > header {
    background: transparent !important;
    border: none !important;
    height: 0 !important;
}

section[data-testid="stSidebar"] {
    background: #0b0d13 !important;
    border-right: 1px solid var(--border) !important;
}

section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

.sidebar-logo {
    padding: 28px 20px 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
}

.sidebar-logo .brand {
    font-family: var(--font-mono);
    font-size: 22px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 3px;
    text-shadow: 0 0 20px var(--accent), 0 0 40px rgba(0,229,255,0.4);
}

.sidebar-logo .tagline {
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 2px;
    margin-top: 4px;
    text-transform: uppercase;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,229,255,0.07);
    border: 1px solid rgba(0,229,255,0.2);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    color: var(--accent);
    font-family: var(--font-mono);
    margin: 12px 20px;
}

.status-dot {
    width: 6px;
    height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 6px var(--accent); }
    50% { opacity: 0.4; box-shadow: none; }
}

section[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
section[data-testid="stSidebar"] .stRadio label {
    color: var(--text-primary) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: background 0.2s !important;
    letter-spacing: 0.5px !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(0,229,255,0.07) !important;
    color: var(--accent) !important;
}

.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0.5;
}

.card-title {
    font-size: 11px;
    letter-spacing: 3px;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 8px;
    font-family: var(--font-mono);
}

.card-value { font-size: 36px; font-weight: 800; color: #e8eaf0; line-height: 1; }
.card-value.danger { color: var(--accent2); text-shadow: 0 0 20px var(--red-glow); }
.card-value.warn   { color: #fbbf24; }
.card-value.safe   { color: #34d399; }
.card-value.info   { color: var(--accent); }
.card-sub { font-size: 12px; color: var(--text-muted); margin-top: 6px; font-family: var(--font-mono); }

.section-header {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}

.section-title { font-size: 22px; font-weight: 800; color: var(--text-primary); letter-spacing: -0.5px; }
.section-badge {
    font-size: 10px;
    letter-spacing: 2px;
    color: var(--accent);
    font-family: var(--font-mono);
    background: rgba(0,229,255,0.08);
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid rgba(0,229,255,0.2);
}

.risk-critical {
    background: rgba(255,76,106,0.15);
    color: #ff4c6a;
    border: 1px solid rgba(255,76,106,0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 11px;
    font-family: var(--font-mono);
    font-weight: 700;
}
.risk-high {
    background: rgba(251,191,36,0.12);
    color: #fbbf24;
    border: 1px solid rgba(251,191,36,0.3);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 11px;
    font-family: var(--font-mono);
    font-weight: 700;
}
.risk-low {
    background: rgba(52,211,153,0.1);
    color: #34d399;
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 11px;
    font-family: var(--font-mono);
    font-weight: 700;
}

.alert-box {
    background: rgba(255,76,106,0.07);
    border: 1px solid rgba(255,76,106,0.25);
    border-left: 3px solid #ff4c6a;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 13px;
    color: #fca5a5;
    font-family: var(--font-mono);
    white-space: normal !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    overflow: visible !important;
    width: 100% !important;
    box-sizing: border-box !important;
}
.alert-box strong { color: #ff4c6a; }

/* ── ALERT CONFIG PANEL ── */
.alert-config-card {
    background: linear-gradient(135deg, #0f1218 0%, #0a0f16 100%);
    border: 1px solid rgba(255,76,106,0.25);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.alert-config-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #ff4c6a, #fbbf24, transparent);
}

/* ALERT LOG ITEM */
.log-item {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    padding: 12px 16px;
    border-radius: 10px;
    margin-bottom: 8px;
    border: 1px solid rgba(255,255,255,0.05);
    font-family: Space Mono, monospace;
    font-size: 12px;
}
.log-item.critical { background: rgba(255,76,106,0.07); border-left: 3px solid #ff4c6a; }
.log-item.high     { background: rgba(251,191,36,0.06); border-left: 3px solid #fbbf24; }
.log-sent   { color: #34d399; font-size: 10px; }
.log-failed { color: #ff4c6a; font-size: 10px; }

.behavior-tag {
    display: inline-block;
    background: rgba(167,139,250,0.1);
    border: 1px solid rgba(167,139,250,0.25);
    color: var(--accent3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 11px;
    margin: 3px;
    font-family: var(--font-mono);
}

.stDataFrame { border: 1px solid var(--border) !important; border-radius: 12px !important; overflow: hidden !important; }

.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--bg-card2) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: var(--font-mono) !important;
}

.stButton > button {
    background: transparent !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 10px !important;
    font-family: var(--font-mono) !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    color: #000 !important;
    box-shadow: 0 0 20px var(--glow) !important;
}

.divider { height: 1px; background: var(--border); margin: 20px 0; }

.timeline-item {
    display: flex;
    gap: 16px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.timeline-dot { width: 8px; height: 8px; border-radius: 50%; margin-top: 6px; flex-shrink: 0; }
.timeline-dot.critical { background: #ff4c6a; box-shadow: 0 0 8px #ff4c6a; }
.timeline-dot.warn     { background: #fbbf24; box-shadow: 0 0 8px #fbbf24; }
.timeline-dot.safe     { background: #34d399; box-shadow: 0 0 8px #34d399; }
.timeline-time { font-family: var(--font-mono); font-size: 11px; color: var(--text-muted); min-width: 80px; }
.timeline-desc { font-size: 13px; color: var(--text-primary); line-height: 1.5; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.2); border-radius: 4px; }

.stAlert > div {
    background: rgba(255,76,106,0.07) !important;
    border: 1px solid rgba(255,76,106,0.3) !important;
    border-radius: 12px !important;
    color: #fca5a5 !important;
}

[data-testid="stMetricValue"] { font-family: var(--font-mono) !important; font-size: 28px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
#  ALERT ENGINE
# ─────────────────────────────────────────

def send_gmail_alert(sender_email, sender_password, recipient_email, subject, body_html):
    """
    Sends an alert email via Gmail.
    Use a Gmail App Password (2FA must be enabled).
    """
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = sender_email
        msg["To"]      = recipient_email

        html_part = MIMEText(body_html, "html")
        msg.attach(html_part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)


def send_telegram_alert(bot_token, chat_id, message):
    """
    Sends a push notification via Telegram Bot to your phone.
    """
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id":    chat_id,
            "text":       message,
            "parse_mode": "HTML",
        }
        r = requests.post(url, json=payload, timeout=8)
        if r.status_code == 200:
            return True, "Telegram alert sent"
        else:
            return False, r.text
    except Exception as e:
        return False, str(e)


def build_email_html(employee_name, department, role, risk_score, reasons, triggered_by):
    """
    Builds a dark-themed cybersecurity-style HTML email template.
    """
    risk_color  = "#ff4c6a" if risk_score >= 80 else "#fbbf24"
    risk_label  = "CRITICAL" if risk_score >= 80 else "HIGH"
    reasons_html = "".join([f"<li style='margin:6px 0; color:#e8eaf0;'>⚑ {r}</li>" for r in reasons])
    timestamp   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="margin:0; padding:0; background:#0a0c10; font-family:'Courier New', monospace;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0c10; padding:40px 20px;">
            <tr><td align="center">
                <table width="580" style="background:#0f1218; border:1px solid rgba(255,76,106,0.3);
                       border-radius:16px; overflow:hidden;">

                    <!-- HEADER -->
                    <tr>
                        <td style="background:linear-gradient(135deg,#0f1218,#1a0a12);
                                   padding:30px 36px; border-bottom:2px solid {risk_color};">
                            <div style="font-size:11px; letter-spacing:4px; color:#6b7280; margin-bottom:6px;">
                                ⬡ INSIGHT-X SECURITY PLATFORM
                            </div>
                            <div style="font-size:26px; font-weight:700; color:{risk_color};
                                        letter-spacing:2px; text-shadow:0 0 20px {risk_color};">
                                🚨 {risk_label} THREAT DETECTED
                            </div>
                            <div style="font-size:11px; color:#6b7280; margin-top:6px;">
                                Alert fired: {timestamp}
                            </div>
                        </td>
                    </tr>

                    <!-- EMPLOYEE INFO -->
                    <tr>
                        <td style="padding:28px 36px;">
                            <table width="100%" style="background:#131720; border-radius:10px;
                                   border:1px solid rgba(255,255,255,0.05); padding:20px;
                                   border-collapse:collapse;">
                                <tr>
                                    <td style="padding:8px 16px;">
                                        <div style="font-size:10px; color:#6b7280; letter-spacing:2px;">EMPLOYEE</div>
                                        <div style="font-size:18px; font-weight:700; color:#e8eaf0;
                                                    margin-top:4px;">{employee_name}</div>
                                    </td>
                                    <td style="padding:8px 16px;">
                                        <div style="font-size:10px; color:#6b7280; letter-spacing:2px;">DEPARTMENT</div>
                                        <div style="font-size:14px; color:#e8eaf0; margin-top:4px;">{department}</div>
                                    </td>
                                    <td style="padding:8px 16px;">
                                        <div style="font-size:10px; color:#6b7280; letter-spacing:2px;">ROLE</div>
                                        <div style="font-size:14px; color:#e8eaf0; margin-top:4px;">{role}</div>
                                    </td>
                                    <td style="padding:8px 16px; text-align:center;">
                                        <div style="background:rgba(255,76,106,0.15); border:1px solid {risk_color};
                                                    border-radius:8px; padding:10px 16px; display:inline-block;">
                                            <div style="font-size:10px; color:#6b7280; letter-spacing:2px;">RISK SCORE</div>
                                            <div style="font-size:28px; font-weight:700; color:{risk_color};
                                                        margin-top:2px;">{risk_score}</div>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- TRIGGER REASON -->
                    <tr>
                        <td style="padding:0 36px 20px;">
                            <div style="background:rgba(255,76,106,0.08);
                                        border:1px solid rgba(255,76,106,0.2);
                                        border-left:3px solid {risk_color};
                                        border-radius:10px; padding:16px 20px;">
                                <div style="font-size:10px; letter-spacing:2px; color:#6b7280;
                                            margin-bottom:8px;">TRIGGERED BY</div>
                                <div style="color:#fca5a5; font-size:13px;">⚡ {triggered_by}</div>
                            </div>
                        </td>
                    </tr>

                    <!-- ALL RISK REASONS -->
                    <tr>
                        <td style="padding:0 36px 28px;">
                            <div style="font-size:10px; letter-spacing:2px; color:#6b7280; margin-bottom:12px;">
                                ALL RISK INDICATORS
                            </div>
                            <ul style="margin:0; padding-left:20px; color:#9ca3af; font-size:13px; line-height:1.8;">
                                {reasons_html}
                            </ul>
                        </td>
                    </tr>

                    <!-- FOOTER -->
                    <tr>
                        <td style="background:#080a0e; padding:20px 36px;
                                   border-top:1px solid rgba(255,255,255,0.05);">
                            <div style="font-size:10px; color:#374151; letter-spacing:1px;">
                                INSIGHT-X Automated Threat Detection · Do not reply to this email<br>
                                Take immediate action in the INSIGHT-X Control Panel → Actions tab
                            </div>
                        </td>
                    </tr>

                </table>
            </td></tr>
        </table>
    </body>
    </html>
    """


def build_telegram_message(employee_name, department, role, risk_score, reasons, triggered_by):
    """
    Builds a Telegram message with emojis in a readable format.
    Sends as a phone notification with vibration.
    """
    risk_label = "🔴 CRITICAL" if risk_score >= 80 else "🟡 HIGH RISK"
    reasons_text = "\n".join([f"  ⚑ {r}" for r in reasons])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""🚨 <b>INSIGHT-X THREAT ALERT</b>

{risk_label} — Score: <b>{risk_score}/100</b>

👤 <b>Employee:</b> {employee_name}
🏢 <b>Department:</b> {department}
💼 <b>Role:</b> {role}

⚡ <b>Triggered By:</b>
{triggered_by}

📋 <b>Risk Indicators:</b>
{reasons_text}

🕐 <b>Detected At:</b> {timestamp}

━━━━━━━━━━━━━━━━━
⚠️ Take action in INSIGHT-X → Control Panel"""


def fire_alerts(emp_info, triggered_by, alert_cfg, alert_log):
    """
    Fires both alerts (Gmail + Telegram) simultaneously
    and adds an entry to the alert log.
    """
    name     = emp_info["name"]
    dept     = emp_info["dept"]
    role     = emp_info["role"]
    score    = emp_info["score"]
    reasons  = emp_info["reasons"]

    log_entry = {
        "timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "employee":     name,
        "dept":         dept,
        "risk_score":   score,
        "triggered_by": triggered_by,
        "email_status": "—",
        "telegram_status": "—",
    }

    # ── EMAIL ──
    if alert_cfg.get("email_enabled") and alert_cfg.get("sender_email") and alert_cfg.get("sender_password"):
        email_html = build_email_html(name, dept, role, score, reasons, triggered_by)
        subject    = f"🚨 INSIGHT-X ALERT — {'CRITICAL' if score>=80 else 'HIGH'} Threat: {name} (Score: {score})"
        ok, msg    = send_gmail_alert(
            alert_cfg["sender_email"],
            alert_cfg["sender_password"],
            alert_cfg["recipient_email"],
            subject,
            email_html
        )
        log_entry["email_status"] = "✅ Sent" if ok else f"❌ {msg[:40]}"
    else:
        log_entry["email_status"] = "⏭ Skipped"

    # ── TELEGRAM ──
    if alert_cfg.get("telegram_enabled") and alert_cfg.get("bot_token") and alert_cfg.get("chat_id"):
        tg_msg = build_telegram_message(name, dept, role, score, reasons, triggered_by)
        ok, msg = send_telegram_alert(
            alert_cfg["bot_token"],
            alert_cfg["chat_id"],
            tg_msg
        )
        log_entry["telegram_status"] = "✅ Sent" if ok else f"❌ {msg[:40]}"
    else:
        log_entry["telegram_status"] = "⏭ Skipped"

    alert_log.append(log_entry)
    return log_entry


# ─────────────────────────────────────────
#  SYNTHETIC DATA ENGINE
# ─────────────────────────────────────────
@st.cache_data
def build_employee_data():
    random.seed(42)
    np.random.seed(42)

    employees = [
        {"id": "EMP-001", "name": "Aman Sharma",    "dept": "Engineering",  "role": "Sr. Developer",      "tenure_yrs": 3},
        {"id": "EMP-002", "name": "Riya Mehta",     "dept": "Finance",      "role": "Financial Analyst",  "tenure_yrs": 5},
        {"id": "EMP-003", "name": "Kavya Patel",    "dept": "HR",           "role": "HR Manager",         "tenure_yrs": 7},
        {"id": "EMP-004", "name": "Raj Verma",      "dept": "Engineering",  "role": "DevOps Engineer",    "tenure_yrs": 1},
        {"id": "EMP-005", "name": "Simran Kaur",    "dept": "Marketing",    "role": "Brand Strategist",   "tenure_yrs": 2},
        {"id": "EMP-006", "name": "Arjun Nair",     "dept": "Engineering",  "role": "Security Analyst",   "tenure_yrs": 4},
        {"id": "EMP-007", "name": "Priya Joshi",    "dept": "Finance",      "role": "Accounts Lead",      "tenure_yrs": 6},
        {"id": "EMP-008", "name": "Dev Malhotra",   "dept": "IT Ops",       "role": "Sysadmin",           "tenure_yrs": 2},
    ]

    file_types  = ["PDF", "CSV", "XLSX", "DOCX", "ZIP", "DB_DUMP", "JSON", "PPTX"]
    channels    = ["VPN", "Browser", "Email", "USB", "Cloud Sync", "FTP", "API"]
    sensitivity = ["Public", "Internal", "Confidential", "Restricted"]

    risk_profiles = {
        "EMP-001": {"score": 82, "reasons": ["After-hours bulk download", "Access to restricted DB", "Used personal USB twice"]},
        "EMP-002": {"score": 91, "reasons": ["Downloaded 14 financial reports in one session", "VPN anomaly from new location", "Mass CSV export flagged"]},
        "EMP-003": {"score": 38, "reasons": ["Normal activity pattern", "Routine HR document access"]},
        "EMP-004": {"score": 75, "reasons": ["Unusual API calls at 2 AM", "Attempted access to prod secrets", "Large ZIP download"]},
        "EMP-005": {"score": 22, "reasons": ["Low activity volume", "Only public documents accessed"]},
        "EMP-006": {"score": 55, "reasons": ["Moderate anomaly: scanned internal network ports", "Accessed legacy admin panel"]},
        "EMP-007": {"score": 88, "reasons": ["Repeated download of salary data", "Logged in from 3 different IPs in 1 day", "Exported full employee DB"]},
        "EMP-008": {"score": 67, "reasons": ["Accessed files outside job scope", "Midnight login from unrecognized device"]},
    }

    rows = []
    base_time = datetime(2025, 6, 10, 8, 0, 0)

    for emp in employees:
        eid  = emp["id"]
        risk = risk_profiles[eid]["score"]
        n_dl = max(2, int(risk / 8) + random.randint(0, 4))

        for _ in range(n_dl):
            size_mb = round(random.uniform(0.1, 180.0) if risk > 60 else random.uniform(0.1, 30.0), 2)
            offset  = timedelta(
                days=random.randint(0, 10),
                hours=random.randint(0, 5) if risk > 60 else random.randint(8, 17),
                minutes=random.randint(0, 59)
            )
            rows.append({
                "emp_id":       eid,
                "name":         emp["name"],
                "department":   emp["dept"],
                "role":         emp["role"],
                "file_type":    random.choice(file_types if risk > 60 else file_types[:5]),
                "size_mb":      size_mb,
                "channel":      random.choice(channels if risk > 60 else channels[:4]),
                "sensitivity":  random.choices(
                                    sensitivity,
                                    weights=[1, 2, 3, 4] if risk > 60 else [4, 3, 2, 1]
                                )[0],
                "timestamp":    (base_time + offset).strftime("%Y-%m-%d %H:%M"),
                "risk_score":   risk,
                "risk_reasons": " | ".join(risk_profiles[eid]["reasons"]),
                "tenure_yrs":   emp["tenure_yrs"],
            })

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df, {e["id"]: {**e, **risk_profiles[e["id"]]} for e in employees}


# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
def risk_badge(score):
    if score >= 80:
        return f'<span class="risk-critical">CRITICAL {score}</span>'
    elif score >= 60:
        return f'<span class="risk-high">HIGH {score}</span>'
    else:
        return f'<span class="risk-low">LOW {score}</span>'

def plot_cfg(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Mono", color="#9ca3af", size=11),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)")
    )
    return fig


# ─────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────
def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Alert configuration store
    if "alert_cfg" not in st.session_state:
        st.session_state.alert_cfg = {
            "email_enabled":    False,
            "telegram_enabled": False,
            "sender_email":     "",
            "sender_password":  "",
            "recipient_email":  "",
            "bot_token":        "",
            "chat_id":          "",
            "min_score":        75,
        }

    # Alert history log
    if "alert_log" not in st.session_state:
        st.session_state.alert_log = []

    # Cooldown: track last alerted employees to avoid spam
    if "alerted_today" not in st.session_state:
        st.session_state.alerted_today = set()


# ─────────────────────────────────────────
#  MAIN DASHBOARD
# ─────────────────────────────────────────
def render_dashboard():
    df, emp_map = build_employee_data()
    cfg         = st.session_state.alert_cfg
    alert_log   = st.session_state.alert_log

    # ── SIDEBAR ──────────────────────────
    with st.sidebar:
        st.markdown("""
        <div class='sidebar-logo'>
            <div class='brand'>⬡ INSIGHT&#8209;X</div>
            <div class='tagline'>Insider Threat Intelligence</div>
        </div>
        <div class='status-pill'>
            <div class='status-dot'></div> SYSTEM ACTIVE
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        menu = st.radio("", [
            "🏠  Overview",
            "👥  Employee Database",
            "📊  Risk Analysis",
            "🧠  Behavior Analysis",
            "🔍  Employee Spotlight",
            "🔔  Alert Config",
            "📋  Alert Log",
            "⚡  Actions",
            "🚪  Logout",
        ], label_visibility="collapsed")

        st.markdown("<br><br>", unsafe_allow_html=True)

        critical_count = len({k for k, v in emp_map.items() if v["score"] >= 80})
        high_count     = len({k for k, v in emp_map.items() if 60 <= v["score"] < 80})
        log_count      = len(alert_log)

        st.markdown(f"""
        <div style='padding: 0 16px; font-family: Space Mono; font-size: 11px; color: #6b7280;'>
        <div style='margin-bottom:8px;'>THREAT SUMMARY</div>
        <div style='color:#ff4c6a; margin-bottom:4px;'>● {critical_count} Critical</div>
        <div style='color:#fbbf24; margin-bottom:4px;'>● {high_count} High Risk</div>
        <div style='color:#34d399; margin-bottom:12px;'>● {len(emp_map) - critical_count - high_count} Normal</div>
        <div style='color:#a78bfa;'>📨 {log_count} Alerts Fired</div>
        </div>
        """, unsafe_allow_html=True)

    if "Logout" in menu:
        st.session_state.logged_in = False
        st.rerun()

    # ─────────────────────────────────────
    #  ALERT CONFIG PAGE  ← NEW
    # ─────────────────────────────────────
    if "Alert Config" in menu:
        st.markdown("""
        <div class='section-header'>
            <span class='section-title'>Alert Configuration</span>
            <span class='section-badge'>NOTIFICATION ENGINE</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background:rgba(0,229,255,0.05); border:1px solid rgba(0,229,255,0.15);
                    border-radius:12px; padding:14px 20px; margin-bottom:20px;
                    font-family:Space Mono; font-size:12px; color:#9ca3af;'>
        ℹ️ &nbsp; For Gmail, use an <b style='color:#00e5ff'>App Password</b> — your normal password will not work.<br>
        ℹ️ &nbsp; For Telegram, create a bot via <b style='color:#00e5ff'>@BotFather</b> and get your Chat ID from <b style='color:#00e5ff'>@userinfobot</b>.
        </div>
        """, unsafe_allow_html=True)

        # ── GMAIL SECTION ──
        st.markdown("""
        <div class='alert-config-card'>
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:18px;'>
                <span style='font-size:20px;'>📧</span>
                <span style='font-size:16px; font-weight:700; color:#e8eaf0;'>Gmail Alert Setup</span>
            </div>
        """, unsafe_allow_html=True)

        email_on = st.toggle("Enable Gmail Alerts", value=cfg["email_enabled"], key="tog_email")
        st.session_state.alert_cfg["email_enabled"] = email_on

        if email_on:
            col1, col2 = st.columns(2)
            with col1:
                s_email = st.text_input("Your Gmail (Sender)", value=cfg["sender_email"],
                                        placeholder="yourname@gmail.com", key="s_email")
                st.session_state.alert_cfg["sender_email"] = s_email

            with col2:
                r_email = st.text_input("Recipient Email", value=cfg["recipient_email"],
                                        placeholder="security@company.com", key="r_email")
                st.session_state.alert_cfg["recipient_email"] = r_email

            s_pass = st.text_input("Gmail App Password", value=cfg["sender_password"],
                                   type="password",
                                   placeholder="xxxx xxxx xxxx xxxx  (16-char App Password)",
                                   key="s_pass")
            st.session_state.alert_cfg["sender_password"] = s_pass

            st.markdown("""
            <div style='font-size:11px; color:#6b7280; font-family:Space Mono; margin-top:6px;'>
            👉 How to create a Gmail App Password:<br>
            myaccount.google.com → Security → 2-Step Verification → App passwords → Generate
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── TELEGRAM SECTION ──
        st.markdown("""
        <div class='alert-config-card'>
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:18px;'>
                <span style='font-size:20px;'>📱</span>
                <span style='font-size:16px; font-weight:700; color:#e8eaf0;'>Telegram Alert Setup</span>
                <span style='font-size:11px; color:#34d399; font-family:Space Mono;
                              background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.25);
                              border-radius:20px; padding:2px 10px;'>PHONE VIBRATE ✓</span>
            </div>
        """, unsafe_allow_html=True)

        tg_on = st.toggle("Enable Telegram Alerts", value=cfg["telegram_enabled"], key="tog_tg")
        st.session_state.alert_cfg["telegram_enabled"] = tg_on

        if tg_on:
            col1, col2 = st.columns(2)
            with col1:
                bot_tok = st.text_input("Bot Token", value=cfg["bot_token"],
                                        placeholder="123456789:ABCdef...", key="bot_tok",
                                        type="password")
                st.session_state.alert_cfg["bot_token"] = bot_tok

            with col2:
                chat_id = st.text_input("Your Chat ID", value=cfg["chat_id"],
                                        placeholder="e.g. 987654321", key="chat_id_inp")
                st.session_state.alert_cfg["chat_id"] = chat_id

            st.markdown("""
            <div style='font-size:11px; color:#6b7280; font-family:Space Mono; margin-top:6px;'>
            👉 How to create a Telegram Bot:<br>
            1. Telegram → search <b style='color:#a78bfa'>@BotFather</b> → /newbot → copy the token<br>
            2. Search <b style='color:#a78bfa'>@userinfobot</b> → /start → get your Chat ID
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── THRESHOLD ──
        st.markdown("""<div class='alert-config-card'>
            <div style='font-size:14px; font-weight:700; color:#e8eaf0; margin-bottom:14px;'>
            ⚙️ Alert Trigger Threshold
            </div>
        """, unsafe_allow_html=True)

        threshold = st.slider(
            "Minimum Risk Score to Trigger Alert",
            min_value=50, max_value=95,
            value=cfg["min_score"], step=5,
            key="thresh_slider"
        )
        st.session_state.alert_cfg["min_score"] = threshold

        above = [v["name"] for v in emp_map.values() if v["score"] >= threshold]
        st.markdown(f"""
        <div style='font-size:12px; color:#9ca3af; font-family:Space Mono; margin-top:8px;'>
        ⚡ Current threshold <b style='color:#00e5ff'>{threshold}</b> will trigger alerts for:
        <b style='color:#ff4c6a'>{", ".join(above) if above else "No employees"}</b>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── TEST ALERT BUTTON ──
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧪 Send Test Alert Now (Riya Mehta — Score 91)"):
            test_emp = emp_map["EMP-002"]
            with st.spinner("Sending test alerts..."):
                result = fire_alerts(
                    test_emp,
                    "TEST ALERT — Manually triggered from Alert Config page",
                    st.session_state.alert_cfg,
                    st.session_state.alert_log
                )
            st.markdown(f"""
            <div style='background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.25);
                        border-radius:10px; padding:14px 18px; font-family:Space Mono; font-size:12px;'>
            <div style='color:#34d399; font-weight:700; margin-bottom:8px;'>Test Alert Result:</div>
            <div>📧 Email: {result["email_status"]}</div>
            <div>📱 Telegram: {result["telegram_status"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ─────────────────────────────────────
    #  ALERT LOG PAGE  ← NEW
    # ─────────────────────────────────────
    elif "Alert Log" in menu:
        st.markdown("""
        <div class='section-header'>
            <span class='section-title'>Alert History</span>
            <span class='section-badge'>FIRED ALERTS</span>
        </div>
        """, unsafe_allow_html=True)

        if not alert_log:
            st.markdown("""
            <div style='text-align:center; padding:60px 20px; font-family:Space Mono;
                        color:#374151; font-size:13px;'>
            📭 No alerts have been fired yet.<br>
            <span style='font-size:11px;'>Fire an alert from the Actions tab or via auto-trigger.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Summary pills
            total      = len(alert_log)
            email_ok   = sum(1 for l in alert_log if "✅" in l.get("email_status",""))
            tg_ok      = sum(1 for l in alert_log if "✅" in l.get("telegram_status",""))

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class='card'>
                    <div class='card-title'>Total Alerts Fired</div>
                    <div class='card-value info'>{total}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class='card'>
                    <div class='card-title'>Emails Delivered</div>
                    <div class='card-value safe'>{email_ok}</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class='card'>
                    <div class='card-title'>Telegram Sent</div>
                    <div class='card-value info'>{tg_ok}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            for entry in reversed(alert_log):
                severity_class = "critical" if entry["risk_score"] >= 80 else "high"
                st.markdown(f"""
                <div class='log-item {severity_class}'>
                    <div style='flex:1;'>
                        <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                            <span style='color:#e8eaf0; font-weight:700;'>{entry["employee"]}</span>
                            <span style='color:#6b7280; font-size:10px;'>{entry["timestamp"]}</span>
                        </div>
                        <div style='color:#9ca3af; font-size:11px; margin-bottom:6px;'>
                            {entry["dept"]} · Risk Score: <b style='color:{"#ff4c6a" if entry["risk_score"]>=80 else "#fbbf24"}'>{entry["risk_score"]}</b>
                        </div>
                        <div style='color:#6b7280; font-size:11px; margin-bottom:6px;'>
                            ⚡ {entry["triggered_by"][:80]}...
                        </div>
                        <div style='display:flex; gap:16px;'>
                            <span>📧 <span class='{"log-sent" if "✅" in entry["email_status"] else "log-failed"}'>{entry["email_status"]}</span></span>
                            <span>📱 <span class='{"log-sent" if "✅" in entry["telegram_status"] else "log-failed"}'>{entry["telegram_status"]}</span></span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if st.button("🗑️ Clear Alert Log"):
                st.session_state.alert_log = []
                st.rerun()

    # ─────────────────────────────────────
    #  OVERVIEW
    # ─────────────────────────────────────
    elif "Overview" in menu:
        st.markdown("""
        <div class='section-header'>
            <span class='section-title'>Threat Overview</span>
            <span class='section-badge'>LIVE MONITORING</span>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        total_dl          = df["size_mb"].sum()
        critical          = len({r for r, v in emp_map.items() if v["score"] >= 80})
        high_risk         = len({r for r, v in emp_map.items() if v["score"] >= 60})
        restricted_events = len(df[df["sensitivity"] == "Restricted"])

        with c1:
            st.markdown(f"""<div class='card'>
                <div class='card-title'>Total Data Moved</div>
                <div class='card-value info'>{total_dl:.0f}<span style='font-size:18px'> MB</span></div>
                <div class='card-sub'>across all employees</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='card'>
                <div class='card-title'>Critical Threats</div>
                <div class='card-value danger'>{critical}</div>
                <div class='card-sub'>employees at risk score ≥ 80</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='card'>
                <div class='card-title'>High-Risk Users</div>
                <div class='card-value warn'>{high_risk}</div>
                <div class='card-sub'>risk score ≥ 60</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='card'>
                <div class='card-title'>Restricted File Events</div>
                <div class='card-value danger'>{restricted_events}</div>
                <div class='card-sub'>accesses flagged</div>
            </div>""", unsafe_allow_html=True)

        # Auto-fire alerts for critical employees on overview load
        cfg = st.session_state.alert_cfg
        auto_fired = []
        for eid, v in emp_map.items():
            if v["score"] >= cfg["min_score"] and eid not in st.session_state.alerted_today:
                if cfg["email_enabled"] or cfg["telegram_enabled"]:
                    result = fire_alerts(v, f"Auto-detected: Risk score {v['score']} exceeds threshold {cfg['min_score']}", cfg, st.session_state.alert_log)
                    st.session_state.alerted_today.add(eid)
                    auto_fired.append(v["name"])

        if auto_fired:
            st.markdown(f"""
            <div style='background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.25);
                        border-left:3px solid #34d399; border-radius:10px;
                        padding:12px 16px; margin-bottom:16px;
                        font-family:Space Mono; font-size:12px; color:#34d399;'>
            ✅ Auto-alerts fired for: <b>{", ".join(auto_fired)}</b> — Check Alert Log
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>🚨 Active Threat Alerts</div>", unsafe_allow_html=True)
        for eid, v in emp_map.items():
            if v["score"] >= 75:
                for reason in v["reasons"]:
                    st.markdown(f"""<div class='alert-box'>
                        <strong>{v['name']}</strong> ({v['dept']}) &nbsp;·&nbsp; {reason}
                    </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>📈 Data Exfiltration Volume — Last 10 Days</div>", unsafe_allow_html=True)
        daily = df.groupby(df["timestamp"].dt.date)["size_mb"].sum().reset_index()
        daily.columns = ["date", "MB"]
        fig_line = px.area(daily, x="date", y="MB", color_discrete_sequence=["#00e5ff"], template="none")
        fig_line.update_traces(line=dict(width=2), fillcolor="rgba(0,229,255,0.07)")
        st.plotly_chart(plot_cfg(fig_line), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    #  EMPLOYEE DATABASE
    # ─────────────────────────────────────
    elif "Employee Database" in menu:
        st.markdown("""
        <div class='section-header'>
            <span class='section-title'>Employee Database</span>
            <span class='section-badge'>DATA ACCESS LOG</span>
        </div>
        """, unsafe_allow_html=True)

        summary = df.groupby(["emp_id","name","department","role","tenure_yrs","risk_score"]).agg(
            total_downloads=("size_mb","count"),
            total_mb=("size_mb","sum"),
            top_channel=("channel", lambda x: x.value_counts().index[0]),
            last_activity=("timestamp","max"),
            restricted_hits=("sensitivity", lambda x: (x=="Restricted").sum()),
        ).reset_index()

        summary["Risk Level"] = summary["risk_score"].apply(
            lambda s: "CRITICAL" if s>=80 else ("HIGH" if s>=60 else "LOW")
        )
        summary["last_activity"] = summary["last_activity"].dt.strftime("%Y-%m-%d %H:%M")
        summary["total_mb"] = summary["total_mb"].round(1)

        display_cols = {
            "emp_id":"ID","name":"Name","department":"Department","role":"Role",
            "total_downloads":"Downloads","total_mb":"Data (MB)","top_channel":"Primary Channel",
            "last_activity":"Last Activity","restricted_hits":"Restricted Hits","Risk Level":"Risk Level",
        }
        out = summary[list(display_cols.keys())].rename(columns=display_cols)
        st.dataframe(
            out.style
               .applymap(lambda v: "color: #ff4c6a; font-weight:700" if v=="CRITICAL"
                         else ("color: #fbbf24; font-weight:700" if v=="HIGH"
                               else ("color: #34d399" if v=="LOW" else "")),
                         subset=["Risk Level"])
               .format({"Data (MB)": "{:.1f}", "Downloads": "{:d}", "Restricted Hits": "{:d}"}),
            use_container_width=True, height=380
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Most Downloaded File Types</div>", unsafe_allow_html=True)
        ft = df.groupby("file_type")["size_mb"].sum().reset_index().sort_values("size_mb", ascending=False)
        fig_ft = px.bar(ft, x="file_type", y="size_mb",
                        color="size_mb", color_continuous_scale=[[0,"#0f1218"],[1,"#00e5ff"]],
                        template="none", labels={"size_mb":"MB","file_type":"File Type"})
        st.plotly_chart(plot_cfg(fig_ft), use_container_width=True)

    # ─────────────────────────────────────
    #  RISK ANALYSIS
    # ─────────────────────────────────────
    elif "Risk Analysis" in menu:
        st.markdown("""
        <div class='section-header'>
            <span class='section-title'>Risk Analysis</span>
            <span class='section-badge'>AI SCORING</span>
        </div>
        """, unsafe_allow_html=True)

        emp_risk = df[["name","risk_score","department","tenure_yrs","risk_reasons"]].drop_duplicates("name")
        emp_risk = emp_risk.sort_values("risk_score", ascending=False)

        colors = ["#ff4c6a" if s>=80 else ("#fbbf24" if s>=60 else "#34d399") for s in emp_risk["risk_score"]]
        fig_bar = go.Figure(go.Bar(
            x=emp_risk["risk_score"], y=emp_risk["name"],
            orientation="h", marker_color=colors,
            text=emp_risk["risk_score"], textposition="outside",
            textfont=dict(family="Space Mono", size=12, color="#e8eaf0")
        ))
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Space Mono", color="#9ca3af", size=11),
            margin=dict(l=10,r=60,t=10,b=10),
            xaxis=dict(range=[0,110], gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"), height=360
        )
        fig_bar.add_vline(x=80, line_dash="dot", line_color="rgba(255,76,106,0.4)", annotation_text="CRITICAL", annotation_font_color="#ff4c6a", annotation_font_size=10)
        fig_bar.add_vline(x=60, line_dash="dot", line_color="rgba(251,191,36,0.4)", annotation_text="HIGH", annotation_font_color="#fbbf24", annotation_font_size=10)
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("<div class='card-title' style='margin-top:8px'>Why are they flagged?</div>", unsafe_allow_html=True)
        for _, row in emp_risk.iterrows():
            score = row["risk_score"]
            badge = risk_badge(score)
            reasons_html = "".join([f"<span class='behavior-tag'>⚑ {r.strip()}</span>" for r in row["risk_reasons"].split("|")])
            st.markdown(f"""
            <div class='card' style='margin-bottom:10px; padding:16px 20px;'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                    <div style='font-weight:700; font-size:15px'>{row['name']}</div>
                    <div>{badge}</div>
                </div>
                <div style='font-size:11px; color:#6b7280; font-family:Space Mono; margin-bottom:8px;'>
                    {row['department']} · {row['tenure_yrs']}y tenure
                </div>
                <div>{reasons_html}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Tenure vs Risk Score</div>", unsafe_allow_html=True)
        fig_sc = px.scatter(emp_risk, x="tenure_yrs", y="risk_score", text="name",
                            color="risk_score", color_continuous_scale=["#34d399","#fbbf24","#ff4c6a"],
                            size_max=20, template="none",
                            labels={"tenure_yrs":"Years at Company","risk_score":"Risk Score"})
        fig_sc.update_traces(textposition="top center", textfont=dict(size=10, color="#9ca3af"), marker=dict(size=12))
        st.plotly_chart(plot_cfg(fig_sc), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    #  BEHAVIOR ANALYSIS
    # ─────────────────────────────────────
    elif "Behavior Analysis" in menu:
        st.markdown("""
        <div class='section-header'>
            <span class='section-title'>Behavior Analysis</span>
            <span class='section-badge'>AI ENGINE</span>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Access Hour Distribution</div>", unsafe_allow_html=True)
            hour_df = df.copy()
            hour_df["hour"] = hour_df["timestamp"].dt.hour
            hour_dist = hour_df.groupby("hour").size().reset_index(name="events")
            fig_hour = px.bar(hour_dist, x="hour", y="events",
                              color="events",
                              color_continuous_scale=[[0,"#131720"],[0.5,"#a78bfa"],[1,"#ff4c6a"]],
                              template="none", labels={"hour":"Hour of Day","events":"Events"})
            fig_hour.add_vrect(x0=22, x1=6, fillcolor="rgba(255,76,106,0.07)", line_width=0,
                               annotation_text="After Hours Zone", annotation_font_size=10,
                               annotation_font_color="#ff4c6a")
            st.plotly_chart(plot_cfg(fig_hour), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_b:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Data Sensitivity Distribution</div>", unsafe_allow_html=True)
            sens = df.groupby("sensitivity").size().reset_index(name="count")
            fig_pie = px.pie(sens, names="sensitivity", values="count",
                             color="sensitivity",
                             color_discrete_map={"Public":"#34d399","Internal":"#60a5fa","Confidential":"#fbbf24","Restricted":"#ff4c6a"},
                             hole=0.55, template="none")
            fig_pie.update_traces(textfont=dict(family="Space Mono", size=10))
            st.plotly_chart(plot_cfg(fig_pie), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Channel Usage Heatmap</div>", unsafe_allow_html=True)
        heat = df.groupby(["name","channel"]).size().reset_index(name="count")
        heat_pivot = heat.pivot(index="name", columns="channel", values="count").fillna(0)
        fig_heat = px.imshow(heat_pivot,
                             color_continuous_scale=[[0,"#0a0c10"],[0.3,"#0f2a3a"],[0.7,"#00e5ff"],[1,"#ff4c6a"]],
                             aspect="auto", template="none", labels=dict(color="Events"))
        fig_heat.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Space Mono", color="#9ca3af", size=10),
            margin=dict(l=10,r=10,t=10,b=10), height=300
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>AI-Detected Anomaly Timeline</div>", unsafe_allow_html=True)
        anomalies = [
            ("critical", "02:14 AM", "Riya Mehta downloaded 14 financial reports via VPN — unusual session length (2h 7m)"),
            ("critical", "03:41 AM", "Dev Malhotra logged in from unrecognized device (New IP: 185.x.x.x)"),
            ("warn",     "11:58 PM", "Raj Verma made 47 API calls in 4 minutes — possible automated scraping"),
            ("critical", "01:22 AM", "Aman Sharma accessed Restricted DB table 'payroll_master' — outside job scope"),
            ("warn",     "09:15 PM", "Arjun Nair scanned internal subnet 10.0.2.0/24 — 3 ports flagged"),
            ("critical", "12:00 AM", "Priya Joshi exported full employee database (87 MB CSV via Email attachment)"),
            ("warn",     "10:45 PM", "Aman Sharma connected personal USB drive — 2nd occurrence this week"),
        ]
        for severity, time_str, desc in anomalies:
            st.markdown(f"""
            <div class='timeline-item'>
                <div class='timeline-dot {severity}'></div>
                <div class='timeline-time'>{time_str}</div>
                <div class='timeline-desc'>{desc}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    #  EMPLOYEE SPOTLIGHT
    # ─────────────────────────────────────
    elif "Employee Spotlight" in menu:
        st.markdown("""
        <div class='section-header'>
            <span class='section-title'>Employee Deep Dive</span>
            <span class='section-badge'>FORENSIC VIEW</span>
        </div>
        """, unsafe_allow_html=True)

        emp_names = sorted(df["name"].unique())
        selected  = st.selectbox("Select Employee", emp_names)
        emp_df    = df[df["name"] == selected].copy()
        eid       = emp_df["emp_id"].iloc[0]
        emp_info  = emp_map[eid]
        score     = emp_info["score"]

        st.markdown(f"""
        <div class='card' style='padding:24px 28px;'>
            <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                <div>
                    <div style='font-size:22px; font-weight:800; margin-bottom:4px;'>{emp_info['name']}</div>
                    <div style='font-family:Space Mono; font-size:12px; color:#6b7280;'>
                        {emp_info['role']} · {emp_info['dept']} · {emp_info['tenure_yrs']} years
                    </div>
                </div>
                <div>{risk_badge(score)}</div>
            </div>
            <div class='divider'></div>
            <div style='font-family:Space Mono; font-size:11px; color:#6b7280; margin-bottom:8px;'>WHY THIS SCORE?</div>
            {"".join([f"<div style='margin-bottom:6px; font-size:13px;'>⚑ &nbsp;{r}</div>" for r in emp_info['reasons']])}
        </div>
        """, unsafe_allow_html=True)

        # Manual alert button for spotlight
        if st.button(f"🚨 Fire Alert for {selected} Now"):
            cfg = st.session_state.alert_cfg
            if not cfg["email_enabled"] and not cfg["telegram_enabled"]:
                st.warning("⚠️ Please set up Gmail or Telegram in the Alert Config tab first!")
            else:
                with st.spinner("Sending alerts..."):
                    result = fire_alerts(
                        emp_info,
                        f"Manual alert fired from Employee Spotlight by admin",
                        cfg,
                        st.session_state.alert_log
                    )
                st.markdown(f"""
                <div style='background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.25);
                            border-radius:10px; padding:14px 18px; font-family:Space Mono; font-size:12px;'>
                <b style='color:#34d399;'>Alert Result:</b><br>
                📧 Email: {result["email_status"]}<br>
                📱 Telegram: {result["telegram_status"]}
                </div>
                """, unsafe_allow_html=True)

        emp_display = emp_df[["timestamp","file_type","size_mb","channel","sensitivity"]].copy()
        emp_display["timestamp"] = emp_display["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        emp_display = emp_display.sort_values("timestamp", ascending=False).rename(columns={
            "timestamp":"When","file_type":"File Type","size_mb":"Size (MB)",
            "channel":"Channel","sensitivity":"Sensitivity"
        })
        st.markdown("<div class='card-title' style='margin-top:16px'>Download Activity Log</div>", unsafe_allow_html=True)
        st.dataframe(
            emp_display.style.applymap(
                lambda v: "color: #ff4c6a; font-weight:700" if v=="Restricted"
                else ("color: #fbbf24" if v=="Confidential" else ""),
                subset=["Sensitivity"]
            ),
            use_container_width=True, height=260
        )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            fig_emp = px.scatter(emp_df, x="timestamp", y="size_mb", color="sensitivity",
                                 color_discrete_map={"Public":"#34d399","Internal":"#60a5fa","Confidential":"#fbbf24","Restricted":"#ff4c6a"},
                                 template="none", size="size_mb", size_max=20)
            st.plotly_chart(plot_cfg(fig_emp), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            ch_cnt = emp_df["channel"].value_counts().reset_index()
            ch_cnt.columns = ["Channel","Count"]
            fig_ch = px.bar(ch_cnt, x="Channel", y="Count",
                            color="Count", color_continuous_scale=[[0,"#0f1218"],[1,"#a78bfa"]],
                            template="none")
            st.plotly_chart(plot_cfg(fig_ch), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    #  ACTIONS
    # ─────────────────────────────────────
    elif "Actions" in menu:
        st.markdown("""
        <div class='section-header'>
            <span class='section-title'>Control Panel</span>
            <span class='section-badge'>ADMIN ACTIONS</span>
        </div>
        """, unsafe_allow_html=True)

        emp_names = sorted(df["name"].unique())
        selected  = st.selectbox("Target Employee", emp_names)
        eid       = df[df["name"]==selected]["emp_id"].iloc[0]
        emp_info  = emp_map[eid]
        score     = emp_info["score"]

        st.markdown(f"""
        <div class='card'>
            <div style='display:flex; gap:12px; align-items:center;'>
                <div>
                    <div style='font-weight:700'>{emp_info['name']}</div>
                    <div style='font-size:11px; color:#6b7280; font-family:Space Mono;'>{emp_info['dept']} · {emp_info['role']}</div>
                </div>
                <div>{risk_badge(score)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("🚫 Block User Access"):
                st.error(f"🔒 {selected} — access suspended. IT notified.")

        with c2:
            if st.button("📧 Send Compliance Alert"):
                st.warning(f"📨 Compliance email sent to {selected} and their manager.")

        with c3:
            if st.button("🔎 Flag for HR Review"):
                st.info(f"🗂️ {selected} flagged. Case ID: {eid}-{datetime.now().strftime('%H%M%S')}")

        # ── ALERT BUTTON IN ACTIONS ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>🚨 Fire Threat Alert</div>", unsafe_allow_html=True)

        alert_reason = st.text_input("Alert Reason (optional)", placeholder="e.g. Suspicious bulk download detected at 2 AM")

        if st.button("🔔 Send Gmail + Telegram Alert Now"):
            cfg = st.session_state.alert_cfg
            if not cfg["email_enabled"] and not cfg["telegram_enabled"]:
                st.warning("⚠️ Please set up Gmail or Telegram in the Alert Config tab first!")
            else:
                triggered = alert_reason if alert_reason else f"Manual alert — Risk Score {score} for {selected}"
                with st.spinner("📡 Sending alerts..."):
                    result = fire_alerts(emp_info, triggered, cfg, st.session_state.alert_log)

                st.markdown(f"""
                <div style='background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.25);
                            border-left:3px solid #34d399; border-radius:10px;
                            padding:16px 20px; font-family:Space Mono; font-size:13px;'>
                <div style='color:#34d399; font-weight:700; margin-bottom:10px;'>✅ Alert Fired!</div>
                <div>📧 Email: <b>{result["email_status"]}</b></div>
                <div>📱 Telegram: <b>{result["telegram_status"]}</b></div>
                </div>
                """, unsafe_allow_html=True)

        # Bulk escalation
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Bulk Actions — Critical Users</div>", unsafe_allow_html=True)
        critical_names = [v["name"] for v in emp_map.values() if v["score"] >= 80]
        for n in critical_names:
            eid_c = [k for k, v in emp_map.items() if v["name"]==n][0]
            st.markdown(f"""<div class='alert-box'>
                <strong>{n}</strong> · {risk_badge(emp_map[eid_c]["score"])} &nbsp;→ Pending review
            </div>""", unsafe_allow_html=True)

        if st.button("🚨 Escalate All Critical Cases + Fire All Alerts"):
            cfg = st.session_state.alert_cfg
            fired = 0
            for eid_c, v in emp_map.items():
                if v["score"] >= 80:
                    fire_alerts(v, f"Bulk escalation — Critical threat score {v['score']}", cfg, st.session_state.alert_log)
                    fired += 1
            st.error(f"🚨 {len(critical_names)} cases escalated. {fired} alerts fired → Check Alert Log.")


# ─────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────
def render_login():
    _, col, _ = st.columns([1.2, 1, 1.2])
    with col:
        st.markdown("""
        <div style='padding:60px 0 20px;'>
            <div style='
                background: #0f1218;
                border: 1px solid rgba(0,229,255,0.15);
                border-radius: 24px;
                padding: 48px 40px;
                text-align: center;
                box-shadow: 0 0 80px rgba(0,229,255,0.06);
            '>
                <div style='
                    font-family: Space Mono, monospace;
                    font-size: 26px;
                    font-weight: 700;
                    color: #00e5ff;
                    letter-spacing: 5px;
                    text-shadow: 0 0 30px #00e5ff;
                    margin-bottom: 6px;
                '>⬡ INSIGHT-X</div>
                <div style='
                    font-size: 11px;
                    color: #6b7280;
                    letter-spacing: 3px;
                    text-transform: uppercase;
                    font-family: Space Mono, monospace;
                    margin-bottom: 36px;
                '>Insider Threat Intelligence Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        if st.button("→ Authenticate"):
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access denied — invalid credentials.")

        st.markdown("""
        <div style='text-align:center; margin-top:16px; font-size:11px; color:#374151; font-family:Space Mono;'>
        demo: admin / 1234
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────
init_session()

if st.session_state.logged_in:
    render_dashboard()
else:
    render_login()