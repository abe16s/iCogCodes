from models.contract_analysis_model import analyze_document

file_path = "data/terms_and_conditions.pdf"

# Get the analysis report
analysis_report = analyze_document(file_path)

print("Key Clauses:")
for clause in analysis_report["key_clauses"]:
    print(f"- {clause}")

print("\nRisky Clauses:")
for clause in analysis_report["risky_clauses"]:
    print(f"- {clause}")
