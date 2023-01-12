from fastapi import FastAPI, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models.godel.Godel import Godel
from models.blenderbot.BlenderBot import BlenderBot
import torch
import uuid
import io

MODEL = 'facebook/blenderbot-400M-distill'
TXT2IMG_MODEL = 'stabilityai/stable-diffusion-2'

app = FastAPI()
blenderbot = BlenderBot()
use_cuda = torch.cuda.is_available()
if use_cuda:
    from models.stablediffusion.StableDiffusion import StableDiffusion
    stablediffusion = StableDiffusion()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_headers=['*'],
    allow_methods=['*']
)

@app.on_event('startup')
def startup_event():
    blenderbot.load_model(MODEL)
    if use_cuda:
        stablediffusion.load_model(TXT2IMG_MODEL)

@app.get('/init')
def init():
    conv_id = blenderbot.init_conv()
    return {
        'conv_id': conv_id
    }

@app.post('/generate')
def generate(conv_id: str, prompt: str):
    conv_id = uuid.UUID(conv_id)
    response = blenderbot.get_response(conv_id, prompt)
    return {
        'conv_id': conv_id,
        'response': response
    }

@app.post('/txt2img', responses = {200: {"content": {"image/png": {}}}}, response_class=Response)
def txt2img(prompt: str):
    if not use_cuda:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="no CUDA device detected")
    image = stablediffusion.generate_img(prompt)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()
    return Response(content=image_bytes, media_type="image/png")