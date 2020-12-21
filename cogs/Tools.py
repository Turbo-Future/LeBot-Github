import discord
import random
import time
import wikipedia
from discord.ext import commands

class Tools(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def say(self, ctx, *, message: commands.clean_content):
    if len(message) > 285:
      await ctx.send("Cannot type message's over 280 charcters long")
      return
    else:
      await ctx.message.delete()
      await ctx.send(f"{message}\n\n\n-{ctx.author}")
      return

  @say.error
  async def say_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("What do you want me to say?")  

  @commands.command()
  async def wiki(self,ctx, *, arg):
        def viki_sum(arg):
            definition = wikipedia.summary(arg,sentences=4,chars=1250)
            return definition
        embed = discord.Embed(title="***Wikipedia:***",description=viki_sum(arg), colour = discord.Colour(random.randint(1, 16777215)))
        await ctx.send(embed=embed)
        
  @wiki.error
  async def wiki_error(self, ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Page doesnt exist")
    else:
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("What do you want me to loop up?")

  @commands.command()
  async def google(self, ctx, *, link): 
    await ctx.send(f"https://google.com/?q={link.replace(' ', '+')}")

  @google.error
  async def google_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("What do you want me to search?")

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

  @commands.command(aliases=['pong','latency'])
  async def ping(self, ctx):
    await ctx.send(f'Latency: {round(self.bot.latency * 1000)}ms')

  @commands.command()
  async def avatar(self, ctx, *,  avamember : discord.Member=None):
    if avamember == None:
      avamember = ctx.message.author
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

  @commands.command(aliases=['stats','info'])
  async def Stats(self, ctx):
    embed = discord.Embed(title=f'{self.bot.user.name} Stats', description="", colour=discord.Colour(random.randint(1, 16777215)))
    embed.set_thumbnail(url=self.bot.user.avatar_url)
    embed.add_field(name="Name", value=self.bot.user.name)
    embed.add_field(name="ID:", value=self.bot.user.id)
    embed.add_field(name='Total Servers:', value=str(len(self.bot.guilds)))
    embed.add_field(name ="Latency:", value=f"{round(self.bot.latency * 1000)} ms")
    embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
    await ctx.send(embed=embed)

  @commands.command(aliases=["serverinfo"])
  async def sinfo(self, ctx):
    members = ctx.guild.members
    roles = ctx.guild.roles
    tc = ctx.guild.text_channels
    vc = ctx.guild.voice_channels
    embed = discord.Embed(title=f"{ctx.guild.name} stats",colour=discord.Colour(random.randint(1, 16777215)))
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="Server name", value=ctx.guild.name)
    embed.add_field(name="Owner", value=f"{ctx.guild.owner} | {ctx.guild.owner.mention}", inline=False)
    embed.add_field(name="ID", value=ctx.guild.id)
    embed.add_field(name="Region", value=ctx.guild.region)
    embed.add_field(name="Members", value=len(members))
    embed.add_field(name="Roles", value=len(roles))
    embed.add_field(name="Text Channels", value=len(tc))
    embed.add_field(name="Voice Channels", value=len(vc))
    await ctx.send(embed=embed)

  @commands.command(aliases=["whois"])
  async def userinfo(self, ctx, member: discord.Member = None):
    if not member: 
        member = ctx.message.author

    embed = discord.Embed(colour=discord.Colour(random.randint(1, 16777215)), timestamp=ctx.message.created_at,title=f"User Info - {member}")

    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Name", value=member.name)
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Nickname:", value=member.display_name)
    embed.add_field(name="Status", value=member.status)
    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M  UTC"))
    embed.add_field(name="Joined Server On:", value=(member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")))
    roles = [role.mention for role in member.roles[1:]]
    if len(member.roles[1:]) < 1:
        embed.add_field(name=f"Roles:",value="None", inline=False)
        embed.add_field(name="Highest Role:", value="None")
    elif roles != None:
        embed.add_field(name=f"Roles({len(roles)}):",value=",".join(roles), inline=False)
        embed.add_field(name="Highest Role:", value=member.top_role.mention)

    await ctx.send(embed=embed)

  @userinfo.error
  async def userinfo_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.send("Member isnt in the server or doesnt exist")

  @commands.command()
  @commands.cooldown(1, 180, commands.BucketType.user)
  async def suggest(self, ctx, *, suggestion=None):
    if suggestion == None:
      await ctx.send("Noob what you wanna suggest")
    else:
      channel = self.bot.get_channel(778534827456069643)
      await channel.send(f"LeBot Suggestion:\n{suggestion}\n\n\n```{ctx.author} ({ctx.author.id}) \nGuild name: {ctx.guild.name}\n Guild ID:{ctx.guild.id}```")
      await ctx.send("Thank you for the suggestion.")

  @suggest.error
  async def suggest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You can suggest after {round(error.retry_after)} seconds")
 

def setup(bot):
  bot.add_cog(Tools(bot))