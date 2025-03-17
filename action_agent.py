import imaplib
import email
from email.header import decode_header
from langgraph.graph import StateGraph
from typing import TypedDict, List
import os

# Email Credentials (Use environment variables in production)
EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"

# Define email structure
class EmailData(TypedDict):
    subject: str
    sender: str
    date: str
    body: str
    category: str  # Already classified

# Define state schema
class ActionState(TypedDict):
    emails: List[EmailData]

# Mapping categories to Gmail folders
FOLDER_MAPPING = {
    "Job": "INBOX/Job",
    "LinkedIn": "INBOX/LinkedIn",
    "Spam": "INBOX/Spam",
    "Medium": "INBOX/Medium",
    "Other": "INBOX/Misc"
}

def move_email(email_subject, category):
    """Move email to the corresponding folder in Gmail."""
    try:
        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        # Search for the email by subject
        status, messages = mail.search(None, f'SUBJECT "{email_subject}"')

        if status == "OK":
            for num in messages[0].split():
                target_folder = FOLDER_MAPPING.get(category, "INBOX/Misc")
                
                # Move email
                mail.store(num, "+X-GM-LABELS", target_folder)
                print(f"✅ Moved '{email_subject}' to {target_folder}")

        mail.logout()
    except Exception as e:
        print(f"❌ Error moving email '{email_subject}': {e}")

# Define workflow
workflow = StateGraph(ActionState)

def process_emails(state: ActionState) -> ActionState:
    """Moves classified emails to the correct folder."""
    emails = state.get("emails", [])

    for email in emails:
        move_email(email["subject"], email["category"])

    return {"emails": emails}

# Define graph
workflow.add_node("move_emails", process_emails)
workflow.set_entry_point("move_emails")
action_graph = workflow.compile()
