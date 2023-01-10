from fastapi import FastAPI
from models.godel.Godel import Godel
import uuid

MODEL = 'microsoft/GODEL-v1_1-large-seq2seq'
CLASSIFIER_MODEL = 'microsoft/DialogRPT-human-vs-rand'

app = FastAPI()
godel = Godel('Instruction: given a dialog context, you need to response empathically. ')

@app.on_event('startup')
def startup_event():
    godel.load_model(MODEL, CLASSIFIER_MODEL)

@app.post('/init')
def init():
    conv_id = godel.init_conv()
    return {
        'conv_id': conv_id
    }

@app.post('/generate')
def init(conv_id: str, prompt: str):
    conv_id = uuid.UUID(conv_id)
    response = godel.get_response(conv_id, prompt)
    return {
        'conv_id': conv_id,
        'response': response
    }