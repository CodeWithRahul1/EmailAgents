from email_reader_agent import email_reader_graph
from classification_agent import classification_graph
from action_agent import action_graph

# Step 1: Fetch emails from Email Reader Agent
email_data = email_reader_graph.invoke({})

# Step 2: Classify emails
classified_emails = classification_graph.invoke(email_data)
action_graph.invoke(classified_emails)

# Print categorized emails
for email in classified_emails["emails"]:
    print(f"📌 Category: {email['category']} | Subject: {email['subject']}")
