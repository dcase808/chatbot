from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Conversation, ConversationalPipeline
import uuid

class BlenderBot:
    def __init__(self, instruction):
        self.conversations = {}
        self.instruction = instruction
    
    def load_model(self, model):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model)
        self.conv_pipeline = ConversationalPipeline(model=self.model, tokenizer=self.tokenizer)
    
    def init_conv(self):
        conv_id = uuid.uuid4()
        self.conversations[conv_id] = Conversation()
        return conv_id
    
    def get_response(self, conv_id, prompt):
        self.conversations[conv_id].add_user_input(prompt)
        result = self.conv_pipeline([self.conversations[conv_id]], do_sample=False, max_length=1000)
        *_, last = result.iter_texts()
        self.conversations[conv_id].mark_processed()
        return(last[-1])
