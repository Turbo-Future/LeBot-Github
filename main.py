import discord
import random
import time
import os
import json
import keep_alive
from discord.ext import commands, tasks

def get_prefix(bot, message):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix = get_prefix)
bot.remove_command('help')


#cogs

@bot.command()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')

  for filename in os.listdir('./cogs'):
    if filename.endswith('.js', '.py'):
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

playin = ["Pewdiepies Pixelings",
          "Brawl Stars",
          "Tuber Simulator"]
listenin = ["anime theme songs",
            "Rickroll ",
            "Complaints",
            "Eminem's Songs"]
watchin = ["YouTube",
           "Anime",
           "Meme Review",
           'LWIAY']

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

#Help

@bot.command()
async def help(ctx):
    embed = discord.Embed(title=f'Lelouch commands', description='', colour=discord.Colour.magenta())
    embed.add_field(name= ":gear:Moderation", value= (f"`Type help_mod for more info`"))
    embed.add_field(name= ":smile:Fun", value= (f"`Type help_fun for more info`"))
    embed.add_field(name=":tools:Tools", value= (f"`Type help_tools for more info`"))
    await ctx.send(embed=embed)

@bot.command()
async def help_fun(ctx):
    embed_2 = discord.Embed(title=f"Fun commands", description='', colour=discord.Colour.green())
    embed_2.add_field(name= "8ball", value="`Ask the 8ball a question`")
    embed_2.add_field(name= "askpewdiepie", value="`Ask pewdiepie a question`")
    embed_2.add_field(name= "dankrate", value= "`How dank are you?`")
    embed_2.add_field(name= "simprate", value="`How much of a simp are you?`")
    embed_2.add_field(name= "epicrate", value="`How epic are you?`")
    embed_2.add_field(name= "roast", value="`As the name says dummy. It roast people`")
    embed_2.add_field(name= "nny", value="`(͡° ͜ʖ ͡°)`")
    embed_2.add_field(name= "hack", value="`Get Hacked`")
    embed_2.add_field(name="pp", value="`smol or big pp?`")
    await ctx.send(embed=embed_2)

@bot.command()
async def help_mod(ctx):
  embed_3 = discord.Embed(title= f" Mod Commands", description="", colour=discord.Colour.blue())
  embed_3.add_field(name= "clear", value="`Purges messages.`")
  embed_3.add_field(name= "kick", value="`Mentioned user gets the boot`")
  embed_3.add_field(name= "ban", value= "`Mentioned user gets the ban hammer`")
  embed_3.add_field(name="unban", value="`Member gets unbanned.`")
  embed_3.add_field(name="prefix", value='`Changes prefix of the bot (Default is "le.")`')
  await ctx.send(embed=embed_3)

@bot.command()
async def help_tools(ctx):
  embed_4 = discord.Embed(title = f'Tools Commands', description="", colour=discord.Colour.purple())
  embed_4.add_field(name= "say", value="`Says stuff`")
  embed_4.add_field(name="dice", value="`Rolls and imaginary dice`")
  embed_4.add_field(name="toss", value="`Settle legendary battles over a coin toss`")
  embed_4.add_field(name= "ping", value="`Shows the ping`")
  embed_4.add_field(name="stats", value="`Shows the stats of the bot`")
  embed_4.add_field(name="avatar", value="`Sends avatar URL`")
  await ctx.send(embed=embed_4)

#Moderation

@bot.command(aliases=['purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount+1)

@clear.error
async def clear_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    clear_error_2 = (f"You are missing the required permissions to use this command.")
    await ctx.send(clear_error_2)
  else:
    if isinstance(error, commands.MissingRequiredArgument):
        clear_error = (f"Incorrect usage of the command. Correct usage is leclear <amount of messages to clear>")
        await ctx.send(clear_error)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')
    user = discord.Member
    if {user.id} == "584831008344506388":
      await ctx.send(f"Why you trynna kick me master dood?")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        kick_error = (f'Missing  Permissions')
        await ctx.send(kick_error)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        ban_error_response = (f'Missing Required Permissions')
        await ctx.send(ban_error_response)

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")

  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"Unbanned {user.name}")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, prefix):

  with open('prefixes.json','r') as f:
      prefixes = json.load(f)

      prefixes[str(ctx.guild.id)] = prefix

      with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

        await ctx.send(f"Prefix changed to: {prefix}")

@prefix.error
async def prefix_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    prefix_error = ('Incorrect usage of the command. Proper usage is "leprefix {prefix}"')
    await ctx.send(prefix_error)
    if isinstance(error, commands.MissingPermissions):
      prefix_error = ("Missing Required Permissions")
      await ctx.send(prefix_error)



#Fun

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    Responses = [" It is certain.",
                 "It is decidedly so.",
                    "Without a doubt.",
                 "Yes – definitely.",
                   "You may rely on it.",
                  "As I see it, yes.",
                   "Most likely.",
                  "Outlook good.",
                  "Yes.",
                  "Signs point to yes.",
                 "Could you shut up?",
                 "Ask again later.",
                   "Better not tell you now.",
                   "Cannot predict now.",
                   "Concentrate and ask again.",
                  "Do not count on it.",
                  "My reply is no.",
                  "My sources say no.",
                    "Outlook not so good.",
                 "Very doubtful.",
                  "Shut it Buster",
                  "Why are you even asking me",
                    "Come another time.",
                 "REEEEEEEEEEEEEEEEEEEEEE"]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(Responses)}')

@bot.command(aliases=['askfelix','askpewds'])
async def askpewdiepie(ctx, *, question):
    pewd_response = ["FLOOR GANG OUH",
            "Ceiling gang is cringe",
             "I moisturize because my skin gets really dry",
             "Im swedish",
             "Ok but, who the hell is Jake Paul?",
           "BIG BRAIN",
           "BIG PP",
           "Yes",
           "Idk but, Your floor gang",
           "smol brain",
           "smol pp",
           "NO",
           "Idk but, Your ceiling gang",
           "idk, ask Sive"]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(pewd_response)}')

@bot.command()
async def dankrate(ctx):
    dankrate_response = random.randint(1,100)
    await ctx.send("Your dankrate is "+str(dankrate_response)+"%")

@bot.command()
async def nny(ctx):
    await ctx.send(f'( ͡° ͜ʖ ͡°)')

@bot.command(aliases=["picrate","er"])
async def epicrate(ctx):
    epicrate_response = random.randint(1,100)
    await ctx.send("Your epicrate is "+str(epicrate_response)+"%")

@bot.command()
async def simprate(ctx):
    simprate_response = random.randint(1,100)
    await ctx.send(f"Your simprate is "+str(simprate_response)+"%")

@bot.command()
async def kill(ctx, member: discord.Member):
    if {member.name} == {ctx.author.name}:
        await ctx.send(f"Lets not do that {ctx.author.name}")
        return
    else:
      kill_response = [f'{member.name} died of cringe',
     f'{member.name} got hit by a canonball',
    f'{member.name} got drunk and decided to jump of the cliff',
    f'{member.name} got shot in the head',
    f'{member.name} got into a fight with the Pope. {member.name} is going to hell',
    f'{member.name} swallowed a rock',
    f'{member.name} died of watching T-Series',
    f'{member.name} became a hitman but got killed by his target instead. {member.name} is a failure.',
    f'{member.name} got rickrolled.',
    f'{member.name} dies due to lack of friends',
    f'{member.name} fell down a cliff while playing pokemon go']
    await ctx.send(f'{random.choice(kill_response)}')

@bot.command()
async def roast(ctx, member: discord.Member):
    roast_response = ['You’re the reason God created the middle finger.',
    'You are more disappointing than an unsalted pretzel.',
    'I forgot the world revolves around you. My apologies, how silly of me.',
    'Your face makes onions cry.',
    'I cant wait to forget you',
    'Take my lowest prioirty and put yourself beneath it',
    "You're like a square blade, all edge no point",
    'You have a face made for radio.',
    "Dont play hard to get when you're hard to want",
    'Just because your head is shaped like a light bulb, doesnt mean you have good ideas',
    f'There will never be enough middle fingers for you in the world {member.name}',
    "Your identity is more confusing than the Japanese alphabet's",
    "When you die, people will struggle to say nice things about you",
    "People like you are the reson god doesnt talk to use anymore",
    "You're as useless as 'ay' in okay",
    "If laughter is the best medicine, you're face must be curing the world"]
    await ctx.send(f'{random.choice(roast_response)}')

@bot.command()
async def pp(ctx):
  pp_response = ['8D',
  "8=D",
  "8==D",
  "8===D",
  "8====D",
  "8=====D",
  "8=======D",
  "8========D"]
  await ctx.send(f'{random.choice(pp_response)}')

@bot.command(aliases=['hack','HACK'])
async def Hack(ctx, member : discord.Member):
  if {member.name} == {ctx.author.name}:
      await ctx.send(f"How do you hack yourself")
  else:
    message = await ctx.send(f" Hacking {member.name} right now chief")
    time.sleep(2)
    await message.edit(content=f"Fetching IP adress")
    time.sleep(2)
    await message.edit(content=f"IP found 182.110.224.90")
    time.sleep(2)
    await message.edit(content=f"Fetching Email and Password")
    time.sleep(2)
    hack_response_email = [f'{member.name}sucks@gmail.com',
    f'{member.name}hasnofriends@gmail.com']
    hack_response_password = ['iliketseries',
    'forgotten',
    'whyarewestillhere']
    await message.edit(content=f"**Email:** {random.choice(hack_response_email)}\n**Password:** {random.choice(hack_response_password)}")
    time.sleep(2)
    hack_Response_tabs = ['animehentai.com',
    "reddit.com",
    "useless.com",
    "howtogetfriends.com"]
    await message.edit(content=f"Fetching recently closed tabs")
    time.sleep(2)
    await message.edit(content=f"{random.choice(hack_Response_tabs)}")
    time.sleep(2)
    await message.edit(content=f"Trojan Injected")
    time.sleep(2)
    await message.edit(content=f"Hack completed chief")

#Tools

@bot.command()
async def say(ctx, *, text="", ):
  say_embed = discord.Embed(title=f'Message by: {ctx.author.name}', description="", colour=discord.Colour.red())
  say_embed.add_field(name=f"Message:", value=f"{text}")
  await ctx.send(embed=say_embed)

@say.error
async def say_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    say_error = (f"What do you want me to say?")
    await ctx.send(say_error)

@bot.command(aliases=['stats','STATS'])
async def Stats(ctx):
    embed = discord.Embed(title=f'{bot.user.name} Stats', description="", colour=discord.Colour.red())
    embed.add_field(name='Developed In:', value="Python")
    embed.add_field(name='Total Servers:', value=str(len(bot.guilds)))
    embed.add_field(name='Total Users in the server:', value=len(ctx.guild.members))
    embed.add_field(name='Bots DOB:', value="17/6/2020")
    embed.add_field(name='Bot Developer:', value="Dio#2097")
    embed.add_field(name ="Latency:", value=f"{round(bot.latency * 1000)} ms")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)

@bot.command(aliases=['pong','latency'])
async def ping(ctx):
  await ctx.send(f'Latency: {round(bot.latency * 1000)}ms')

@bot.command()
async def dice(ctx):
  dice_response = random.randint(1,6)
  dice_message = await ctx.send("Rolling the dice.....")
  time.sleep(4)
  await dice_message.edit(content=f"You rolled a {dice_response}")

@bot.command()
async def toss(ctx):
    toss_response = ['Heads','Tails']
    toss_message = await ctx.send("The coin is in the air....")
    time.sleep(3)
    rancoin = random.choice(toss_response)
    await toss_message.edit(content=f"The coin toss results is {rancoin}")



keep_alive.keep_alive()

bot.run('NzE2MzIzNTA4NDcyMzgxNTEw.XxhFKA.X_iNoqNCgiYDwqW5evXDI988uws')
