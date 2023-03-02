import os
from json import load
from discord import Intents
from discord.ext import commands
import random
intents = Intents.default()
intents.message_content = True

app = commands.Bot(intents=intents,command_prefix="=>")

TOKEN_FILE = os.path.abspath("./config.json")

def get_token(config_file : str) -> str:
    json_file = open(config_file,mode="r")
    token = load(json_file)["token"]
    json_file.close()
    return token
    
@app.command()
async def sus(ctx):
    await ctx.send("imposter ඞ")

@app.command()
async def rng(ctx):
    rand_number = str(random.random())
    await ctx.send(rand_number)

if __name__ == "__main__":
    token = get_token(TOKEN_FILE)
    app.run(token)