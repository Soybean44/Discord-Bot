"""
TITLE: Bot Main File
AUTHOR: SOVEREIGN SHAHID
DATE: 2022-09-24
"""
import datetime
import json
import os
import random

import discord
from discord import ApplicationContext, Bot, Embed, Intents, Option
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from db import getConfession, uploadConfession

load_dotenv()

# --- VARIABLES --- #

with open("yo_mama_jokes.json") as f:
    jokes = json.load(f)

with open("pickup_lines.json") as f:
    pickup_lines = json.load(f)

intents = Intents.default()
intents.message_content = True

bot = Bot(intents=intents)

mommy_enable = True
mommy_count = 0
mommy_max = 3

mod_id = 1193718992423108781


# --- BOT STUFF --- #


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.listen()
async def on_message(message):
    global jokes, mommy_count, mommy_max
    if message.author == bot.user:
        return
    mom_words = ["mom", "mum", "ma ", "mama", "mother", "mommy"]

    words = message.content.lower().split()
    if mommy_enable:
        for mom in mom_words:
            if any(word == mom for word in words):
                if mommy_count == 0:
                    await message.channel.send(jokes[random.randrange(len(jokes))])
                else:
                    pass
                mommy_count += 1

        if mommy_count >= mommy_max:
            mommy_count = 0


@bot.slash_command(description="Repeats What you say")
async def echo(ctx: ApplicationContext, phrase: Option(str, "Enter Phrase")):
    await ctx.respond(f"{phrase}")


@bot.slash_command(
    description="Anonymous Confessions",
)
async def confess(ctx: ApplicationContext, confession: Option(str, "Enter Confession")):
    global bot
    timestamp = datetime.datetime.now()
    obj = uploadConfession(confession, timestamp, ctx.user.name)
    confession_embed = Embed(
        title=f"Confession (#{obj.id})", description=obj.confession
    )
    confession_channel = bot.get_channel(1193718433578225685)
    await confession_channel.send(embed=confession_embed)
    await ctx.send_response(content="Confession was sent sucessfully", ephemeral=True)


@bot.slash_command(description="View Confession Log (Mods only)")
async def get_confession(ctx: ApplicationContext, id: Option(int, "Enter Confession")):
    global bot
    if ctx.guild.get_role(mod_id) <= ctx.user.roles[-1]:
        obj = getConfession(id)
        if obj is None:
            await ctx.send_response(content=f"confession #{id} does not exist")
        else:
            log_embed = Embed(
                title=f"Confession log (#{obj.id})",
                description=f"{obj.user} sent the following confession",
            )
            log_embed.add_field(name="Timestamp", value=obj.timestamp)
            log_embed.add_field(name="Confession", value=obj.confession)
            await ctx.send_response(embed=log_embed)
    else:
        await ctx.send_response(content="nuh uh uh", ephemeral=True)


@bot.slash_command(description="Generates pickup lines for you so you can get bitches")
async def pickup_line_generator(
    ctx: ApplicationContext,
    ping: Option(discord.User, "Ping the person of your dreams", required=False),
):
    global pickup_lines

    if not ping:
        res = f"{pickup_lines[random.randrange(len(pickup_lines))]}"
    else:
        res = f"{ping.mention}: {pickup_lines[random.randrange(len(pickup_lines))]}"
    await ctx.send_response(res)


@bot.slash_command(
    description="Command for yo mama jokes so you dont have to spam mommy every time"
)
async def yo_mama_generator(ctx: ApplicationContext):
    global jokes

    res = f"{jokes[random.randrange(len(jokes))]}"
    await ctx.send_response(res)


@bot.slash_command(
    description="For mods to disable yo mama jokes if the time isnt apropriate"
)
async def yo_mama_enable(ctx: ApplicationContext):
    global mommy_enable

    if ctx.guild.get_role(mod_id) <= ctx.user.roles[-1]:
        if mommy_enable:
            mommy_enable = False
        else:
            mommy_enable = True
        res = f"{mommy_enable}: is what the jokes are set to"
    else:
        res = "You aren't allowed to do that"
    await ctx.send_response(content=res, ephemeral=True)


@bot.slash_command(description="use this to get verified")
async def verify(
    ctx: ApplicationContext,
):
    general_channel = bot.get_channel(1193715211148996648)
    member = ctx.guild.get_member_named(ctx.user.name)
    verification_role = ctx.guild.get_role(1193716184613408768)
    if verification_role in ctx.user.roles:
        res = "You are already verified"
    else:
        create_date = ctx.user.created_at
        join_date = ctx.user.joined_at
        if create_date and (create_date + datetime.timedelta(days=14)) < join_date:
            verification_role = ctx.guild.get_role(1193716184613408768)
            await member.add_roles(verification_role)
            res = f"{ctx.user.name} has sucessfully been verified"
            await general_channel.send(
                content=f"Welcome {ctx.user.mention} go get roles in the designated channels"
            )
        else:
            res = f"{ctx.user.mention}'s account is too young to enter"
    await ctx.send_response(content=res)


bot.run(os.getenv("BOT_TOKEN"))
