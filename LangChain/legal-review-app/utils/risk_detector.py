def detect_risky_clauses(text):
    risky_terms = ["automatic renewal", "data collection", "arbitration clause", "opt-out"]
    highlighted_clauses = [clause for clause in text.split('.') if any(term in clause.lower() for term in risky_terms)]
    return highlighted_clauses
