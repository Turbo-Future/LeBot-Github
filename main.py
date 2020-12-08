import discord
import os
import random
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

#Events

@bot.event
async def on_ready():
    change_activity.start()

def RAG():
    activity_type = random.choice(['watchin','listenin','playin'])
    activity = ''
    if activity_type == 'watchin':
        activity = random.choice(watchin)
    elif activity_type == 'listenin':
        activity = random.choice(listenin)
    else:
        activity = random.choice(playin)
    return activity_type, activity

playin = ["Fall Guys | @LeBot",
          "CS:GO | @LeBot",
          "WATCHDOGS 2 | @LeBot",
          "Among Us | @LeBot",]
listenin = ["Spotify | @LeBot",
            "Complaints",
            "Eminem's Songs"]
watchin = ["YouTube | @LeBot",
           "Anime | @LeBot",
           "Meme Review | @LeBot"]

@tasks.loop(seconds=60)
async def change_activity():
    activity_type, activity = RAG()
    if activity_type == 'playin':
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=activity))
    elif activity_type == 'listenin':
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
    else:
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=activity))

@bot.event
async def on_message(message):
    if message.author.id in bot.blacklisted_users:
        return

    await bot.process_commands(message)

    if message.content == "<@!716323508472381510>":
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

keep_alive.keep_alive()
bot.run(token)