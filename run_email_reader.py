from email_reader_agent import email_reader_graph

# Run the Langraph workflow
result = email_reader_graph.invoke({})
print(result["emails"])  # Print extracted emails
