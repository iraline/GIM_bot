import jsonpickle
import telebot
import requests
from config import TELEGRAM_API_KEY
import json
import time

def getMessageInfos(data):
    messageKeys =  {"completeAnalysis": None, "profileUser": None, "network": None, "language": None, "username": ""}
    
    if("profiles" in data):
        if("bot_probability" in data["profiles"][0] and "all" in data["profiles"][0]["bot_probability"]):
            messageKeys["completeAnalysis"] = data["profiles"][0]["bot_probability"]["all"]
            
        if("language_independent" in data["profiles"][0]):

            if("user" in data["profiles"][0]["language_independent"]):
                messageKeys["profileUser"] = data["profiles"][0]["language_independent"]["user"]

            if("network" in data["profiles"][0]["language_independent"]):
                messageKeys["network"] = data["profiles"][0]["language_independent"]["network"]

        if("sentiment" in data["profiles"][0]["language_dependent"] and "value" in data["profiles"][0]["language_dependent"]["sentiment"]):
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
            formattedMessage = jsonpickle.encode(message)
            formattedMessage  = json.loads(formattedMessage)
            itemsToSearch = getWords(formattedMessage["text"])
            # URL = "https://pegabot.com.br/botometer?profile=twitter&search_for=profile&is_admin=true"
            
            if itemsToSearch != [""]:
                print("Profiles to search")
                print(itemsToSearch)
                for iProfile in range(len(itemsToSearch)):
                    print(itemsToSearch[iProfile])
                    PARAMS = {"profile":itemsToSearch[iProfile].strip(), "search_for":"profile", "is_admin":"true"}
                
                    request = requests.get(url = URL, params =PARAMS)
                    data = request.json()
                    messageKeys = getMessageInfos(data)
               
                    INITIAL_MSG = "Probabilidade de " + itemsToSearch[iProfile].strip() + " ser um robô: \n\n"
                    messageToUser = INITIAL_MSG

                    keys= ["completeAnalysis", "profileUser", "network", "language"]
                    profileMsgs = ["Análise completa", "Perfil do usuário", "Rede (seguidores e seguidos)", "Linguagem utilizada nos tweets"]

                    for iKey in range(len(keys)):
                        if (messageKeys[keys[iKey]] != None):
                            messageKeys[keys[iKey]] =  round(messageKeys[keys[iKey]],2)
                            messageToUser += profileMsgs[iKey]+": "+ str(messageKeys[keys[iKey]])+"\n" 

                    
                    if (messageToUser == INITIAL_MSG):
                        messageToUser = "Não encontramos o perfil "+ itemsToSearch[iProfile].strip() + ", verifique se você escreveu corretamente ou se esse usuário existe"
                    
                    print(messageToUser)
                    bot.reply_to(message, messageToUser)
                    time.sleep(10)
   
    @bot.message_handler(commands=["site_pegabot"])
    def result(message):
        text = "https://pegabot.com.br"
    
        bot.send_message(message.chat.id,text)
        print("Site sent")

    @bot.message_handler(commands=["como_usar"])
    def result(message):
        text = """
        Para verificar se determinado perfil é um bot, basta inserir o comando /analise "perfil". 
        Exemplo: Caso queira saber se fulano é um bot, basta inserir "/analise fulano". 
        Caso queira saber se fulano e sicrano são um bot, basta inserir "/analise fulano sicrano"
        """
    
        bot.send_message(message.chat.id,text)
        print("Help sent")

    @bot.message_handler(func=allowMessages)
    def result(message):

        text = """
        Opções disponíveis: 
            /analise (Perfil1) (Perfil2)...
            /site_pegabot Site do pegabot
            /como_usar Como utilizar o bot
        """
        
        bot.send_message(message.chat.id,text)
        print("Options sent")

    bot.polling()