import os
import aiofiles
from videohash import VideoHash
import time
from typing import Optional, List

# from sqlalchemy import create_engine, text
# from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# import pandas as pd
# import numpy as np
import logging

# from starlette.exceptions import HTTPException as StarletteHTTPException

# load_dotenv()

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
async def get_sports(file=Form(None)):
    try:
        filepath = os.path.basename(file.filename)
        folder = 'data'
        filename = f'{time.time()}_{filepath}'
        filepath = f'{folder}/{filename}'
        async with aiofiles.open(filepath, 'wb') as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
        videohash = VideoHash(filepath).hash_hex
        hashedpath = f'{folder}/{videohash}_{filename}'
        os.rename(filepath, str(hashedpath))
        return {"hash": videohash}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,
                            detail='There was an error uploading the file')
    finally:
        await file.close()


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
