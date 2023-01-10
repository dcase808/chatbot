from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch

class StableDiffusion:
    def __init__(self):
        pass
    
    def load_model(self, model):
        self.scheduler = EulerDiscreteScheduler.from_pretrained(model, subfolder="scheduler")
        self.pipe = pipe = StableDiffusionPipeline.from_pretrained(model, scheduler=self.scheduler, torch_dtype=torch.float16)
        self.pipe = pipe.to('cuda')
        self.pipe.enable_attention_slicing()
    
    def generate_img(self, prompt):
        image = self.pipe(prompt, num_inference_steps=50, width=512, height=512).images[0]
        return image
