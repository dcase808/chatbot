import gpt_2_simple as gpt2
import uuid

class GPT2():
    def __init__(self, length, temperature):
        self.conversations = {}
        self.length = length
        self.temperature = temperature
    
    def load_model(self, model):
        self.sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(self.sess, model_name=model, model_dir='models/gpt/models')

    def init_conv(self, name):
        conv_id = uuid.uuid4()
        self.conversations[conv_id] = []
        self.conversations[conv_id].append('USER: ')
        self.conversations[conv_id].append(f'My name is {name}. You are an AI. Answer questions as an AI.\n')
        self.conversations[conv_id].append('AI: ')
        self.conversations[conv_id].append('Okay, I will answer questions as an AI.\n')
        return conv_id

    def get_response(self, conv_id, prompt):
        if conv_id not in self.conversations:
            return False
        self.conversations[conv_id].append('USER: ')
        self.conversations[conv_id].append(f'{prompt}\n')
        self.conversations[conv_id].append('AI: ')
        answer = gpt2.generate(self.sess, model_name=self.model, model_dir='models/gpt/models', prefix=''.join(self.conversations[conv_id]), length=self.length, temperature=self.temperature, include_prefix=False, truncate='\n', return_as_list=True)
        self.conversations[conv_id].append(f'{answer[0]}\n')
        return answer[0]
