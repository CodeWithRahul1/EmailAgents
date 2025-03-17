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
