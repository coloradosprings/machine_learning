
from fastapi import FastAPI
from typing import Optional
import json
import pathlib
import numpy as np



from app import (ml, config)

app = FastAPI()
settings = config.get_settings()

BASE_DIR = pathlib.Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR.parent / "models"
SMS_SPAM_MODEL_DIR = MODEL_DIR / "spam-sms"
MODEL_PATH = SMS_SPAM_MODEL_DIR / "spam-model.h5"
TOKENIZER_PATH = SMS_SPAM_MODEL_DIR / "spam-classifer-tokenizer.json"
METADATA_PATH = SMS_SPAM_MODEL_DIR / "spam-classifer-metadata.json"

SPAM_MODEL = None

@app.on_event("startup")
def on_startup():
    global AI_MODEL
    AI_MODEL = ml.AIModel(
        model_path = MODEL_PATH,
        tokenizer_path = TOKENIZER_PATH,
        metadata_path = METADATA_PATH )



    
@app.get("/") # /?q= this is awesome
def read_index(q:Optional[str] = None):
    global AI_MODEL
    query = q or"hello world"
    preds_dict = AI_MODEL.predict_text(query)
    return {"query" : query,"results": preds_dict}