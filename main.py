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
class JsonParser():
    _file_path = ""
    def __init__(self, path: str) -> None:
        self._file_path = path
        if(not os.path.exists(path)):
            self.create_empty_json()
        
    def read_content(self) -> dict:
        content_file = open(file=self._file_path, mode="r")
        data = load(content_file)
        content_file.close()
        return data
    
    def create_empty_json(self) -> None:
        Path(self._file_path).touch()
        self.write_content({})
    
    def write_content(self, data: dict) -> None:
        content_file = open(file=self._file_path, mode="w")
        dump(data, content_file)
        content_file.close()

    def _does_path_exist(self,path : str) -> bool:
        return os.path.exists(path)

data_file = JsonParser(f"{WORKDIR}/data.json")
config_file = JsonParser(f"{WORKDIR}/config.json")
app = commands.Bot(intents=intents,command_prefix="$")

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
    token = config_file.read_content()["token"]
    return token
if __name__ == "__main__":
    token = get_token()
    app.run(token)