import pandas as pd
import requests
import json
import smtplib
import time
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ================= CONFIGURATION =================
# 1. API KEYS
API_KEYS = [
    "key0",
    "key1",
    "key2",
    "key3"
]

# 2. MODELS - REORDERED FOR RELIABILITY
# We moved Gemma up because it is stable.
MODELS = [
    "gemini-2.5-flash-lite",  # ✅ FASTEST (Primary)
    "gemma-3-4b-it",          # ✅ SAFETY NET (Open Model, very reliable)
    "gemini-2.5-flash",       # ⚠️ Busy often
    "gemini-2.0-flash-lite"   # ⚠️ Backup
]

CURRENT_KEY_INDEX = 0

# 3. EMAIL CREDENTIALS
SENDER_EMAIL = "mail@gmail.com"
SENDER_PASSWORD = "16-digit password" 

# 4. FILE SETTINGS
CSV_FILE_PATH = "list of clients.xls" 

# 5. RESUME FROM ROW 92 (Sunil Goher)
START_FROM_ROW = 127

DRY_RUN = False
# =================================================

def get_current_api_key():
    return API_KEYS[CURRENT_KEY_INDEX]

def switch_api_key():
    global CURRENT_KEY_INDEX
    CURRENT_KEY_INDEX = (CURRENT_KEY_INDEX + 1) % len(API_KEYS)
    print(f"   🔄 Switching to API Key #{CURRENT_KEY_INDEX + 1}...")

def generate_smart_email(client_name, client_company, attempt=0):
    # Stop if we've tried too many times
    if attempt > 12:
        print("   ❌ All resources exhausted. Skipping this client.")
        return None, None

    active_key = get_current_api_key()
    
    # LOGIC: Switch model every 2 attempts (instead of 3)
    # This cycles through models faster if one is broken.
    model_index = (attempt // 2) % len(MODELS) 
    current_model = MODELS[model_index]
    
    print(f"   🤖 AI Drafting ({current_model}) using Key #{CURRENT_KEY_INDEX + 1}...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{current_model}:generateContent?key={active_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt = f"""
    Act as a expert Senior Web developer. Write a B2B cold email to {client_name}, the owner of {client_company}.
    
    **Sender:** "your name".
    **Contact:** "your email, numbers, website".
    
    **The Hook:**
    Most websites today are static. We build **Intelligent Web Ecosystems** using the modern 2026 tech stack.
    
    **Tech Stack:**
    1. **Web:** Next.js & React (Fast & SEO Optimized).
    2. **AI:** Custom Generative AI Agents (24/7 Support).
    
    **Goal:**
    Ask for a brief 10-minute demo.
    
    **Format:**
    Subject: [Catchy Subject]
    Body: [Concise Body]
    """
    
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        
        # RATE LIMIT (429) or SERVER OVERLOAD (503)
        if response.status_code in [429, 503]:
            print(f"   ⚠️ Busy ({response.status_code}) on {current_model}. Pausing 15s...")
            
            # INCREASED WAIT TIME: 15 seconds allows the API to breathe
            time.sleep(2)
            
            # Switch Key
            switch_api_key()
            
            return generate_smart_email(client_name, client_company, attempt + 1)
        
        if response.status_code == 404:
            print(f"   ⚠️ Model {current_model} error. Skipping to next model...")
            # Jump ahead 2 attempts to force a model switch
            return generate_smart_email(client_name, client_company, attempt + 2)
            
        if response.status_code == 200:
            try:
                text = response.json()['candidates'][0]['content']['parts'][0]['text']
                return parse_email_response(text)
            except:
                print("   ⚠️ JSON Parsing error, retrying...")
                return generate_smart_email(client_name, client_company, attempt + 1)
        else:
            print(f"   ❌ AI Error: {response.status_code}")
            switch_api_key()
            return generate_smart_email(client_name, client_company, attempt + 1)
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
        time.sleep(5)
        return generate_smart_email(client_name, client_company, attempt + 1)

def parse_email_response(text):
    lines = text.split('\n')
    subject = "Partnership Opportunity"
    body_lines = []
    
    for line in lines:
        if line.strip().lower().startswith("subject:"):
            subject = line.split(":", 1)[1].strip()
        elif "body:" not in line.lower():
            body_lines.append(line)
    return subject, "\n".join(body_lines).strip()

def send_email(to_email, subject, body):
    if DRY_RUN:
        print(f"   🐢 [DRY RUN] Generated for: {to_email}")
        return True

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"   ✅ Email ACTUALLY SENT to {to_email}")
        return True
    except Exception as e:
        print(f"   ❌ Failed to send: {e}")
        return False

def main():
    print("📂 Loading Client Data...")
    try:
        if CSV_FILE_PATH.endswith('.xls') or CSV_FILE_PATH.endswith('.xlsx'):
            df = pd.read_excel(CSV_FILE_PATH)
        else:
            df = pd.read_csv(CSV_FILE_PATH, encoding='latin1')
        
        df = df.rename(columns={"NAME OF BROKERS": "Name", "EMAIL ADDRESS": "Email", "BUSINESS NAME": "Company"})
        df = df.dropna(subset=["Email"])
        
        print(f"📊 Found {len(df)} contacts. Resuming from Row {START_FROM_ROW}...\n")
        
        count = 0
        for index, row in df.iterrows():
            if (count + 1) < START_FROM_ROW:
                count += 1
                continue

            name = row['Name']
            email = row['Email']
            company = row['Company']
            
            if "@" not in str(email): continue

            print(f"[{count+1}] Processing: {name} ({company})")
            
            subject, body = generate_smart_email(name, company)
            
            if subject and body:
                send_email(email, subject, body)
            
            print("   ⏳ Cooling down (35s)...")
            time.sleep(35)
            
            count += 1
            print("-" * 40)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()