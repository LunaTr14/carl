from os.path import abspath
from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context
from discord import User
from random import random, randrange
from carl_modules.user import User as CarlUser
from carl_modules.csv_handler import CSV as CarlCSV
from carl_modules.inventory import Inventory as CarlInventory
from carl_modules.game import Game as CarlGame
from carl_modules.item import Item as CarlItem

WORKDIR = abspath("./")

CSV_HEADINGS = {"user":["discord_id","sus_amount","game_id","inventory_id"],
                "item":["item_id","name","boost"],
                "game":["game_id","wins","losses","score"],
                "inventory":["inventory_id","item","amount"]}

token_file = f"{WORKDIR}/discord.token"
item_csv = CarlCSV(file_name=f"{WORKDIR}/data/item.csv",headings=CSV_HEADINGS["item"])
users_csv = CarlCSV(f"{WORKDIR}/data/users.csv",headings=CSV_HEADINGS["user"])
game_csv = CarlCSV(f"{WORKDIR}/data/game.csv",headings=CSV_HEADINGS["game"])
inventory_csv = CarlCSV(f"{WORKDIR}/data/inventory.csv",headings=CSV_HEADINGS["inventory"])
intents = Intents.default()
intents.message_content = True
app = commands.Bot(intents=intents,command_prefix="$")

@app.command(name="sus")
async def sus(ctx : Context) -> None:
    user = CarlUser()
    discord_id = str(ctx.author)
    if(users_csv.does_entry_exist("discord_id",discord_id)):
        user.set_values_from_row(users_csv.get_entry("discord_id",discord_id))
        users_csv.remove_duplicates("discord_id",discord_id)
    else:
        user.create(discord_id)
    user.set_sus(user.get_sus() +  1)
    users_csv.append_record([user.export_row()])
    await ctx.send("imposter ඞ\n{user}: {amount}".format(user=discord_id,amount=user.get_sus()))

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

def create_carl_user() -> CarlUser:
    user = CarlUser()
    user.create_if_empty(users_csv,"discord_id")
    return user
def get_fight_results(sender_boost: int,recipient_boost: int) -> str:
    total = sender_boost + recipient_boost
    if((sender_boost / total) > random()):
        return "sender"
    return "recipient"

@app.command(name="fight")
async def fight(ctx : Context, recipient : User)  -> None:
    author_user = CarlUser(users_csv,str(ctx.author))
    recipient_user = CarlUser(users_csv,str(recipient))
    author_inventory = CarlInventory(author_user.get_inventory_id())
    recipient_inventory = CarlInventory(recipient_user.get_inventory_id())
    author_game = CarlGame(game_csv,author_user.get_game_id())
    recipient_game = CarlGame(game_csv,recipient_user.get_game_id())
    author_boost = author_inventory.get_total_boost(item_csv)
    recipient_boost = recipient_inventory.get_total_boost(item_csv)
    results = get_fight_results(author_boost,recipient_boost)
    winner = ""
    winner_score =""
    loser = ""
    loser_score =""
    if(results == "sender"):
        author_game.update_score(True,recipient_game.get_score())
        author_game.incriment_win()
        recipient_game.incriment_loss()
        winner = author_user.get_discord_id()
        loser = recipient_user.get_discord_id()
        winner_score = author_game.get_score()
        loser_score = recipient_game.get_score()
    else:
        recipient_game.update_score(True,author_game.get_score())
        recipient_game.incriment_win()
        author_game.incriment_loss()
        loser = author_user.get_discord_id()
        winner = recipient_user.get_discord_id()
        loser_score = author_game.get_score()
        winner_score = recipient_game.get_score()
    author_user.save_user(users_csv)
    recipient_user.save_user(users_csv)
    author_game.save_game(game_csv)
    recipient_game.save_game(game_csv)
    await ctx.send(f"{winner} has won, score: {winner_score}\n{loser} score: {loser_score}")

def get_token() -> str:
    token = open(f"{WORKDIR}/discord.token",mode="r").readline()
    return token

@app.event
async def on_ready():
    print("Bot is Running")

if __name__ == "__main__":
    token = get_token()
    app.run(token)