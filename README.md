# Pronunciation Scorer API

This is a FastAPI service that accepts an audio file (.webm) and a target string (text to pronounce), then scores the pronunciation quality and returns the result.

## Features
- Accepts audio files via `multipart/form-data`
- Restricts uploads to audio/webm MIME types
- Enforces a file size limit (10 MB)
- Requires a target string to score against
- Returns pronunciation score and transcript

## Requirements
- Python 3.9+
- FastAPI
- Uvicorn

Install dependencies:

```bash
pip install -r requirements.txt
```

## Start Server
```bash 
uvicorn main:app --reload
```
## Alternative start script
``` 
py ./run.py 
```
## Example Request
```bash 
curl -X POST "http://127.0.0.1:5000/api/v1/score/" \
  -F "file=@sample.webm" \
  -F "target=hello world"
```

## TTS Options
By default the api uses recognize_google from speech_recognition, but you can specify a custom tts api route
```
# App config
...
tts_api_url = your_api_route
```

## Optimization Summary

### Handles 900% more Request Per Second
Before: 2.77 req/s -> After : 27.8 req/s

### Improved Average Request Duration by 96%
Before: 9.39 s -> After : 361.22 ms

[Details](./loadTest.md)

## Future Improvements
- Set up dedicated speech to text api as to not rely on recognizer_google.
- Containerization for easier deployment and scalibilty
