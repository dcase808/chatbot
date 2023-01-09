from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class Classifier:
    def load_model(self, model):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForSequenceClassification.from_pretrained(model)

    def score(self, context, prompts):
        highest_score = 0
        best_prompt = ''
        for prompt in prompts:
            input = self.tokenizer.encode(context + '<|endoftext|>' + prompt, return_tensors="pt")
            result = self.model(input, return_dict=True)
            print(prompt)
            current_score = torch.sigmoid(result.logits).squeeze().item()
            print(current_score)
            if current_score > highest_score:
                highest_score = current_score
                best_prompt = prompt
        print(f'RETURNING:\n {best_prompt}\nSCORE: {highest_score}\n')
        return best_prompt