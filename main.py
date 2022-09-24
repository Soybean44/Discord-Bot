"""
TITLE: King Nerd Bot Main File
AUTHOR: SOVEREIGN SHAHID
DATE: 2022-09-24
"""
from discord import Option, Bot, ApplicationContext, Intents
from dotenv import load_dotenv
import random
import json
import os

load_dotenv()

with open("yo_mama_jokes.json") as f:
    jokes = json.load(f)

intents = Intents.default()
intents.message_content = True

bot = Bot(intents=intents)
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.listen()
async def on_message(message):
    global jokes
    if message.author == bot.user:
        return
    if "mom" in message.content.lower():
        await message.channel.send(jokes[random.randint(0,len(jokes)-1)])




@bot.slash_command(guild_ids=[1019797564620554342], description="Repeats What you say",)
async def echo(
    ctx: ApplicationContext,
    phrase: Option(str, "Enter Phrase")
):
    await ctx.respond(f"{phrase}")



bot.run(os.getenv("BOT_TOKEN"))
