import discord
import random
from discord.ext import commands

class Help(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help(self, ctx):
    embed = discord.Embed(title=f'LeBot commands', description='', colour=discord.Colour(random.randint(1, 16777215)))
    embed.add_field(name= ":gear:Moderation", value= (f"`Type help_mod for more info`"))
    embed.add_field(name= ":smile:Fun", value= (f"`Type help_fun for more info`"))
    embed.add_field(name=":tools:Tools", value= (f"`Type help_tools for more info`"))
    await ctx.send(embed=embed)

  @commands.command()
  async def help_fun(self, ctx):
    embed_2 = discord.Embed(title=f"Fun commands", description='', colour=discord.Colour(random.randint(1, 16777215)))
    embed_2.add_field(name= "8ball", value="`Ask the 8ball a question`")
    embed_2.add_field(name= "dankrate", value= "`How dank are you?`")
    embed_2.add_field(name= "simprate", value="`How much of a simp are you?`")
    embed_2.add_field(name= "epicrate", value="`How epic are you?`")
    embed_2.add_field(name="waifurate", value="`How waifu are you`")
    embed_2.add_field(name= "roast", value="`As the name says dummy. It roast people`")
    embed_2.add_field(name= "nny", value="`(͡° ͜ʖ ͡°)`")
    embed_2.add_field(name= "hack", value="`Get Hacked`")
    await ctx.send(embed=embed_2)
    
  @commands.command()
  async def help_mod(self, ctx):
    embed_3 = discord.Embed(title= f" Mod Commands", description="", colour=discord.Colour(random.randint(1, 16777215)))
    embed_3.add_field(name= "clear", value="`Purges messages.`")
    embed_3.add_field(name= "kick", value="`Mentioned user gets the boot`")
    embed_3.add_field(name= "ban", value= "`Mentioned user gets the ban hammer`")
    embed_3.add_field(name="unban", value="`Member gets unbanned.`")
    embed_3.add_field(name="prefix", value='`Changes prefix of the bot (Default is "le.")`')
    embed_3.add_field(name="mute", value="`Mutes a user`")
    embed_3.add_field(name="unmute", value="`Unmutes a user`")
    embed_3.add_field(name="lock", value="`Locks the channel the command is used in.`")
    embed_3.add_field(name= "unlock", value="`Unlocks the channel the command is used in.`")
    await ctx.send(embed=embed_3)
  
  @commands.command()
  async def help_tools(self, ctx):
    embed_4 = discord.Embed(title = f'Tools Commands', description="", colour=discord.Colour(random.randint(1, 16777215)))
    embed_4.add_field(name= "say", value="`Says stuff`")
    embed_4.add_field(name="dice", value="`Rolls and imaginary dice`")
    embed_4.add_field(name="toss", value="`Settle legendary battles over a coin toss`")
    embed_4.add_field(name= "ping", value="`Shows the ping`")
    embed_4.add_field(name="stats", value="`Shows the stats of the bot`")
    embed_4.add_field(name="avatar", value="`Sends avatar URL`")
    embed_4.add_field(name="invite", value="`Sends bot invite`")
    await ctx.send(embed=embed_4)
    
def setup(bot):
  bot.add_cog(Help(bot))