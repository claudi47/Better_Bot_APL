from discord.ext import commands
from discord.ext.commands import Context
from web_sites_scripts import goldbet, bwin

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Annotation to specify the decorator (Decorator Pattern)
    # The function command() contains another function called decorator(func) and returns it
    @commands.command()
    # This is the function passed by param to the decorator -> decorator(func)
    async def call_scratch(self, context:Context, msg:str, category:str):
        if msg == 'goldbet':
            # The variable result is our generator. This generator contains string elements that will be showed
            # in the chat
            result = goldbet.run(category)
        else:
            result = bwin.run(category)

        for element in result:
            # await is a command similar to return but for async functions
            # await is necessary when a context switch happens (for example when two command are invoked simultaneously)
            # the funct stops and resumes his work after the other event finishes
            await context.send(element)
