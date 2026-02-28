# 🚀 AutoMail AI: Resilient B2B Cold Email Automation

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini-orange?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

AutoMail AI is a production-ready Python script designed to automate highly personalized B2B cold email outreach. Built for reliability and scale, it utilizes Google's Generative AI to draft context-aware emails and sends them automatically via Gmail.

To ensure your campaigns run without interruption, this tool features built-in API key rotation, multi-model fallbacks, and intelligent rate-limit handling.

---

## ✨ Features

- **🧠 Dynamic AI Drafting:** Generates unique, personalized emails tailored to the client's name and company using advanced AI models.
- **🔄 Multi-Model Fallback:** Automatically cycles through models (`gemini-2.5-flash-lite`, `gemma-3-4b-it`, `gemini-2.5-flash`) to ensure continuous operation if one endpoint is busy.
- **🔑 API Key Rotation:** Seamlessly switches between an array of API keys to bypass `429 Too Many Requests` or `503 Service Unavailable` errors.
- **⏸️ Smart Resuming:** Easily start or resume your campaign from any specific row in your dataset, preventing duplicate sends.
- **🐢 Dry Run Mode:** Test the AI generation and console output safely without actually triggering any SMTP sends.
- **📊 Broad File Support:** Reads client data directly from `.xls`, `.xlsx`, or `.csv` files.

## 🛠️ Step-by-Step Setup Guide

Follow these steps to configure and run AutoMail AI on your local machine.

### 1. Clone the Repository
Open your terminal and clone this repository to your local machine:
```bash
git clone [https://github.com/NIKHILUTTAM/automail.git](https://github.com/NIKHILUTTAM/automail.git)
cd automail

```

### 2. Install Dependencies

Ensure you have Python 3.x installed. Then, install the required data processing and networking libraries:

```bash
pip install pandas requests openpyxl xlrd

```

### 3. Get Google GenAI API Keys

You need API keys to power the email generation engine.

1. Go to Google AI Studio.
2. Create 2 to 4 different API keys (Using multiple keys is highly recommended to prevent rate limiting).
3. Keep these keys secure for the configuration step.

### 4. Create a Gmail App Password

Standard Google passwords will not work for SMTP connections due to Two-Factor Authentication (2FA).

1. Go to your Google Account Security settings.
2. Ensure 2-Step Verification is enabled.
3. Search for App Passwords in the search bar.
4. Create a new App Password (e.g., name it "AutoMail").
5. Copy the generated 16-character password.

### 5. Configure the Script

Open `mail.py` and locate the `CONFIGURATION` section at the top. Update it with your credentials and preferences:

```python
# ================= CONFIGURATION =================

# 1. API KEYS
API_KEYS = [
    "YOUR_FIRST_API_KEY_HERE",
    "YOUR_SECOND_API_KEY_HERE"
]

# 2. EMAIL CREDENTIALS
SENDER_EMAIL = "your.email@gmail.com"
SENDER_PASSWORD = "your-16-digit-app-password" 

# 3. FILE SETTINGS
CSV_FILE_PATH = "your_client_data.xlsx" 

# 4. EXECUTION SETTINGS
START_FROM_ROW = 1 # Update this if the script stops and you need to resume
DRY_RUN = True # Set to False when you are ready to actually send emails

# =================================================

```

### 6. Format Your Client Data

Ensure your Excel or CSV file contains the correct column headers. By default, the script looks for the following columns to map data:

| Your File Header | Mapped To | Description |
| --- | --- | --- |
| `NAME OF BROKERS` | Client Name | Used for the personal greeting in the AI prompt. |
| `EMAIL ADDRESS` | Client Email | The destination address for the SMTP server. |
| `BUSINESS NAME` | Company Name | Context for the AI to personalize the pitch. |

*Note: If your dataset uses different headers, simply update the `df.rename()` function inside the `main()` block of `mail.py`.*

## 🚀 Usage

Once your data is formatted and your configuration is set, run the script from your terminal:

```bash
python mail.py

```

### Execution Flow

1. **Load:** The script loads your dataset and jumps directly to your configured `START_FROM_ROW`.
2. **Draft:** It drafts a custom email using the active AI model and API key.
3. **Send:** If the generation is successful (and `DRY_RUN` is False), it connects to the SMTP server and dispatches the email.
4. **Cooldown:** It implements a 35-second cooldown between emails to maintain a natural human-like sending cadence and protect your sender reputation from spam filters.

