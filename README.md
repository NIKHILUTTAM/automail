# 🚀 AutoMail AI: Resilient B2B Cold Email Automation

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini-orange?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

AutoMail AI is a production-ready Python script designed to automate highly personalized B2B cold email outreach. Built for reliability, it utilizes Google's Generative AI to draft context-aware emails and sends them automatically via Gmail. 

To ensure your campaigns run without interruption, this tool features built-in API key rotation, multi-model fallbacks, and intelligent rate-limit handling.

---

## ✨ Features

- **🧠 Dynamic AI Drafting:** Generates unique, personalized emails tailored to the client's name and company using advanced AI models.
- **🔄 Multi-Model Fallback:** Automatically cycles through models (`gemini-2.5-flash-lite`, `gemma-3-4b-it`, `gemini-2.5-flash`) to ensure continuous operation if one endpoint is busy.
- **🔑 API Key Rotation:** Seamlessly switches between an array of API keys to bypass `429 Too Many Requests` or `503 Service Unavailable` errors.
- **⏸️ Smart Resuming:** Easily start or resume your campaign from any specific row in your dataset.
- **🐢 Dry Run Mode:** Test the AI generation and console output safely without actually sending any emails.
- **📊 Broad File Support:** Reads client data directly from `.xls`, `.xlsx`, or `.csv` files.

---

## 🛠️ Step-by-Step Setup Guide

Follow these steps to configure and run AutoMail AI on your local machine.

### 1. Clone the Repository
Open your terminal and clone this repository:
```bash
git clone [https://github.com/NIKHILUTTAM/automail.git](https://github.com/NIKHILUTTAM/automail.git)
cd automail
