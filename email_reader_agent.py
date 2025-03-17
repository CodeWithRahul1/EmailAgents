import os
import imapclient
import email
from email.header import decode_header
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from typing import TypedDict, List

# Load environment variables
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_FOLDER = os.getenv("EMAIL_FOLDER", "INBOX")

class EmailData(TypedDict):
    subject: str
    sender: str
    date: str
    body: str

class EmailReaderAgent:
    def __init__(self):
        self.client = imapclient.IMAPClient(EMAIL_HOST, ssl=True)

    def login(self):
        """Log in to the email account."""
        try:
            self.client.login(EMAIL_USER, EMAIL_PASS)
            print("✅ Logged in successfully.")
        except Exception as e:
            print(f"❌ Login failed: {e}")

    def fetch_unseen_emails(self, max_emails=5) -> List[EmailData]:
        """Fetch unseen emails from the inbox."""
        self.client.select_folder(EMAIL_FOLDER)
        unseen_messages = self.client.search("UNSEEN")
        
        print(f"📩 Found {len(unseen_messages)} unseen emails.")
        
        emails = []
        for msgid in unseen_messages[:max_emails]:  # Limit for testing
            raw_message = self.client.fetch([msgid], ["RFC822"])
            email_obj = email.message_from_bytes(raw_message[msgid][b"RFC822"])
            
            subject, encoding = decode_header(email_obj["Subject"])[0]
            subject = subject.decode(encoding) if encoding else subject

            sender = email_obj["From"]
            date = email_obj["Date"]

            # Extract email content
            body = ""
            if email_obj.is_multipart():
                for part in email_obj.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = email_obj.get_payload(decode=True).decode(errors="ignore")

            emails.append({"subject": subject, "sender": sender, "date": date, "body": body})

        return emails

    def logout(self):
        """Logout from the email account."""
        self.client.logout()
        print("🔒 Logged out.")

# Define the state schema for Langraph
class EmailReaderState(TypedDict):
    emails: List[EmailData]

# Define the workflow
workflow = StateGraph(EmailReaderState)

def read_emails(state: EmailReaderState) -> EmailReaderState:
    """Langraph step to read emails."""
    agent = EmailReaderAgent()
    agent.login()
    emails = agent.fetch_unseen_emails()
    agent.logout()
    
    state["emails"] = emails
    return state

# Add the step to the workflow
workflow.add_node("read_emails", read_emails)
workflow.set_entry_point("read_emails")
email_reader_graph = workflow.compile()
from langgraph.graph import StateGraph
from typing import TypedDict, List
import re

# Define email structure
class EmailData(TypedDict):
    subject: str
    sender: str
    date: str
    body: str
    category: str  # New field for classified category

# Define state schema
class ClassificationState(TypedDict):
    emails: List[EmailData]

# Keyword-based classification function
def classify_email(email: EmailData) -> str:
    """Classifies email into categories based on keywords."""
    job_keywords = ["interview", "job offer", "hiring", "recruitment"]
    linkedin_keywords = ["linkedin"]
    spam_keywords = ["lottery", "win", "prize", "urgent"]
    medium_keywords = ["medium", "newsletter"]

    subject = email["subject"].lower()
    body = email["body"].lower()

    if any(word in subject or word in body for word in job_keywords):
        return "Job"
    elif any(word in subject or word in body for word in linkedin_keywords):
        return "LinkedIn"
    elif any(word in subject or word in body for word in spam_keywords):
        return "Spam"
    elif any(word in subject or word in body for word in medium_keywords):
        return "Medium"
    else:
        return "Other"

# Classification workflow
workflow = StateGraph(ClassificationState)

def classify_emails(state: ClassificationState) -> ClassificationState:
    """Langraph step to classify emails."""
    emails = state.get("emails", [])
    
    for email in emails:
        email["category"] = classify_email(email)  # Assign category
    
    return {"emails": emails}

# Define graph
workflow.add_node("classify_emails", classify_emails)
workflow.set_entry_point("classify_emails")
classification_graph = workflow.compile()
