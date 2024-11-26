from utils.document_loader import load_pdf_document
from utils.text_splitter import split_document
from utils.clause_extractor import extract_key_clauses_from_chunks
from utils.risk_detector import detect_risky_clauses

def analyze_document(file_path):
    # Step 1: Load the document (can be PDF, DOCX, etc.)
    text = load_pdf_document(file_path)

    # Step 2: Split the document into chunks for easier processing
    chunks = split_document(text)

    # Step 3: Extract key clauses (privacy, liability, payment, etc.)
    clauses = extract_key_clauses_from_chunks(chunks)

    # Step 4: Detect risky clauses (e.g., automatic renewal, arbitration)
    risky_clauses = detect_risky_clauses(text)

    # Combine all analysis results into a report
    analysis_report = {
        "key_clauses": clauses,
        "risky_clauses": risky_clauses,
        "full_text": text
    }
    return analysis_report
