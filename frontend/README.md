# Wordwave — LSTM next-word suggestion frontend

React + Vite + Tailwind UI inspired by a mobile suggestion keyboard.

## Start
```bash
npm install
cp .env.example .env
# Set VITE_API_URL to your Hugging Face Space endpoint ending in /predict
npm run dev
```
Build with `npm run build`.

## API contract
The frontend sends `POST` to `VITE_API_URL` with JSON:
```json
{"text":"your current sentence"}
```
It supports these JSON responses:
```json
["word one","word two","word three"]
```
or `{"suggestions":[...]}`, `{"words":[...]}`, `{"predictions":[...]}`, `{"next_words":[...]}`, or `{"top3":[...]}`. Array entries may be strings or objects with `word` / `text`.

If your FastAPI request model expects a different field, edit the `JSON.stringify({text:value.trim()})` line in `src/App.jsx`. The app assumes POST; adapt `predict()` if your API uses another method.

## CORS
Allow your frontend origin in FastAPI with `CORSMiddleware`, including `http://localhost:5173` during development. Do not ship private Hugging Face tokens in a public browser app.
