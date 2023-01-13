from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch

class StableDiffusion:
    def __init__(self):
        self.use_cuda = torch.cuda.is_available()
    
    def load_model(self, model):
        self.scheduler = EulerDiscreteScheduler.from_pretrained(model, subfolder="scheduler")
        if self.use_cuda:
            self.pipe = pipe = StableDiffusionPipeline.from_pretrained(model, scheduler=self.scheduler, torch_dtype=torch.float32)
            self.pipe = pipe.to('cuda')
        else:
            self.pipe = pipe = StableDiffusionPipeline.from_pretrained(model, scheduler=self.scheduler, torch_dtype=torch.float32)
            self.pipe = pipe.to('cpu')
        self.pipe.enable_attention_slicing()
    
    def generate_img(self, prompt):
        if self.use_cuda:
            image = self.pipe(prompt, num_inference_steps=20, width=256, height=256).images[0]
        return image
