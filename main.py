import discord
import os
import random
import asyncio
import json
import time
import keep_alive
from colorama import Fore
from settings import token
from discord import Embed
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
          "Cyberpunk 2077 | @LeBot",
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

@bot.event
async def on_message_edit(before, after):
  if before.guild.id == "707490932655652945":
        embed = Embed(description=f"Message edited in {before.channel.mention}", color=0x4040EC)
        embed.set_author(name=before.author, url=Embed.Empty, icon_url=before.author.avatar_url)
        embed.add_field(name="Original Message", value=before.content)
        embed.add_field(name="Edited Message", value=after.content)
        embed.timestamp = after.created_at
        channel=bot.get_channel(772730486912450581)
        await channel.send(embed=embed)

#.mention for role in roles

#Testing

snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

@bot.event
async def on_message_delete(message):

    global snipe_message_content
    global snipe_message_author
    global snipe_message_id

    snipe_message_content = message.content
    snipe_message_author = message.author
    snipe_message_id = message.id
    await asyncio.sleep(60)

    if message.id == snipe_message_id:
        snipe_message_author = None
        snipe_message_content = None
        snipe_message_id = None


t = time.localtime()
current_time = time.strftime("%H:%M", t)

@bot.command()
async def snipe(message):
    if snipe_message_content==None:
        await message.channel.send("Theres nothing to snipe.")
    else:
        embed = discord.Embed(title=f"Good luck covering that one up {snipe_message_author}",description=f"{snipe_message_content}", colour=discord.Colour.red())
        embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator} at {current_time}", icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)
        return

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