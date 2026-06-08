import fitz # PyMuPDF
import spacy
import re
from typing import Dict, Any

# Load spaCy model for NER
# In production, we'd use a better model or an LLM for complex extraction
# For now, we use the small English model and basic heuristics
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def parse_resume(file_bytes: bytes) -> Dict[str, Any]:
    """
    Parse resume text and extract entities.
    Returns a dictionary matching the schema structure.
    """
    text = extract_text_from_pdf(file_bytes)
    doc = nlp(text)

    # Basic extraction heuristics for Phase 1
    skills_list = ["Python", "SQL", "Machine Learning", "TypeScript", "FastAPI", "React", "PostgreSQL", "MongoDB", "Docker", "Azure", "AWS"]
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]

    # Extract name (simplified: first PERSON entity)
    name = "Unknown User"
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    return {
        "name": name,
        "skills": [{"name": s, "category": "General"} for s in set(found_skills)],
        "projects": [], # Advanced extraction needed for these
        "experiences": []
    }
