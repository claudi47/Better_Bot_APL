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
    async def goldbet(self, context:Context, category:str):
        # The variable result is our generator. This generator contains string elements that will be showed
        # in the chat
        result = '\n'.join(goldbet.run(category))

        # await is a command similar to return but for async functions
        # await is necessary when a context switch happens (for example when two command are invoked simultaneously)
        # the funct stops and resumes his work after the other event finishes
        await context.send(result)

    @commands.command(brief='Shows the quotes of the principal soccer matches inside Bwin website',
                      description='This command shows the most important quotes about all the soccer matches inside bwin'
                                  ' website. The quotes are 1x2 and Over/Under')
    async def bwin(self, ctx:Context, category:str):
        result = '\n'.join(bwin.run(category))
        await ctx.send(result)