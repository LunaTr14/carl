from os.path import abspath
from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context
from discord import User
from random import random, randrange
from carl_modules.csv_handler import CSV as CarlCSV
from carl_modules.game import Game as CarlGame
from time import time_ns
WORKDIR = abspath("./")

CSV_HEADINGS = {"user":["discord_id","sus_amount","game_id"],
                "game":["game_id","score","boost"]}

DEFAULT_SCORE = 1000
DEFAULT_BOOST = 100

token_file = f"{WORKDIR}/discord.token"

intents = Intents.default()
intents.message_content = True
app = commands.Bot(intents=intents,command_prefix="$")

game_csv = CarlCSV(f"{WORKDIR}/data/game.csv")
user_csv = CarlCSV(f"{WORKDIR}/data/user.csv")

def generate_id() -> str:
    return str(randrange(99999,999999) * time_ns())[0:6]

@app.command(name="sus")
async def sus(ctx : Context) -> None:
    
    user_id = str(ctx.author.id)
    user_row = [user_id,0,generate_id()]
    if(user_csv.does_entry_exist(user_id)):
        user_row = user_csv.search(user_id)[0]
    sus_amount = user_row[1]
    user_row[1] = str(int(user_row[1]) + 1)
    user_csv.save(user_row)
    await ctx.send("imposter ඞ\n{user}: {amount}".format(user=ctx.author.display_name,amount=sus_amount))

@app.command(name="rng")
async def rng(ctx : Context) -> None:
    rand_number = str(random())
    await ctx.send(rand_number)

@app.command(name="flip-coin")
async def flip_coin(ctx : Context,*args) -> None:
    rand = randrange(0,2)
    if(rand == 1):
        await ctx.send("HEADS")
    elif (rand == 0):
        await ctx.send("TAILS")

@app.command(name="fight")
async def fight(ctx : Context, opponent : User)  -> None:
    user_id = str(ctx.author.id)
    opponent_id = str(opponent.id)
    if(not user_csv.does_entry_exist(user_id)):
        game_id = generate_id()
        user_csv.save([user_id,0,game_id])
        game_csv.save([game_id,DEFAULT_SCORE,DEFAULT_BOOST])
    if(not user_csv.does_entry_exist(opponent_id)):
        game_id = generate_id()
        user_csv.save([opponent_id,0,game_id])
        game_csv.save([game_id,DEFAULT_SCORE,DEFAULT_BOOST])
    
    user_game_id = user_csv.search(user_id)[0][2]
    user_game_row = game_csv.search(user_game_id)[0]

    opponent_game_id = user_csv.search(opponent_id)[0][2]
    opponent_game_row = game_csv.search(opponent_game_id)[0]

    winner = CarlGame(game_csv).fight(user_game_row,opponent_game_row)
    if(winner == "OPPONENT"):
        await ctx.send(f"Winner is: {opponent.display_name}")
    else:
        await ctx.send(f"Winner is: {ctx.author.display_name}")

@app.command(name="score")
async def get_score(ctx : Context, user : User = None):
    user_id = str(ctx.author.id)
    display_name = ctx.author.display_name
    if(user != None):
        user_id = str(user.id)
        display_name = ctx.author.display_name
    
    if(not user_csv.does_entry_exist(user_id)):
        await ctx.send("User Does not exist")
        return
    
    game_id = user_csv.search(user_id)[0][2]
    score = game_csv.search(game_id)[0][1]
    await ctx.send(f'{display_name} Score: {score}')

def get_token() -> str:
    token = open(f"{WORKDIR}/discord.token",mode="r").read()
    return token

@app.event
async def on_ready():
    print("Bot is Running")

if __name__ == "__main__":
    token = get_token()
    app.run(token)