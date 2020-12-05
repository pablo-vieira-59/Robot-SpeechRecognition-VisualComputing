
import chatbot

while 1:
    msg = input('Mensagem para o Chatbot:')
    pred, prob = chatbot.make_prediction(msg, chatbot.model_common)
    print('Classe : %s , Probalididade : %s %% \n' % (pred, prob))
    print(chatbot.gen_response(pred, msg))