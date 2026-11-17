
import numpy as np
import pickle

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


# -----------------------------
# Initialize FastAPI
# -----------------------------

app = FastAPI(
    title="LSTM Next Word Prediction API",
    description="Predicts the top 3 next words using an LSTM model",
    version="1.0.0"
)


# -----------------------------
# CORS Configuration
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Load Model and Tokenizer
# -----------------------------

try:
    model = load_model("model.keras", compile=False)

    with open("tokenizer2.pkl", "rb") as f:
        tokenizer = pickle.load(f)

    max_length = model.input_shape[1]
    vocab_size = len(tokenizer.word_index) + 1

    if model.output_shape[-1] != vocab_size:
        raise ValueError(
            f"Model output size ({model.output_shape[-1]}) "
            f"does not match vocabulary size ({vocab_size}). "
            "Retrain the model with Dense(vocab_size)."
        )

    print("Model loaded successfully!")
    print("Vocabulary size:", vocab_size)
    print("Maximum sequence length:", max_length)

except Exception as e:
    raise RuntimeError(f"Failed to load model artifacts: {e}")


# -----------------------------
# Request Schema
# -----------------------------

class PredictionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)


# -----------------------------
# Prediction Endpoint
# -----------------------------

@app.post("/predict")
def predict(request: PredictionRequest):

    try:
        text = request.text.strip().lower()

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Input text cannot be empty"
            )

        # Convert text into token IDs
        token_sequence = tokenizer.texts_to_sequences([text])[0]

        if not token_sequence:
            raise HTTPException(
                status_code=400,
                detail="No known words found in input"
            )

        # Apply padding
        padded_sequence = pad_sequences(
            [token_sequence],
            maxlen=max_length,
            padding="pre",
            truncating="pre"
        )

        # Predict probabilities
        predictions = model.predict(
            padded_sequence,
            verbose=0
        )[0]

        # Get top 3 word indices, excluding padding index 0
        ranked_indices = np.argsort(predictions)[::-1]

        suggestions = []

        for idx in ranked_indices:
            if idx == 0:
                continue

            word = tokenizer.index_word.get(int(idx))

            if word and word not in suggestions:
                suggestions.append(word)

            if len(suggestions) == 3:
                break

        return {
            "input": text,
            "suggestions": suggestions
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "LSTM Next Word Prediction API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "vocabulary_size": vocab_size
    }
