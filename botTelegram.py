import jsonpickle
import telebot
import requests
from config import TELEGRAM_API_KEY
import json

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
def getSecondWord(text):
    textArray = text.split(' ')
    if(len(textArray) != 2):
        raise Exception("Message in wrong format")

    return textArray[1]

if __name__ == "__main__":
    bot = telebot.TeleBot(TELEGRAM_API_KEY)
    URL = "https://pegabot.com.br/botometer?"
    
    @bot.message_handler(commands=["analise"])
    def analysis(message):
        try:
            formattedMessage = jsonpickle.encode(message)
            formattedMessage  = json.loads(formattedMessage)
            itemToSearch = getSecondWord(formattedMessage["text"])
            # URL = "https://pegabot.com.br/botometer?profile=twitter&search_for=profile&is_admin=true"
            if itemToSearch != "":
                print(itemToSearch)
                PARAMS = {"profile":itemToSearch.strip(), "search_for":"profile", "is_admin":"true"}
                print("\n\n\n")
                r = requests.get(url = URL, params =PARAMS)
                data = r.json()
                messageKeys = getMessageInfos(data)
                print(messageKeys)
                bot.reply_to(message, "Analisando")
        except:
             print("Wrong message format!")
    @bot.message_handler(func=allowMessages)
    def result(message):

        text = """
        Opção disponível: 
        /analise (Nome_Perfil)
        """

        print("\n\n")
        bot.reply_to(message, text)
    


    bot.polling()