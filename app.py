import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Initialize FastAPI app
app = FastAPI()

# Initialize Presidio Engines
analyzer = AnalyzerEngine(nlp_engine_name="spacy", supported_languages=["en"])
anonymizer = AnonymizerEngine()

# Define request model
class TextRequest(BaseModel):
    text: str

@app.post("/anonymize/")
def anonymize_text(request: TextRequest):
    text = request.text

    # Step 1: Detect PII (Personally Identifiable Information)
    entities = analyzer.analyze(text=text, entities=None, language="en")

    # Step 2: Anonymize detected PII
    anonymized_result = anonymizer.anonymize(text=text, analyzer_results=entities)

    return {
        "original_text": text,
        "anonymized_text": anonymized_result.text
    }

@app.get("/")
def home():
    return {"message": "FastAPI PII Anonymization API is Running on Render!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's default port
    uvicorn.run(app, host="0.0.0.0", port=port, workers=1)
