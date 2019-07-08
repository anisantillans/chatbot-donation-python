from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from textblob import TextBlob
import statistics

app = Flask(__name__)

bot = ChatBot("Chatterbot")
trainer = ListTrainer(bot)
data = open('data.txt','r').readlines()
trainer.train(data)

list = ['inicio']

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    msgEnglish = TextBlob(userText).translate(to="en")
    list.append(str(msgEnglish))
    return str(bot.get_response(userText))

@app.route("/getanalysis")
def get_analysis_response():
    polarity = []
    for listDePalabras in list:
        polarity.append(TextBlob(listDePalabras).sentiment.polarity)
    avg = statistics.mean(polarity)
    resp=''
    if avg  > 0:
        resp = str(avg) + " - Sentimiento muy positivo"                                       
    elif avg  == 0:
        resp = str(avg) + " - Sentimiento neutro"      
    else:                                  
        resp = str(avg) + " - Sentimiento muy negativo" 
        
    return resp

if __name__ == "__main__":
    app.run()
