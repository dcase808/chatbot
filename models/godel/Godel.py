from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import uuid
from models.dialogrpt.Classifier import Classifier

class Godel:
    def __init__(self, instruction):
        self.conversations = {}
        self.instruction = instruction
        self.classifier = Classifier()
    
    def load_model(self, model, classifier_model):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model)
        self.classifier.load_model(classifier_model)
    
    def init_conv(self):
        conv_id = uuid.uuid4()
        self.conversations[conv_id] = []
        return conv_id
    
    def get_response(self, conv_id, prompt):
        self.conversations[conv_id].append(f'{prompt}\n')
        dialog = ''.join(self.conversations[conv_id])
        query = f"{self.instruction} [CONTEXT] {dialog}"
        print(query)
        input_ids = self.tokenizer(f"{query}" + self.tokenizer.eos_token, return_tensors="pt").input_ids
        output_list = []
        for _ in range(5):
            outputs = self.model.generate(input_ids, max_length=128, min_length=8, top_p=0.9, do_sample=True)
            output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            output_list.append(output)
        out = self.classifier.score(dialog, output_list)
        print(f'GOT:\n {out}\n FROM CLASSIFIER\n')
        self.conversations[conv_id].append(out + '\n')
        return out
