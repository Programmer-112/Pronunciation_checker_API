from io import BytesIO
from typing import Annotated

from fastapi import FastAPI, File, UploadFile, status
from fastapi.params import Form
from fastapi.responses import JSONResponse

from scorer import Scorer

app = FastAPI()

scorer = Scorer()

file_size_limit = 10 * 1024 * 1024  # 10MB

# accept audio file not longer than file_size_limit
# and a target string representing the words to be pronounced
@app.post("/score-audio/")
async def upload_audio(target:  Annotated[str, Form(...)], file: UploadFile = File(...)):
    try:
        # Validate content type
        if not file.content_type or not file.content_type.startswith('audio/'):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Only audio files are allowed"}
            )

        if not target:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Target is required"}
            )
    
        contents = await file.read()
        
        # Validate file size after reading (in case size wasn't available before)
        if len(contents) > file_size_limit:
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={"error": f"File size exceeds {file_size_limit / (1024 * 1024)}MB limit"}
            )

        audio_stream = BytesIO(contents)
        score, transcript = await scorer.async_score(audio_stream, target)
        # score, transcript =  scorer.sync_score(audio_stream, target)
        return JSONResponse(content={
            "filename": file.filename,
            "content_type": file.content_type,
            "score": score,
            "transcript": transcript
        })

    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        raise
@app.get("/health")
async def health():
    return {"status": "ok"}
