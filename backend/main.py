from fastapi import FastAPI
from pydantic import BaseModel
from langdetect import detect, LangDetectException
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dynamic Translation Pipeline Cache ---
translators = {}

# --- Updated Request Schema ---
class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None

@app.get("/")
def home():
    return {"message": "Welcome to the Universal Translator API 🚀"}

@app.post("/translate")
def translate_text(request: TranslationRequest):
    source_lang = request.source_language
    final_source_lang = source_lang

    # 1. Detect language if not provided
    if not source_lang:
        try:
            detected_lang = detect(request.text)
            source_lang = detected_lang
            final_source_lang = detected_lang
        except LangDetectException:
            logger.warning(f"Could not detect language. Defaulting to 'en'.")
            source_lang = "en"
            final_source_lang = "en"

    translator_key = f"{source_lang}-{request.target_language}"
    translator = None

    # 2. Try to load the detected language model
    if translator_key in translators:
        translator = translators[translator_key]
    else:
        try:
            model_name = f"Helsinki-NLP/opus-mt-{translator_key}"
            logger.info(f"Attempting to load model: {model_name}")
            translators[translator_key] = pipeline("translation", model=model_name)
            translator = translators[translator_key]
            logger.info(f"Successfully loaded model: {model_name}")
        except Exception:
            logger.warning(f"Could not load model for '{translator_key}'.")
            translator = None

    # 3. --- FALLBACK LOGIC ---
    # If the first attempt failed, fall back to English
    if translator is None and source_lang != 'en':
        logger.warning(f"Falling back to English for translation.")
        final_source_lang = 'en'
        fallback_key = f"en-{request.target_language}"
        
        if fallback_key in translators:
            translator = translators[fallback_key]
        else:
            try:
                model_name = f"Helsinki-NLP/opus-mt-{fallback_key}"
                logger.info(f"Attempting to load fallback model: {model_name}")
                translators[fallback_key] = pipeline("translation", model=model_name)
                translator = translators[fallback_key]
                logger.info(f"Successfully loaded fallback model: {model_name}")
            except Exception as e:
                logger.error(f"Failed to load even the fallback model '{model_name}'. Error: {e}")
                return {"error": f"Translation to '{request.target_language}' is not supported."}

    # If no translator could be loaded at all, return an error
    if translator is None:
        return {"error": f"Translation from '{source_lang}' to '{request.target_language}' is not supported."}

    # 4. Perform the translation
    try:
        result = translator(request.text, max_length=512)[0]["translation_text"]
        return {
            "source_language": final_source_lang,
            "target_language": request.target_language,
            "input_text": request.text,
            "translated_text": result
        }
    except Exception as e:
        logger.error(f"Translation failed for key {translator_key}: {e}")
        return {"error": "An unexpected error occurred during translation."}

# To run: uvicorn main:app --reload
