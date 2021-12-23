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

async def _validation(ctx:Context, website):
    can_execute = requests.get(f'http://localhost:8000/validation/?user_id={ctx.author.id}&website={website}')
    if not can_execute.ok:
        return False, "Validation error!"
    validation_data = can_execute.text
    if validation_data == 'banned':
        return False, "You got banned"
    elif validation_data == 'reached_max':
        return False, "You cannot do another research"
    elif validation_data == 'disabled':
        return False, "This website is temporarily disabled by the Admin"

    return True,


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
        is_valid, description = _validation(ctx, 'goldbet')
        if not is_valid:
            return await ctx.send(description)
        bet_data = goldbet.run(category)
        print(bet_data.to_json())
        search_data = _get_search_data(ctx, bet_data)
        # sending json object to web server through POST method
        response_csv_filename = requests.post('http://localhost:8000/bot/goldbet/', json=search_data.data)
        if not response_csv_filename.ok:
            await ctx.send("Error during the parsing of the file")
            print("Che è successo? Non è arrivato bene il file csv. LOL!")
        else:
            response_data = response_csv_filename.json()
            csv_file_path = os.path.abspath(r'C:\Users\claud\Desktop\Advanced Programming Languages\Computing_Parsing_APL\Computing_Parsing_Module\Computing_Parsing_Module\\'
                                            + response_data['filename'])
            with open(csv_file_path, "rb") as file: # opening in read-binary mode
                # instance of discord File class that wants the filepointer and his new name (optional)
                discord_file = discord.File(file, f"goldbet_search_{ctx.author.name}_{category}.csv")
                message = await ctx.send(f"Here's your research, {ctx.author.name}. Bet safely...", file=discord_file)
            # taking the url of the uploaded file on discord, saved into the CDN (Content Delivery Network)
            url_csv = message.attachments[0].url
            patching_associated_search_data = {'url_csv': url_csv, 'search_id': response_data['search_id']}
            patching_url_csv = requests.post('http://localhost:8000/bot/csv/', data=patching_associated_search_data)
            if not patching_url_csv.ok:
                await message.delete()
            

    @commands.command(brief='Shows the quotes of the principal soccer matches inside Bwin website',
                      description='This command shows the most important quotes about all the soccer matches inside bwin'
                                  ' website. The quotes are 1x2 and Over/Under')
    async def bwin(self, ctx:Context, category):
        is_valid, description = _validation(ctx, 'bwin')
        if not is_valid:
            return await ctx.send(description)
        bet_data = bwin.run(category)
        search_data = _get_search_data(ctx, bet_data)
        response_csv_filename = requests.post('http://localhost:8000/bot/bwin/', json=search_data.data)
        if not response_csv_filename.ok:
            await ctx.send("Error during the parsing of the file")
            print("Che è successo? Non è arrivato bene il file csv. LOL!")
        else:
            response_data = response_csv_filename.json()
            csv_file_path = os.path.abspath(r'C:\Users\claud\Desktop\Advanced Programming Languages\Web_Server_APL\\'
                                            + response_data['filename'])
            with open(csv_file_path, "rb") as file: # opening in read-binary mode
                # instance of discord File class that wants the filepointer and his new name (optional)
                discord_file = discord.File(file, f"bwin_search_{ctx.author.name}_{category}.csv")
                message = await ctx.send(f"Here's your research, {ctx.author.name}. Bet safely...", file=discord_file)
            # taking the url of the uploaded file on discord, saved into the CDN (Content Delivery Network)
            url_csv = message.attachments[0].url
            patching_associated_search_data = {'url_csv': url_csv, 'search_id': response_data['search_id']}
            patching_url_csv = requests.post('http://localhost:8000/bot/csv/', data=patching_associated_search_data)
            if not patching_url_csv.ok:
                await message.delete()

        # await is a command similar to return but for async functions
        # await is necessary when a context switch happens (for example when two command are invoked simultaneously)
        # the funct stops and resumes his work after the other event finishes
