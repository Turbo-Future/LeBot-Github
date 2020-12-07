import discord
import os
import time
import json
import keep_alive
from colorama import Fore
from settings import token
from discord.ext import commands, tasks

def get_prefix(bot, message):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = get_prefix, intents=intents)
bot.blacklisted_users = []

bot.remove_command('help')
#Cogs

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs/'):
  if filename.endswith('.py'):
      bot.load_extension(f'cogs.{filename[:-3]}')

@tasks.loop(minutes=1)
async def poggers():
  channel=bot.get_channel(763763048401338399)
  await channel.send("poggers")

#events

@bot.event
async def on_message(message):
    if message.author.id in bot.blacklisted_users:
        return

    await bot.process_commands(message)

    if message.content == "<@!734379671126278145>":
      with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
        
        prefix = prefixes[str(message.guild.id)]

      await message.channel.send(f"The server prefix is \"**{prefix}**\"")
      return

@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
      prefixes = json.load(f)

      prefixes[str(guild.id)] = "le"

      with open('prefixes.json', "w") as f:
        json.dump(prefixes, f, indent=4)  

@bot.event
async def on_guild_remove(guild):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  prefixes.pop(str(guild.id))

  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f, indent=4)

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "welcome":
            await channel.send(f'{member.mention} Yo wassup homie, welcome to the server')


@bot.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == "welcome":
            await channel.send(f'Alexa this is so sad, {member.name} has left the server, please play despacito')


#.mention for role in roles

#Owner commands

@bot.command()
@commands.is_owner()
async def bot_guild(ctx):
    await ctx.send("Printed server names")
    for guild in bot.guilds:
      print(Fore.GREEN + guild.name)

@bot_guild.error
async def bot_guild_error(ctx, error):
    if isinstance(error, commands.NotOwner):
      print(Fore.BLUE + f"{ctx.author} in {ctx.author.guild} has used bot_guild command")



#Testing



keep_alive.keep_alive()
bot.run(token)