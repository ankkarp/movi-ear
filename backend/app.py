import os
import glob
import aiofiles
from videohash import VideoHash
import time

# from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.responses import FileResponse

from model.src.main import pipeline
# import pandas as pd
# import numpy as np
import logging

# from video_utils import open_file

# from starlette.exceptions import HTTPException as StarletteHTTPException

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


app = FastAPI()
CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# engine = create_engine("postgresql://{user}:{psw}@{host}:{port}/{db}".format(
#     user=os.environ.get('PGUSER'),
#     psw=os.environ.get('POSTGRES_PASSWORD'),
#     host=os.environ.get('DB_HOST'),
#     port=os.environ.get('DB_PORT'),
#     db=os.environ.get('POSTGRES_DB'))
# )
# con = engine.connect()


@app.post("/upload")
async def upload(file=Form(None)):
    try:
        filepath = os.path.basename(file.filename)
        folder = os.environ.get("STORAGE")
        print(folder)
        filename = f'{time.time()}_{filepath}'
        filepath = f'{folder}/{filename}'
        async with aiofiles.open(filepath, 'wb') as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
        videohash = VideoHash(filepath).hash_hex[2:]

        if len(glob.glob(f'{os.environ.get("STORAGE")}/{videohash}*')):
            os.remove(filepath)
        else:
            hashedpath = f'{folder}/{videohash}_{filename}'
            pipeline(filepath, hashedpath)
            #os.remove(filepath, str(hashedpath))
            os.remove(filepath)
        return {"hash": videohash}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,
                            detail='There was an error uploading the file')


# @app.get("/video/{hash}")
# async def get_streaming_video(request: Request, videohash: str) -> StreamingResponse:
#     try:
#         file, status_code, content_length, headers = await open_file(request, videohash)
#         response = StreamingResponse(
#             file,
#             media_type='video/mp4',
#             status_code=status_code,
#         )

#         response.headers.update({
#             'Accept-Ranges': 'bytes',
#             'Content-Length': str(content_length),
#             **headers,
#         })
#         return response
#     except Exception:
#         raise HTTPException(status_code=404,
#                             detail='Файл не найден')

@app.get("/video/{videohash}")
def download_file(videohash):
    # print(f'{os.environ.get("STORAGE")}/{videohash}*.jpg')
    files = glob.glob(f'{os.environ.get("STORAGE")}/{videohash}*')
    if len(videohash) == 16 and len(files) > 0:
        filepath = files[0]
        return FileResponse(path=filepath, media_type='video/mp4')
    else:
        raise HTTPException(status_code=404, detail='Файл не найден')


# @app.get("/video/{videohash}")
# async def video_endpoint(videohash: str, range: str = Header(None)):
#     filepath = glob.glob(f'{os.environ.get("STORAGE")}/{videohash}*.mp4')[0]
#     # start, end = range.replace("bytes=", "").split("-")
#     # start = int(start)
#     # end = int(end) if end else start + CHUNK_SIZE
#     with open(filepath, "rb") as video:
#         # video.seek(start)
#         data = video.read()
#         # data = video.read(end - start)
#         # filesize = str(filepath.stat().st_size)
#         # headers = {
#         #     'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
#         #     'Accept-Ranges': 'bytes'
#         # }
#         return Response(data, status_code=200, headers=headers, media_type="video/mp4")


if __name__ == '__main__':
    #print(os.getcwd())
    uvicorn.run(app, host='localhost', port=8000)
