import discord
import random
from discord.ext import commands

class Help(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.group(invoke_without_command=True)
  async def help(self, ctx):
    embed = discord.Embed(title=f'LeBot commands', description="", colour=discord.Colour(random.randint(1, 16777215)))
    embed.add_field(name= ":gear:Moderation", value= (f"Type `help mod for more info"))
    embed.add_field(name= ":smile:Fun", value= (f"Type `help fun for more info"))
    embed.add_field(name=":tools:Tools", value= (f"Type `help tools for more info"))
    embed.add_field(name=":moneybag: Economy", value="Type `help economy for more info")
    await ctx.send(embed=embed)

  @help.command()
  async def fun(self, ctx):
    embed_2 = discord.Embed(title=f":smile:Fun commands", description='', colour=discord.Colour(random.randint(1, 16777215)))
    embed_2.add_field(name="\u200b", value="`8ball`,`dankrate`,`simprate`,`epicrate`,`waifurate`,`roast`,`nny`,`hack`, `meme`, `food`")
    await ctx.message.author.send(embed=embed_2)
    await ctx.send("Check your dm's homie")

  @help.command()
  async def mod(self, ctx):
    embed_3 = discord.Embed(title= f":hammer:Mod Commands", description="", colour=discord.Colour(random.randint(1, 16777215)))
    embed_3.add_field(name= "\u200b", value="`clear`,`kick`,`ban`,`unban`,`mute`,`unmute`,`rolecreate`,`roleadd`,`roleremove`,`roledelete`,`lock`,`unlock`")
    embed_3.set_footer("Role commands are case sensitive. Make sure to get the role name's right")
    embed_3.set_footer(text="Role commands are case sensitive. Make sure to get the role name's right")
    await ctx.message.author.send(embed=embed_3)
    await ctx.send("Check your dms's homie")
  
  @help.command()
  async def tools(self, ctx):
    embed_4 = discord.Embed(title = f':nut_and_bolt:Tools Commands', description="", colour=discord.Colour(random.randint(1, 16777215)))
    embed_4.add_field(name= "\u200b", value="`say`,`dice`,`toss`,`wiki`,`ping`,`avatar`,`stats`,`sinfo`,`userinfo`,`avatar`,`invite`")
    await ctx.message.author.send(embed=embed_4)
    await ctx.send("Chek your dm's homie")

  @help.command()
  async def economy(self, ctx):
    embed = discord.Embed(title=f":moneybag: Economy Commands", colour=discord.Colour.gold())
    embed.add_field(name="\u200b", value="`balance`,`withdraw`,`deposit`,`daily`,`beg`,`inventory`,`shop`,`buy`,`sell`,`slots`,`send`,`rob`,`heist`,`work`,`gamble`, `passive`")
    await ctx.message.author.send(embed=embed)
    await ctx.send("Check your dm's homie")

def setup(bot):
  bot.add_cog(Help(bot))