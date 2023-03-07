import os
from json import load,dump
from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context
from random import random, randrange
from pathlib import Path
intents = Intents.default()
intents.message_content = True

WORKDIR = os.path.abspath("./")
app = commands.Bot(intents=intents,command_prefix="=>")

def get_token(config_file : str) -> str:
    json_file = open(config_file,mode="r")

class JsonParser():
    _file_path = ""
    def __init__(self, path: str) -> None:
        self._file_path = path
    def read_content(self) -> dict:
        content_file = open(file=self._file_path, mode="r")
        data = load(content_file)
        content_file.close()
        return data
    def write_content(self, data: dict) -> None:
        content_file = open(file=self._file_path, mode="w")
        dump(data, content_file)
        content_file.close()

    def _does_path_exist(self,path : str) -> bool:
        return os.path.exists(path)
    
    def _create_json(self) -> None:
        json_file=open(self._file_path,mode="w")
        json_file.write("{}")



data_file = JsonParser(f"{WORKDIR}/data.json")
config_file = JsonParser(f"{WORKDIR}/config.json")
@app.command()
async def sus(ctx : Context) -> None:
    user = str(ctx.author)
    if(not is_json_valid(CONTENT_FILE) or not does_user_exist(user)):
        write_content(CONTENT_FILE,{user:{"num_sus":1}})
        content = read_content(CONTENT_FILE)
    else:
        content = read_content(CONTENT_FILE)
        content[user]["num_sus"] = content[user]["num_sus"] + 1
        write_content(CONTENT_FILE, content)
    await ctx.send("imposter ඞ\n{user}: {amount}".format(user=user,amount=content[user]["num_sus"]))

def does_user_exist(user : str):
    if(user in read_content(CONTENT_FILE).keys()):
        print(read_content(CONTENT_FILE).keys())
        return True
    return False

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

if __name__ == "__main__":
    if(not is_json_valid(CONTENT_FILE)):
        write_content(CONTENT_FILE,{})
    if(not is_json_valid(CONFIG_FILE)):
        write_content(CONFIG_FILE,{})
    
    token = get_token(CONFIG_FILE)
    app.run(token)