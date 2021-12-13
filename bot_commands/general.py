import discord
import requests
import os
from discord.ext import commands
from discord.ext.commands import Context
from web_sites_scripts import goldbet, bwin

from models.search_data import SearchData
from models.user_data import UserData
from models.betting_data import BettingData


# static functions are collocated outside the classes
def _get_search_data(ctx:Context, bet_data:BettingData):
    user_id = ctx.author.id
    username = ctx.author.name
    user_data = UserData(user_id, username)
    search_data = SearchData(bet_data, user_data)
    return search_data

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Annotation to specify the decorator (Decorator Pattern)
    # The function command() contains another function called decorator(func) and returns it
    # During run-time, the method goldbet (or bwin) is passed to the decorator, through the command function,
    # who instantiates a Command class into a variable with the same name of the function passed to it
    @commands.command(brief='Shows the quotes of the principal soccer matches inside GoldBet website',
                      description='This command shows the most important quotes about all the soccer matches inside'
                                  ' GoldBet website. The quotes are 1x2 and Under/Over')
    # This is the function passed by param to the decorator -> decorator(func)
    async def goldbet(self, ctx:Context, category):
        bet_data = goldbet.run(category)
        print(bet_data.to_json())
        search_data = _get_search_data(ctx, bet_data)
        # sending json object to web server through POST method
        response_csv_filename = requests.post('http://localhost:8000/bot/goldbet/', json=search_data.data)
        if not response_csv_filename.ok:
            await ctx.send("Error during the parsing of the file")
            print("Che è successo? Non è arrivato bene il file csv. LOL!")
        else:
            csv_file_path = os.path.abspath(r'C:\Users\claud\Desktop\Advanced Programming Languages\Web_Server_APL\\'
                                            + response_csv_filename.text)
            with open(csv_file_path, "rb") as file:
                discord_file = discord.File(file, f"goldbet_search_{ctx.author.name}_{category}")
                await ctx.send(f"Here's your research, {ctx.author.name}. Bet safely...", file=discord_file)
            

    @commands.command(brief='Shows the quotes of the principal soccer matches inside Bwin website',
                      description='This command shows the most important quotes about all the soccer matches inside bwin'
                                  ' website. The quotes are 1x2 and Over/Under')
    async def bwin(self, ctx:Context, category):
        bet_data = bwin.run(category)
        search_data = _get_search_data(ctx, bet_data)
        requests.post('http://localhost:8000/bot/bwin/', json=search_data.data)

        # await is a command similar to return but for async functions
        # await is necessary when a context switch happens (for example when two command are invoked simultaneously)
        # the funct stops and resumes his work after the other event finishes
