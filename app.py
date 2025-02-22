from fastapi import FastAPI
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

app = FastAPI()

# Initialize Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

@app.post("/anonymize/")
async def anonymize_text(data: dict):
    text = data.get("text", "")

    # Step 1: Detect PII
    pii_entities = analyzer.analyze(text=text, entities=None, language="en")

    # Step 2: Anonymize detected PII
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=pii_entities)

    return {"original_text": text, "anonymized_text": anonymized_text.text}

