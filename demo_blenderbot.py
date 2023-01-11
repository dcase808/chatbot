from models.blenderbot.BlenderBot import BlenderBot

bbot = BlenderBot('yo')
bbot.load_model('facebook/blenderbot-1B-distill')
id = bbot.init_conv()
while True:
    print('Prompt:\n')
    print(bbot.get_response(id, input()))
