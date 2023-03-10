import os

from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context
from random import random, randrange
from asyncio import sleep
from carl_modules.user import User as CarlUser
from carl_modules.csv_handler import CSV as CarlCSV
intents = Intents.default()
intents.message_content = True

WORKDIR = os.path.abspath("./")

token_file = "discord.token"
items_csv = CSVFile(f"{WORKDIR}/data/items.csv",["item_id","name","booster"])
game_csv = CSVFile(f"{WORKDIR}/data/game.csv",["game_id","wins","losses","score",])
inventory_csv = CSVFile(f"{WORKDIR}/data/inventory.csv",["inventory_id","item","amount"])
config_file = JsonParser(f"{WORKDIR}/config.json")
CSV_HEADINGS = {"user":["discord_id","sus_amount","game_id","inventory_id"],"item":["item_id","name","booster"],"game":["game_id","wins","losses","score"],"inventory":["inventory_id","item","amount"]}
users_csv = CarlCSV(f"{WORKDIR}/data/users.csv",headings=CSV_HEADINGS["user"])

app = commands.Bot(intents=intents,command_prefix="$")
is_bot_running = False

@app.command()
async def sus(ctx : Context) -> None:
    user = CarlUser()
    discord_id = str(ctx.author)
    user_record = users_csv.search_entry("discord_id",discord_id)
    if(user_record != []):
        user.set_values_from_row(user_record[0])
        users_csv.remove_duplicates("discord_id",discord_id)
    else:
        user.create_user(discord_id=discord_id)
    user.sus_amount = int(user.sus_amount) + 1
    users_csv.append_record([user.export_row()])
    await ctx.send("imposter ඞ\n{user}: {amount}".format(user=discord_id,amount=user.sus_amount))

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