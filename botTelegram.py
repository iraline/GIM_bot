import telebot
import requests
from config import TELEGRAM_API_KEY

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



if __name__ == "__main__":
    bot = telebot.TeleBot(TELEGRAM_API_KEY)

    @bot.message_handler(func=allowMessages)
    def result(message):
        r = requests.get(url = URL)
        data = r.json()
        print("\n\n")
        
        messageKeys = getMessageInfos(data)
        
        print(messageKeys)
        print("\n\n")
        bot.reply_to(message, "Aqui é o GIM Bot")
    
    # print(message)

    

    URL = "https://pegabot.com.br/botometer?profile=twitter&search_for=profile&is_admin=true"
    r = requests.get(url = URL)
    data = r.json()
    bot.polling()