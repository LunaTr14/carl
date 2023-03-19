from os.path import abspath
import interactions
from random import random, randrange
from carl_modules.csv_handler import CSV as CarlCSV
from carl_modules.game import Game as CarlGame
from time import time_ns, time, sleep
from threading import Thread
WORKDIR = abspath("./")

CSV_HEADINGS = {"user":["discord_id","sus_amount","game_id"],
                "game":["game_id","score","boost"]}

DEFAULT_SCORE = 1000
DEFAULT_BOOST = 100

token_file = f"{WORKDIR}/discord.token"
game_csv = CarlCSV(f"{WORKDIR}/data/game.csv")
user_csv = CarlCSV(f"{WORKDIR}/data/user.csv")

def get_token() -> str:
    token = open(f"{WORKDIR}/discord.token",mode="r").read()
    return token

app = interactions.Client(get_token())

def generate_id() -> str:
    return str(randrange(99999,999999) * time_ns())[0:6]


@app.command(name="sus",description="IMPOSTER SUS?!??!?!")
async def sus(ctx : interactions.CommandContext) -> None:
    
    sender_id = str(ctx.author.id)
    displayname = ctx.author.user.username
    user_row = [sender_id,0,generate_id()]
    if(user_csv.does_entry_exist(sender_id)):
        user_row = user_csv.search(sender_id)[0]
    sus_amount = user_row[1]
    user_row[1] = str(int(user_row[1]) + 1)
    user_csv.save(user_row)
    await ctx.send("imposter ඞ\n{user}: {amount}".format(user=displayname,amount=sus_amount))

@app.command(name="rng",description="Generates a random number from 0 to 1")
async def rng(ctx : interactions.CommandContext) -> None:
    rand_number = str(random())
    await ctx.send(rand_number)

@app.command(name="flip-coin",description="Flips a Coin")
async def flip_coin(ctx : interactions.CommandContext,*args) -> None:
    rand = randrange(0,2)
    if(rand == 1):
        await ctx.send("HEADS")
    elif (rand == 0):
        await ctx.send("TAILS")

@app.command(name="fight",description="Fights tagged player",options=[
    interactions.Option(
    name="opponent",
    description="Opponent Player",
    type=interactions.OptionType.USER,
    required=True
)])
async def fight(ctx : interactions.CommandContext, opponent : interactions.User)  -> None:    
    sender_id = str(ctx.user.id)
    opponent_id = str(opponent.id)
    if(sender_id == opponent_id):
        await ctx.send("Sender and Opponent are the same User")
        return
    sender_username = ctx.user.username
    opponent_username = opponent.username
    if(not user_csv.does_entry_exist(sender_id)):
        game_id = generate_id()
        user_csv.save([sender_id,0,game_id])
        game_csv.save([game_id,DEFAULT_SCORE,DEFAULT_BOOST])
    if(not user_csv.does_entry_exist(opponent_id)):
        game_id = generate_id()
        user_csv.save([opponent_id,0,game_id])
        game_csv.save([game_id,DEFAULT_SCORE,DEFAULT_BOOST])
    
    user_game_id = user_csv.search(sender_id)[0][2]
    user_game_row = game_csv.search(user_game_id)[0]

    opponent_game_id = user_csv.search(opponent_id)[0][2]
    opponent_game_row = game_csv.search(opponent_game_id)[0]

    winner = CarlGame(game_csv).fight(user_game_row,opponent_game_row)
    winner_display_name = opponent_username
    if(winner[0] == user_game_id):
        winner_display_name = sender_username
    
    await ctx.send(f"Winner: {winner_display_name}\nScore: {winner[1]}")
    
@app.command(name="score",description="Gets tagged player's score",options=[
    interactions.Option(
    name="user",
    description="Tagged player",
    type=interactions.OptionType.USER,
    required=False
)])
async def get_score(ctx : interactions.CommandContext, user : interactions.User = None):
    sender_id = str(ctx.user.id)
    display_name = ctx.user.username
    if(user != None):
        sender_id = str(user.id)
        display_name = user.username
    
    if(not user_csv.does_entry_exist(sender_id)):
        await ctx.send("User Does not exist")
        return
    
    game_id = user_csv.search(sender_id)[0][2]
    score = game_csv.search(game_id)[0][1]
    await ctx.send(f'{display_name} Score: {score}')
@app.command(name="check_boost",description="Gets a player's boost",options=[
    interactions.Option(
    name="user",
    description="Tagged player",
    type=interactions.OptionType.USER,
    required=False
)])
async def get_chance(ctx: interactions.CommandContext, user : interactions.User = None):
    sender_id = str(ctx.author.id)
    display_name = ctx.user.username
    if(user != None):
        sender_id = str(user.id)
        display_name = user.username
    
    if(not user_csv.does_entry_exist(sender_id)):
        await ctx.send("User Does not exist")
        return
    game_id = user_csv.search(sender_id)[0][2]
    boost = game_csv.search(game_id)[0][2]
    await ctx.send(f"{display_name}' Boost: {boost}\nNext Boost Drop: {round(time_delay-time())}s")

@app.event
async def on_ready():    
    print("Bot is Running")
    global is_running
    is_running = True
    Thread(target=item_spawn).start()

def item_spawn():
    global time_delay
    time_delay = 0.0
    while(is_running):
        if(time_delay - time()<= 0 ):
            all_entries = game_csv.get_all()
            random_entry = all_entries[randrange(0,len(all_entries) - 1)]
            random_boost = randrange(10,100)
            random_entry[2] = str(int(random_entry[2]) + random_boost)
            game_csv.save(random_entry)
            time_delay = time() + randrange(1800,5400)
        sleep(100)

if __name__ == "__main__":
    app.start()