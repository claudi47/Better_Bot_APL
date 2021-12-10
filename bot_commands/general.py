import requests
from discord.ext import commands
from discord.ext.commands import Context
from web_sites_scripts import goldbet, bwin

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
    async def goldbet(self, ctx:Context, category:str):
        result = goldbet.run(category)
        print(result.to_json())
        # sending json object to web server through POST method
        requests.post('http://localhost:8000/bot/goldbet/', json=result.data)

    @commands.command(brief='Shows the quotes of the principal soccer matches inside Bwin website',
                      description='This command shows the most important quotes about all the soccer matches inside bwin'
                                  ' website. The quotes are 1x2 and Over/Under')
    async def bwin(self, ctx:Context, category:str):
        result = bwin.run(category)
        requests.post('http://localhost:8000/bot/bwin/', json=result.data)

    @commands.command()
    async def test_command(self, ctx:Context): # testing communication between bot and the server
        response = requests.get('http://localhost:8000/bot')

        # await is a command similar to return but for async functions
        # await is necessary when a context switch happens (for example when two command are invoked simultaneously)
        # the funct stops and resumes his work after the other event finishes
        await ctx.send(response.text)