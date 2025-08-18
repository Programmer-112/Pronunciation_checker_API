# Pronunciation Scorer API

This is a FastAPI service that accepts an audio file and a target string (text to pronounce), then scores the pronunciation quality and returns the result.

## Features
- Accepts audio files via `multipart/form-data`
- Restricts uploads to audio MIME types
- Enforces a file size limit (10 MB)
- Requires a target string to score against
- Returns pronunciation score and transcript

## Requirements
- Python 3.9+
- FastAPI
- Uvicorn
- Your custom `scorer.py` module with a `Scorer` class

Install dependencies:

```bash
pip install fastapi uvicorn
```

## Start Server
```bash 
uvicorn main:app --reload
```
## Example Request
```bash 
curl -X POST "http://127.0.0.1:8000/score-audio/" \
  -F "file=@sample.wav" \
  -F "target=hello world"
```

