import jsonpickle
import telebot
import requests
from config import TELEGRAM_API_KEY
import json
import time

def getMessageInfos(data):
    messageKeys =  {"completeAnalysis": None,"profileUser": None, "network":None, "language":None }
    
    if("profiles" in data):
        if ("bot_probability" in data["profiles"][0] and "all" in data["profiles"][0]["bot_probability"] ):
            messageKeys["completeAnalysis"] = data["profiles"][0]["bot_probability"]["all"]
            
        if ("language_independent" in data["profiles"][0]):

            if ("user" in data["profiles"][0]["language_independent"]):
                messageKeys["profileUser"] = data["profiles"][0]["language_independent"]["user"]

            if ("network" in data["profiles"][0]["language_independent"]):
                messageKeys["network"] = data["profiles"][0]["language_independent"]["network"]

        if ("sentiment" in data["profiles"][0]["language_dependent"] and "value" in data["profiles"][0]["language_dependent"]["sentiment"]):
            messageKeys["language"] = data["profiles"][0]["language_dependent"]["sentiment"]["value"]

    return messageKeys


def allowMessages(message):
    return True
def getWords(text):
    textArray = " ".join(text.split())
    textArray = text.split()
    return textArray[1:]

if __name__ == "__main__":
    bot = telebot.TeleBot(TELEGRAM_API_KEY)
    URL = "https://pegabot.com.br/botometer?"
    
    @bot.message_handler(commands=["analise"])
    def analysis(message):
        # try:
            formattedMessage = jsonpickle.encode(message)
            formattedMessage  = json.loads(formattedMessage)
            itemsToSearch = getWords(formattedMessage["text"])
            # URL = "https://pegabot.com.br/botometer?profile=twitter&search_for=profile&is_admin=true"
            
            if itemsToSearch != [""]:
                print("Words\n\n")
                print(itemsToSearch)
                for i in range(len(itemsToSearch)):
                    print(itemsToSearch[i])
                    PARAMS = {"profile":itemsToSearch[i].strip(), "search_for":"profile", "is_admin":"true"}
                    print("\n\n\n")
                    r = requests.get(url = URL, params =PARAMS)
                    data = r.json()
                    messageKeys = getMessageInfos(data)
                    print(messageKeys)

                    INITIAL_MSG = "Probabilidade de ser um robô: \n\n"
                    messageToUser = INITIAL_MSG

                    keys= ["completeAnalysis", "profileUser", "network", "language"]
                    profileMsgs = ["Análise completa", "Perfil do usuário", "Rede (seguidores e seguidos)", "Linguagem utilizada nos tweets"]

                    for i in range(len(keys)):
                        if (messageKeys[keys[i]] != None):
                            messageKeys[keys[i]] =  round(messageKeys[keys[i]],2)
                            messageToUser += profileMsgs[i]+": "+ str(messageKeys[keys[i]])+"\n" 

                    print(messageToUser)
                    if (messageToUser == INITIAL_MSG):
                        messageToUser = "Não encontramos esse perfil, verifique se você escreveu corretamente ou se esse usuário existe"
                    bot.reply_to(message, messageToUser)
                    time.sleep(10)
        # except:
        #       print("Wrong message format!")
    @bot.message_handler(func=allowMessages)
    def result(message):

        text = """
        Opção disponível : 
        /analise (Nome_Perfil1) (Nome_Perfil2)...
        """

        print("\n\n")
        bot.reply_to(message, text)
    


    bot.polling()