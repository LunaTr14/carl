import os

from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context
from random import random, randrange
from asyncio import sleep
from data_handler import JsonParser, CSVFile
intents = Intents.default()
intents.message_content = True

WORKDIR = os.path.abspath("./")

token_file = "discord.token"
config_file = JsonParser(f"{WORKDIR}/config.json")

app = commands.Bot(intents=intents,command_prefix="$")
is_bot_running = False

@app.command()
async def sus(ctx : Context) -> None:
    user = str(ctx.author)
    file_content = data_file.read_content()
    number_of_sus = 1
    if(user in file_content.keys()):
        number_of_sus = file_content[user]["num_sus"] + 1
    file_content[user] = {"num_sus":number_of_sus}
    data_file.write_content(file_content)
    await ctx.send("imposter ඞ\n{user}: {amount}".format(user=user,amount=file_content[user]["num_sus"]))

@app.command()
async def rng(ctx : Context) -> None:
    rand_number = str(random())
    await ctx.send(rand_number)

@app.command(name="flip-coin")
async def flip_coin(ctx : Context) -> None:
    rand = randrange(0,2)
    if(rand == 1):
        await ctx.send("HEADS")
    elif (rand == 0):
        await ctx.send("TAILS")

def get_token() -> str:
    token = open(f"{WORKDIR}/discord.token",mode="r").readline()
    return token

async def send_croissant(channel_id : int) -> None:
    await app.get_channel(channel_id).send("Are you gonna finish that __*CROISSANT*__")

@app.event
async def on_ready():
    print("Bot is Running")
    is_bot_running = True
    channel_id = config_file.read_content()["croissant_channel"]
    while(is_bot_running):
        await send_croissant(channel_id)
        time_delay = randrange(start=21600,stop=86400)
        await sleep(time_delay)

if __name__ == "__main__":
    token = get_token()
    app.run(token)