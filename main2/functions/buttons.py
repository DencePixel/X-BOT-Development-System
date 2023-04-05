import discord
import random
from discord import Embed, app_commands
from discord.ext import commands
import discord.ext





class hint(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    
    #@commands.Cog.listener(name="on_command_completion")
    async def send_hint(self, ctx):
        descriptions = [
            "If you're enjoying AGB, please consider leaving a review on [Top.gg!](https://top.gg/bot/723726581864071178#reviews)",
            "If you're enjoying AGB and would like to contribute, feel free to leave a vote on [Top.gg!](https://top.gg/bot/723726581864071178/vote)",
            "Check out our [partner](https://connect.twisea.net)",
            "Boosters of the support server get lessened to zero cooldowns. Join by running </invite:969267005779755010>",
            "If you have suggestions don't hesitate to </suggest:966053481888772145> your ideas!",
                        ]
        HintEmbed = Embed(
            title="Did you know...?", description=random.choice(descriptions))
        await ctx.send(embed=HintEmbed)
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(hint(client))


