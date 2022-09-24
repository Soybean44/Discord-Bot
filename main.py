"""
TITLE: King Nerd Bot Main File
AUTHOR: SOVEREIGN SHAHID
DATE: 2022-09-24
"""
from discord import Option, Bot, ApplicationContext
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[1019797564620554342], description="Repeats What you say",)
async def echo(
    ctx: ApplicationContext,
    phrase: Option(str, "Enter Phrase")
):
    await ctx.respond(f"{phrase}")



bot.run(os.getenv("BOT_TOKEN"))
