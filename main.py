import os

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

files = {
    item: os.path.join('samples_directory', item)
    for item in os.listdir('samples_directory')
}

some_file_path = "samples_directory/file_sample.avi"
app = FastAPI()
templates = Jinja2Templates(directory="templates")
origins = [
    "http://localhost",
    "http://localhost:5000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_video/{video_name}")
async def get_video(video_name: str, response_class=StreamingResponse):
    video_path = files.get(video_name)
    if video_path:
        return StreamingResponse(open(video_path, 'rb'))
    else:
        return Response(status_code=404)


@app.get('/play_video/{video_name}')
async def play_video(video_name: str, request: Request, response_class=HTMLResponse):
    video_path = files.get(video_name)
    if video_path:
        return templates.TemplateResponse(
            'play_video.html', {'request': request, 'video': {'path': video_path, 'name': video_name}})
    else:
        return Response(status_code=404)


@app.get('/play_video_wasm/{video_name}')
async def play_video(video_name: str, request: Request, response_class=HTMLResponse):
    video_path = files.get(video_name)
    if video_path:
        return templates.TemplateResponse(
            'wasm_player.html', {'request': request, 'video': {'path': video_path, 'name': video_name}})
    else:
        return Response(status_code=404)


@app.get('/')
async def videos_list(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("videos_list.html", {'request': request, 'files': files})


@app.get('/ping')
async def ping_pong():
    return {'message': 'pong'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
