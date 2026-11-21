WordWave — AI-Powered Next Word Prediction

WordWave is an AI-powered writing assistant that predicts the next words in a sentence using a custom-trained Long Short-Term Memory (LSTM) neural network. It helps users maintain their writing flow by generating intelligent word suggestions based on the context of their input.

The application combines a modern React interface with a FastAPI backend that serves a TensorFlow/Keras language model.

<p align="center">
  <a href="https://word-wave-wine.vercel.app/">Live Demo</a> •
  <a href="https://github.com/Siddharth-Jain-252/WordWave">Source Code</a>
</p>---

Table of Contents

- "Overview" (#overview)
- "Features" (#features)
- "How It Works" (#how-it-works)
- "System Architecture" (#system-architecture)
- "Technology Stack" (#technology-stack)
- "Machine Learning Model" (#machine-learning-model)
- "Project Structure" (#project-structure)
- "API Documentation" (#api-documentation)
- "Installation and Setup" (#installation-and-setup)
- "Configuration" (#configuration)
- "Running the Application" (#running-the-application)
- "Deployment" (#deployment)
- "Error Handling" (#error-handling)
- "Future Improvements" (#future-improvements)
- "Contributing" (#contributing)
- "License" (#license)

---

Overview

Traditional writing tools generally focus on spelling and grammar correction. WordWave takes a different approach by using a language model to predict what a user might want to write next.

Users enter a sentence or a partial thought, and the application processes the text through an LSTM-based neural network. The model analyzes the input sequence and returns the three most probable next words.

Users can select any suggestion to append it to their existing text and continue writing.

Problem Statement

Writing continuously can become difficult when users struggle to find the next appropriate word. WordWave addresses this problem through contextual word prediction.

Proposed Solution

WordWave provides an interactive writing environment backed by a trained neural network. Rather than generating an entire paragraph, it focuses on predicting the next word, allowing users to retain control over their writing.

---

Features

1. AI-Powered Next Word Prediction

- Uses a trained LSTM neural network.
- Analyzes the existing text as input.
- Generates the three most probable next words.
- Uses a tokenizer to convert text into numerical sequences.

2. Interactive Writing Interface

- Minimal and responsive writing environment.
- Live word counter.
- Clear text functionality.
- Keyboard shortcut ("Ctrl + Enter") to trigger predictions.

3. Smart Suggestion Bar

- Displays the top three predictions.
- Allows users to select a suggested word.
- Automatically appends the selected word to the existing text.
- Supports continuous writing and prediction.

4. Backend API Integration

- FastAPI-based prediction service.
- JSON-based communication between frontend and backend.
- Configurable prediction API endpoint.
- Error handling for unsuccessful API requests.

5. Model Integration

- Loads a pre-trained Keras model.
- Uses the corresponding tokenizer for text preprocessing.
- Maintains compatibility between the model vocabulary and tokenizer.
- Supports model inference without retraining on every request.

6. Additional Interface Features

- Copy written text to clipboard.
- Connection settings for configuring the prediction endpoint.
- Loading indicators during prediction.
- User-friendly error messages.

---

How It Works

WordWave follows a straightforward machine learning inference pipeline.

flowchart TD
    A[User enters text] --> B[React Frontend]
    B --> C[POST /predict]
    C --> D[FastAPI Backend]
    D --> E[Text Preprocessing]
    E --> F[Tokenizer]
    F --> G[Sequence Padding]
    G --> H[LSTM Model]
    H --> I[Probability Distribution]
    I --> J[Top 3 Word Selection]
    J --> K[JSON Response]
    K --> L[Suggestion Bar]
    L --> M[User selects a word]
    M --> A

Step 1: User Input

The user enters a sentence or partial text in the writing interface.

Example:

Machine learning is transforming

Step 2: Text Preprocessing

The backend:

- Converts input text to lowercase.
- Removes unnecessary surrounding whitespace.
- Converts words into token IDs using the trained tokenizer.
- Applies sequence padding to match the model's expected input length.

Step 3: Model Inference

The processed sequence is passed to the trained LSTM model.

The model generates a probability distribution over the vocabulary.

Step 4: Selecting Predictions

The backend ranks the predicted probabilities and selects the three highest-ranked valid words, excluding the padding token.

Step 5: Returning Suggestions

The API returns a JSON response containing the original input and the predicted words.

Step 6: Continuous Writing

The frontend displays the suggestions. Selecting a word appends it to the text, allowing the user to request another prediction.

---

System Architecture

WordWave follows a frontend-backend architecture with a separately trained machine learning model.

Component| Responsibility
React Frontend| Writing interface and user interaction
FastAPI Backend| Request handling and model inference
TensorFlow/Keras| Neural network inference
LSTM Model| Contextual next-word prediction
Tokenizer| Text-to-token conversion
NumPy| Probability ranking and numerical operations

The frontend communicates with the backend through HTTP requests. The backend loads the trained model and tokenizer and uses them to generate predictions.

---

Technology Stack

Frontend

Technology| Purpose
React 18| Component-based UI
Vite| Development server and build tool
Tailwind CSS| Styling and responsive design
Lucide React| Interface icons
JavaScript| Frontend application logic

Backend

Technology| Purpose
Python| Backend implementation
FastAPI| REST API framework
Uvicorn| ASGI server
TensorFlow| Deep learning framework
Keras| Model loading and inference
NumPy| Numerical computations
Pickle| Tokenizer serialization

Machine Learning

Technology| Purpose
LSTM| Sequential language modeling
Tokenization| Text preprocessing
Sequence Padding| Fixed-length model input
Softmax probabilities| Ranking predicted vocabulary words

---

Machine Learning Model

WordWave uses a Long Short-Term Memory (LSTM) neural network for next-word prediction.

LSTM is a type of recurrent neural network designed to learn dependencies in sequential data. It uses memory cells and gating mechanisms to retain relevant information across a sequence.

Prediction Pipeline

Input Text
    |
    v
Tokenization
    |
    v
Numerical Sequence
    |
    v
Sequence Padding
    |
    v
Trained LSTM Model
    |
    v
Probability Distribution
    |
    v
Top 3 Predictions

Model Artifacts

The backend requires two trained artifacts:

File| Description
"model.keras"| Trained LSTM neural network
"tokenizer2.pkl"| Fitted tokenizer containing vocabulary mappings

Important: Both artifacts must correspond to the same training run. The backend checks whether the model output dimension matches the tokenizer vocabulary size before serving predictions.

Inference Details

- Input is converted to lowercase.
- Unknown words are ignored by the tokenizer.
- Sequences are pre-padded to the model's expected input length.
- Long sequences are truncated from the beginning.
- Padding token index "0" is excluded from predictions.
- The backend returns up to three valid suggestions.

---

Project Structure

WordWave/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── model.keras
│   └── tokenizer2.pkl
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── ...
│   │
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── ...
│
├── training/
│   └── Model training scripts and related resources
│
└── README.md

Note: The structure above highlights the main application components. Model artifacts must be available in the backend working directory when starting the API.

---

API Documentation

WordWave uses FastAPI to expose the trained model through HTTP endpoints.

Base URL

http://localhost:8000

1. Health Check

Endpoint: "GET /"

Checks whether the API is running.

Example response:

{
  "status": "running",
  "message": "LSTM Next Word Prediction API"
}

2. Model Health Check

Endpoint: "GET /health"

Returns the model loading status and vocabulary information.

Example response:

{
  "status": "healthy",
  "model_loaded": true,
  "vocabulary_size": 10000
}

The vocabulary size shown above is illustrative and depends on the trained tokenizer.

3. Predict Next Words

Endpoint: "POST /predict"

Generates up to three next-word predictions.

Request:

{
  "text": "machine learning is transforming"
}

Response:

{
  "input": "machine learning is transforming",
  "suggestions": [
    "technology",
    "industries",
    "business"
  ]
}

The suggested words are illustrative. Actual predictions depend on the trained model.

Request Validation:

- "text" is required.
- Minimum input length: 1 character.
- Maximum input length: 500 characters.
- Input must contain at least one word recognized by the tokenizer.

API Documentation Interface

FastAPI automatically provides interactive API documentation.

http://localhost:8000/docs

---

Installation and Setup

Follow these instructions to run WordWave locally.

Prerequisites

Install the following:

- Python 3.10+
- Node.js and npm
- Git
- Access to the trained model artifacts

1. Clone the Repository

git clone https://github.com/Siddharth-Jain-252/WordWave.git

cd WordWave

2. Backend Setup

Navigate to the backend directory:

cd backend

Create a virtual environment:

Windows:

python -m venv venv
venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Ensure the following files are available in the backend directory:

model.keras
tokenizer2.pkl

3. Start the Backend

Run:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

The API will be accessible at:

http://localhost:8000

4. Frontend Setup

Open another terminal and navigate to the frontend directory:

cd frontend

Install dependencies:

npm install

5. Configure the Backend URL

Create a ".env" file inside the frontend directory:

VITE_API_URL=http://localhost:8000/predict

6. Start the Frontend

npm run dev

Vite will display the local development URL, usually:

http://localhost:5173

Open the URL in your browser to start using WordWave.

---

Configuration

The frontend supports configuring the prediction endpoint through its settings interface.

Alternatively, use the following environment variable:

VITE_API_URL=https://your-api-domain/predict

For example, if the backend is deployed on Hugging Face Spaces:

VITE_API_URL=https://your-space.hf.space/predict

Restart the frontend development server after changing environment variables.

Security Note: Never expose private API credentials or secret tokens through frontend environment variables. Variables prefixed with "VITE_" are included in the client-side build.

---

Deployment

WordWave separates frontend hosting from machine learning inference hosting.

Frontend Deployment

The frontend is deployed using Vercel.

To deploy another instance:

1. Import the GitHub repository into Vercel.
2. Set the project root directory to "frontend".
3. Configure the build command as "npm run build".
4. Configure the output directory as "dist".
5. Add the "VITE_API_URL" environment variable.
6. Deploy the application.

Backend Deployment

The FastAPI backend can be hosted on a Python-compatible platform, including Hugging Face Spaces.

Deployment requirements:

- Install dependencies from "requirements.txt".
- Include "model.keras" and "tokenizer2.pkl".
- Start the FastAPI application using Uvicorn.
- Configure the frontend with the deployed "/predict" endpoint.
- Configure CORS with trusted frontend origins for production.

---

Error Handling

The backend handles several common prediction errors.

Scenario| HTTP Status| Description
Empty or invalid input| 422| Request validation failure
No recognized words| 400| Tokenizer cannot process the input
Invalid model artifacts| Startup failure| Model or tokenizer loading failed
Internal prediction failure| 500| Unexpected inference error

The frontend also handles:

- Missing API configuration.
- Backend connection failures.
- Unsuccessful HTTP responses.
- Empty prediction responses.
- Loading states during inference.

---

Future Improvements

Potential improvements for future versions include:

- Context-Aware Predictions: Improve prediction quality by training on larger and more diverse datasets.
- Transformer-Based Models: Experiment with Transformer architectures for improved contextual understanding.
- Personalized Suggestions: Adapt predictions to individual writing styles.
- Sentence Completion: Extend the system from single-word prediction to phrase and sentence generation.
- Multilingual Support: Support next-word prediction across multiple languages.
- Prediction Performance: Optimize model inference latency and resource consumption.
- Keyboard Integration: Extend the application into a browser extension or virtual keyboard.
- Model Evaluation: Introduce top-k accuracy, perplexity, and other language-model evaluation metrics.

---
