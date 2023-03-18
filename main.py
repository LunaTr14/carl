from os.path import abspath
from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context
from discord import User
from random import random, randrange
from carl_modules.user import User as CarlUser
from carl_modules.csv_handler import CSV as CarlCSV
from carl_modules.game import Game as CarlGame
WORKDIR = abspath("./")

CSV_HEADINGS = {"user":["discord_id","sus_amount","game_id"],
                "game":["game_id","score","boost"]}

token_file = f"{WORKDIR}/discord.token"

intents = Intents.default()
intents.message_content = True
app = commands.Bot(intents=intents,command_prefix="^")

game_csv = CarlCSV(f"{WORKDIR}/data/game.csv")
user_csv = CarlCSV(f"{WORKDIR}/data/user.csv")

@app.command(name="sus")
async def sus(ctx : Context) -> None:
    user = CarlUser(ctx.author)
    user.add_sus()
    await ctx.send("imposter ඞ\n{user}: {amount}".format(user=ctx.author,amount=user.get_sus()))

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
    
def get_fight_results(sender_boost: int,recipient_boost: int) -> str:
    total = sender_boost + recipient_boost
    if((sender_boost / total) > random()):
        return "sender"
    return "recipient"

@app.command(name="fight")
async def fight(ctx : Context, opponent : User)  -> None:
    sender_user = CarlUser(user_csv,game_csv,str(ctx.author.id))
    opponent_user = CarlUser(user_csv,game_csv,str(opponent.id))
    sender_game = CarlGame(game_csv,sender_user.get_game_id())
    winner = sender_game.fight(opponent_user.get_game_id())
    if(winner == "OPPONENT"):
        await ctx.send(f"Winner is: {opponent}")
    else:
        await ctx.send(f"Winner is: {ctx.author}")


def get_token() -> str:
    token = open(f"{WORKDIR}/discord.token",mode="r").read()
    return token

@app.event
async def on_ready():
    print("Bot is Running")

if __name__ == "__main__":
    token = get_token()
    app.run(token)