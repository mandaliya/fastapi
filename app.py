import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

# ===============================
# 🚀 Configure Lightweight NLP Engine (Presidio Built-in)
# ===============================
nlp_configuration = {
    "nlp_engine_name": "presidio",
    "models": [{"lang_code": "en", "model_name": "en"}]
}

provider = NlpEngineProvider(nlp_configuration)
nlp_engine = provider.create_engine()

# Initialize Presidio Engines
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
anonymizer = AnonymizerEngine()

# ===============================
# 🚀 FastAPI Setup
# ===============================
app = FastAPI()

class TextRequest(BaseModel):
    text: str

# ===============================
# 🔍 PII Anonymization Endpoint
# ===============================
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

# ===============================
# ✅ Root Endpoint (Health Check)
# ===============================
@app.get("/")
def home():
    return {"message": "FastAPI PII Anonymization API is Running on Render!"}

# ===============================
# 🚀 Run the App on Render
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render uses port 10000
    uvicorn.run(app, host="0.0.0.0", port=port)
