## Project2_FoodRecommendationBot

# To crete virtual env
python -m venv venv
./venv/Scripts/activate

# To install rasa and discord.py
pip install -r requirements.txt

# To train model
rasa train

# To run server
python DiscordBot.py
