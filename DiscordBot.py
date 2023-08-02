import discord
import os
from rasa.core.agent import Agent
from rasa.core.trackers import DialogueStateTracker
from rasa.shared.core.events import UserUttered, ActionExecuted

MODEL_NAME = "20230720-224118-pizzicato-weight.tar.gz"
TOKEN = "MTExNzMzMjY0Njc1ODk5Mzk1MA.GelRN8.p__bc9wFNSUtVOJKR6yaIf39ZfwAbUyMCHaafw"

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

    # Create a conversation tracker
    tracker = DialogueStateTracker.from_events(sender_id=message.author.id, evts=[UserUttered(user_message)])

    # Get the Rasa agent's response using the conversation tracker
    rasa_response = await agent.handle_text(user_message, tracker)

    print(rasa_response)
    # Extract the text from the Rasa response
    response_text = rasa_response[0]["text"]
    await message.channel.send(response_text)

client.run(TOKEN)