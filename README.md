# Multi-Agent Email Classification System

## 📌 Overview
This project implements a multi-agent system using Langraph to automate email processing. The system consists of three agents:

1. **Email Reader Agent** – Fetches unseen emails from an email inbox.
2. **Classification Agent** – Uses AI to categorize emails into predefined labels (e.g., Job, LinkedIn, Spam, Medium, etc.).
3. **Action Agent** – Moves classified emails into appropriate folders or applies labels.

## 🚀 Features
- Automatically fetches unseen emails.
- AI-powered classification of emails.
- Moves emails to the correct folders based on their category.

## 🏗 Project Structure
```
email_multi_agent/
│── email_reader_agent.py   # Fetches emails
│── classification_agent.py # Classifies emails using AI
│── action_agent.py         # Moves emails based on classification
│── run_email_reader.py     # Runs the Email Reader Agent
│── test.py                 # Tests the full workflow
│── requirements.txt        # Dependencies
│── README.md               # Project Documentation
```

## 🔧 Installation & Setup

### 1️⃣ Create a Virtual Environment
```bash
python3 -m venv emailvenv
source emailvenv/bin/activate  # On Windows, use: emailvenv\Scripts\activate
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Email Credentials
Edit `email_reader_agent.py` and `action_agent.py` to add your email and app password:
```python
EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"  # Use an App Password, NOT your email password
```

### 4️⃣ Run the Email Reader Agent
```bash
python run_email_reader.py
```

### 5️⃣ Run Full Workflow
```bash
python test.py
```

## ⚙️ How It Works
1. The **Email Reader Agent** logs into the email inbox and fetches unseen emails.
2. The **Classification Agent** processes the emails and categorizes them using AI.
3. The **Action Agent** moves the emails to the correct folders.
4. The system logs all actions taken.

## 🤖 AI Used in Classification
- Uses NLP techniques (e.g., TF-IDF, BERT, or Llama-2) to analyze email content.
- Classifies emails into predefined categories.

## 🛠 Troubleshooting
**Authentication Failed Error:**
- Enable **IMAP** in Gmail settings.
- Use an **App Password** instead of your regular password.

**No Emails Found:**
- Ensure there are unseen emails in your inbox.

## 📌 Future Enhancements
- **Auto-reply agent** to send responses based on email type.
- **Summarization agent** to provide brief email summaries.
- **Customizable rules** for classification.

---
### 📝 Author: Rahul
Feel free to contribute or suggest improvements! 🚀


