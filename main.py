from os.path import abspath
import interactions
from interactions import Client, SlashCommand, slash_command, SlashContext
import random
from carl_modules.csv_handler import CSV as CarlCSV
from time import time_ns
WORKDIR = abspath("./")

CSV_HEADINGS = ["discord_id","sus_amount","score","win_chance","win","loss"]

DEFAULT_SCORE = 1000
DEFAULT_BOOST = 100

token_file = f"{WORKDIR}/discord.token"
user_csv = CarlCSV(file_name="user.csv",file_path=WORKDIR)

def get_token() -> str:
    token = open(f"{WORKDIR}/discord.token",mode="r").read()
    return token

app = interactions.Client()

def generate_id() -> str:
    return str(randrange(99999,999999) * time_ns())[0:6]


@slash_command(name="sus",description="IMPOSTER SUS?!??!?!")
async def sus(ctx : SlashContext) -> None:
    sus_amount = 0
    displayname = ctx.author.username
    discord_id = str(ctx.author.id)
    search_value = user_csv.search(discord_id)
    if(len(search_value) <= 0):
        search_value = [[discord_id,"0","0","100","0","0"]]
    sus_amount = int(search_value[0][1])
    sus_amount += 1
    search_value[0][1] = str(sus_amount)
    user_csv.remove_entries_by_id(discord_id)
    user_csv.append(search_value)
    await ctx.send("imposter ඞ\n{user}: {amount}".format(user=displayname,amount=sus_amount))

@slash_command(name="rng",description="Generates a random number from 0 to 1")
async def rng(ctx : SlashContext) -> None:
    seed = str(ctx.author.id) + str(ctx.author.nickname)
    rand = random
    rand.seed = seed
    await ctx.send(str(rand.random()))

@slash_command(name="flip-coin",description="Flips a Coin")
async def flip_coin(ctx : SlashContext,*args) -> None:
    seed = str(ctx.author.id) + str(ctx.author.nickname)
    rand = random
    rand.seed = seed
    rand_int = int(rand.randrange(0,2))
    if(rand_int == 1):
        await ctx.send("HEADS")
    elif (rand_int == 0):
        await ctx.send("TAILS")

"""
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
"""
@interactions.listen()
async def on_ready():
    print("Bot is Running")

if __name__ == "__main__":
    app.start(get_token())