from pyrogram import Client, filters
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# Initialize Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['telegram_bot']
users_collection = db['users']

@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Store user in database
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id, "user_name": user_name})

    message.reply_text("Hello! I am your bot and I am running 24x7 🚀")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
