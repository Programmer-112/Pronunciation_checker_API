from io import BytesIO
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, status
from fastapi.params import Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import ffmpeg
from scorer import Scorer
import re

# FastAPI config
app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

version = 2
scorer = Scorer()
file_size_limit = 10 * 1024 * 1024  # 10MB
allowed_mime_types = ["audio/webm", "video/webm"]


async def read_webm_audio(file: UploadFile):
    webm_bytes = await file.read()

    # Validate file size
    if len(webm_bytes) > file_size_limit:
        raise ValueError("File size exceeds limit")

    return webm_bytes


async def convert_to_wav(webm_bytes:bytes):
    out, _ = (
        ffmpeg.input("pipe:0")  # read from stdin
        .output("pipe:1", format="wav", acodec="pcm_s16le")  # write to stdout
        .run(input=webm_bytes, capture_stdout=True, capture_stderr=True)
    )

    wav_bytes = BytesIO(out)
    return wav_bytes

def process_target(target:str):
    # remove all speical characters from target
    target = re.sub(r"[^a-zA-Z0-9 ]", "", target)
    return target


# accept audio file not longer than file_size_limit
# and a target string representing the words to be pronounced
@app.post("/api/v1/score/")
async def upload_audio(target: Annotated[str, Form(...)], file: UploadFile = File(...)):
    target = process_target(target=target)
    try:
        # Validate content type
        if not file.content_type or not file.content_type in allowed_mime_types:
            print(file.content_type)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Only webm files are allowed"},
            )
        if not target:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Target is required"},
            )

        webm_bytes = await read_webm_audio(file=file)
         
        wav_bytes = await convert_to_wav(webm_bytes)
        # remove all speical characters from target
        target = process_target(target=target)
        score, transcript = await scorer.async_score(wav_bytes, target)

        json_response = JSONResponse(
            content={
                "filename": file.filename,
                "content_type": file.content_type,
                "score": score,
                "transcript": transcript,
                "target": target,
                "version": version,
            }
        )
        print(f"INFO: {file.filename} scored {score}/1.0\n")
        print(f"INFO: {file.filename} transcript {transcript}\n")
        print(f"INFO: {file.filename} target {target}\n")

        return json_response

    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={
                "error": f"File size exceeds {file_size_limit / (1024 * 1024)}MB limit"
            },
        )

    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        raise


@app.get("/health")
async def health():
    return {"status": "ok"}
