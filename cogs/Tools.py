import discord
import random
import time
from discord.ext import commands

class Tools(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def say(self, ctx, *, message):
    if len(message) > 285:
      await ctx.send("Cannot type message's over 280 charcters long")
      return
    else:
      embed = discord.Embed(title=f"Message by {ctx.author.name}:", color=discord.Color(random.randint(1, 16777215)))
      embed.add_field(name="Message:", value=f"{message}")
      await ctx.send(embed=embed)

  @say.error
  async def say_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("What do you want me to say?")

  @commands.command()
  async def dice(self, ctx):
    dice_response = random.randint(1,6)
    dice_message = await ctx.send("Rolling the dice.....")
    time.sleep(4)
    await dice_message.edit(content=f"You rolled a {dice_response}")

  @commands.command()
  async def toss(self, ctx):
    toss_response = ['Heads','Tails']
    toss_message = await ctx.send("The coin is in the air....")
    time.sleep(3)
    rancoin = random.choice(toss_response)
    await toss_message.edit(content=f"The coin toss results is {rancoin}")

  @commands.command()
  async def invite(self, ctx):
    embed = discord.Embed(title="Invites", description="", colour = discord.Color(random.randint(1, 16777215)))
    embed.add_field(name="LeBot", value="[LeBot invite](https://discord.com/oauth2/authorize?client_id=716323508472381510&permissions=8&scope=bot)")
    await ctx.send(embed=embed)


def setup(bot):
  bot.add_cog(Tools(bot))