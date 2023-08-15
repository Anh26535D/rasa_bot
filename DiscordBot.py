import discord
import os
from rasa.core.agent import Agent

MODEL_NAME = "20230720-224118-pizzicato-weight.tar.gz"

with open("secret.txt", "r") as f:
    TOKEN = f.readlines()

cur_path = os.getcwd()

model_path = os.path.join(cur_path, "models", MODEL_NAME)
agent = Agent()
agent.load_model(model_path=model_path)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Get the user's message
    user_message = message.content

    rasa_response = agent.handel

    print(rasa_response)
    # Extract the text from the Rasa response
    response_text = rasa_response[0]["text"]
    await message.channel.send(response_text)

client.run(TOKEN)