import os
from json import load,dump
from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context
from random import random, randrange
intents = Intents.default()
intents.message_content = True

app = commands.Bot(intents=intents,command_prefix="=>")

CONFIG_FILE = os.path.abspath("./config.json")
CONTENT_FILE = os.path.abspath("./data.json")

def get_token(config_file : str) -> str:
    json_file = open(config_file,mode="r")
class TestJsonParser():
    __test_file = os.path.abspath("./test/test.json")
    __json_parser = None
    __template_json = {"test": {"read": "9649718a1cd61179343786855795b9c75269d97016f752f697e52e7d0d4141fa",
                                "write": ""}}
    __write_answer = "32539bab79202b64f4cfe9dff1288d77f8311ab8934ad9b963679750aca7d238"
    __read_answer = "9649718a1cd61179343786855795b9c75269d97016f752f697e52e7d0d4141fa"

    def __init__(self) -> None:
        self.__json_parser = JsonParser(self.__test_file)
        self.__reset_json()

    def __reset_json(self):
        json_file = open(self.__test_file, mode="w")
        dump(self.__template_json, json_file)
        json_file.close()

    def test_read(self):
        result = self.__json_parser.read_content()["test"]["read"]
        assert result == self.__read_answer, self.__print_err(
            self.__read_answer, result)

    def test_write(self):
        content = self.__json_parser.read_content()
        content["test"]["write"] = "32539bab79202b64f4cfe9dff1288d77f8311ab8934ad9b963679750aca7d238"
        self.__json_parser.write_content(content)
        result = self.__json_parser.read_content()["test"]["write"]
        assert result == self.__write_answer, self.__print_err(
            self.__write_answer, result)

    def __print_err(self, expected, result):
        return "\n>>Expected: {sample}\n>>Got: {result}".format(sample=expected, result=result)


class JsonParser():
    file_path = ""
    config_file = "./config.json"
    save_file = "./save.json"

    def __init__(self, path: str) -> None:
        self.file_path = path

    def read_content(self) -> dict:
        content_file = open(file=self.file_path, mode="r")
        data = load(content_file)
        content_file.close()
        return data

    def write_content(self, data: dict) -> None:
        content_file = open(file=self.file_path, mode="w")
        dump(data, content_file)
        content_file.close()

    def is_json_valid(file_path: str) -> bool:
        try:
            f = open(file_path, mode="r")
            load(f)
            f.close()
            return True
        except:
            return False
    token = load(json_file)["token"]
    json_file.close()
    return token

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