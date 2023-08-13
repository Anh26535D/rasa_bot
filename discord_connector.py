import discord
from discord.ext import commands

import requests

rasa_server_url = "http://localhost:5055/webhook"
discord_token = "YOUR_TOKEN"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)

def get_rasa_response(message):

    payload = {"sender": message.author.id, "message": message.content}

    response = requests.post(rasa_server_url, json=payload)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0].get("text")
    return None

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    bot_response = get_rasa_response(message)

    if bot_response:
        await message.channel.send(bot_response)

# Run the bot using the token
bot.run(discord_token)