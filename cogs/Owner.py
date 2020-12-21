import discord
import time
import json
from discord.ext import commands, tasks

def read_json(filename):
    with open(f"{filename}.json", "r") as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(f"{filename}.json", "w") as file:
        json.dump(data, file, indent=4)

class Owner(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.bot.blacklisted_users = []

  @commands.Cog.listener()
  async def on_ready(self):
    data = read_json("blacklist")
    self.bot.blacklisted_users = data["blacklistedUsers"]
    print("Bot is ready")

  @commands.command(aliases=["break"])
  @commands.is_owner()
  async def maintainence(self,ctx, *,arg):
        for guild in self.bot.guilds:
             await guild.text_channels[0].send(f"**LeBot is going under maintanence for: {arg}**")
        await ctx.send("Break message send")
        time.sleep(5)

  @commands.command(aliases=["cast"])
  @commands.is_owner()
  async def textcast(self,ctx, *,arg):
    await ctx.send("Casted the message")
    for guild in self.bot.guilds:
      await guild.text_channels[0].send(f"**{arg}**")

  @commands.command()
  @commands.is_owner()
  async def blacklist(self, ctx, user: discord.Member):
      self.bot.blacklisted_users.append(user.id)
      data = read_json("blacklist")
      data["blacklistedUsers"].append(user.id)
      write_json(data, "blacklist")
      await ctx.send(f"**{user} ({user.id})** has been blacklisted")

  @commands.command()
  @commands.is_owner()
  async def whitelist(self, ctx, user: discord.Member):
      self.bot.blacklisted_users.remove(user.id)
      data = read_json("blacklist")
      data["blacklistedUsers"].remove(user.id)
      write_json(data, "blacklist")
      await ctx.send(f"**{user} ({user.id})** has been removed from the blacklist")

def setup(bot):
  bot.add_cog(Owner(bot))