import discord
import random
import time
import os
import json
import asyncio
import keep_alive
from discord.ext import commands, tasks

def get_prefix(bot, message):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix = get_prefix)
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


#events

@bot.event
async def on_ready():
  change_activity.start()
  print('Bot is ready')

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

playin = ["Pewdiepies Pixelings | lehelp",
          "Brawl Stars | lehelp",
          "Tuber Simulator | lehelp"]
listenin = ["anime theme songs | lehelp",
            "Rickroll | lehelp",
            "Complaints | lehelp",
            "Eminem's Songs | lehelp"]
watchin = ["YouTube | lehelp",
           "Anime | lehelp",
           "Meme Review | lehelp",
           'LWIAY | lehelp']

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
async def on_guild_join(guild):
    with open('prefixes.json','r') as f:
      prefixes = json.load(f)

    prefixes[str(guild.id)] = 'le'

    with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)
      for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hey there! Thanks for adding me to the server! My default prefix is "le"')
        break

@bot.event
async def on_guild_remove(guild):
  with open('prefixes.json','r') as f:
      prefixes = json.load(f)
      
      prefixes.pop(str(guild.id))

      with open('prefixes.json', 'w') as f:
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


#Tools

@bot.command(aliases=['stats','STATS'])
async def Stats(ctx):
    embed = discord.Embed(title=f'{bot.user.name} Stats', description="", colour=discord.Colour(random.randint(1, 16777215)))
    embed.add_field(name='Total Servers:', value=str(len(bot.guilds)))
    embed.add_field(name='Total Users in the server:', value=len(ctx.guild.members))
    embed.add_field(name='Bot Developer:', value="Dio#2097")
    embed.add_field(name ="Latency:", value=f"{round(bot.latency * 1000)} ms")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)

@bot.command(aliases=['pong','latency'])
async def ping(ctx):
  await ctx.send(f'Latency: {round(bot.latency * 1000)}ms')


keep_alive.keep_alive()
token = os.environ.get("token")
bot.run(token)
