from fastapi import FastAPI, Response
from models.godel.Godel import Godel
from models.stablediffusion.StableDiffusion import StableDiffusion
import uuid
import io

MODEL = 'microsoft/GODEL-v1_1-large-seq2seq'
CLASSIFIER_MODEL = 'microsoft/DialogRPT-human-vs-rand'
TXT2IMG_MODEL = 'stabilityai/stable-diffusion-2'

app = FastAPI()
godel = Godel('Instruction: given a dialog context, you need to response empathically. ')
stablediffusion = StableDiffusion()

@app.on_event('startup')
def startup_event():
    #godel.load_model(MODEL, CLASSIFIER_MODEL)
    stablediffusion.load_model(TXT2IMG_MODEL)

@app.post('/init')
def init():
    conv_id = godel.init_conv()
    return {
        'conv_id': conv_id
    }

@app.post('/generate')
def generate(conv_id: str, prompt: str):
    conv_id = uuid.UUID(conv_id)
    response = godel.get_response(conv_id, prompt)
    return {
        'conv_id': conv_id,
        'response': response
    }

@app.post('/txt2img', responses = {200: {"content": {"image/png": {}}}}, response_class=Response)
def txt2img(prompt: str):
    image = stablediffusion.generate_img(prompt)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()
    return Response(content=image_bytes, media_type="image/png")