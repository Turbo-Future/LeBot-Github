import discord
import json
import random
from discord.ext import commands


class Moderation(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.has_permissions(manage_guild=True)
  async def changeprefix(self, ctx, prefix=None):
    if prefix == None:
      await ctx.send("What should the new prefix be?")

    with open("prefixes.json", "r") as f:
      prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
      json.dump(prefixes, f, indent=4)

    await ctx.send(f"Prefix changed to **{prefix}**")

  @commands.command(aliases=['purge'])
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, amount : int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"{amount} message's was deleted by {ctx.author.name}")
      
  @clear.error
  async def clear_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        clear_error_2 = (f"You are missing the required permissions to use this command.")
        await ctx.send(clear_error_2)
      else:
        if isinstance(error, commands.MissingRequiredArgument):
            clear_error = (f"Incorrect usage of the command. Correct usage is leclear <amount of messages to clear>")
            await ctx.send(clear_error)
        else:
          if isinstance(error, commands.BadArgument):
            await ctx.send("tf is that supposed to mean")

        
  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member : discord.Member, *, reason=None):
    if member == ctx.message.author:
      await ctx.send("You cant kick yourself :/")
      return
    if member.id == 716323508472381510:
      await ctx.send("I cant kick myself :/")
      return
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.name}")
    if reason == None:
      reason1 = "for being a jerk!"
      await member.send(f"You have been kicked from {ctx.guild.name} for {reason1}")
    else: 
      await member.send(f'You have been kicked from {ctx.guild.name} for "{reason}"')

  @kick.error
  async def kick_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
        kick_error = (f'Missing Permissions')
        await ctx.send(kick_error)
    else:
      if isinstance(error, commands.BadArgument):
        await ctx.send("Cant kick a non-existent")

  @kick.error
  async def kick_Error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Who do you want me to boot?")

  @kick.error
  async def kick_error(self, ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
      await ctx.send(f"I do not have permissions to kick a user")

  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member : discord.Member, *, reason=None):
    if member == ctx.message.author:
      await ctx.send("You cant ban yourself :/")
      return
    if member.id == 716323508472381510:
      await ctx.send("I cant ban myself :/")
      return
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')
    if reason == None:
      reason1 = "for breaking the rules multiple times!"
      await member.send(f"You have been banned from {ctx.guild.name} for {reason1}")
    else: 
      await member.send(f'You have been banned {ctx.guild.name} for "{reason}"')
    
  @ban.error
  async def ban_error(self,ctx, error):
    if isinstance(error, commands.MissingPermissions):
        ban_error_response = (f'Missing Required Permissions')
        await ctx.send(ban_error_response)
    else:
      if isinstance(error, commands.BadArgument):
        await ctx.send("Cant ban a non-existent person")
  
  @ban.error
  async def ban_Error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      ban_error_response_2 = (f"Who do you want me to use the ban hammer on?")
      await ctx.send(ban_error_response_2)

  @commands.command()
  async def unban(self, ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
      user = ban_entry.user
  
    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"{user} have been unbanned sucessfully")

  @unban.error
  async def unban_error(self, ctx, error):
    if isinstance(error, commands.CommandInvokeError):
      unban_error_response = (f"This user has already been unbaned or has never been banned")
      await ctx.send(unban_error_response)

  @unban.error
  async def unban_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        unban_error_response_2 = f"Who do you want me to lift the ban hammer on? "
        await ctx.send(unban_error_response_2)

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def mute(self, ctx, member: discord.Member):
    if member.id == 716323508472381510:
      await ctx.send("I cant mute myself :/")
      return
    if member == ctx.author:
      await ctx.send("You cant mute your self")
    else:
      await ctx.send(f"Muted {member.name}")
      role = discord.utils.get(ctx.guild.roles, name="Muted")
      await member.add_roles(role)

  @mute.error
  async def mute_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("Missing Required Permissions")
    else:
      if isinstance(error, commands.BadArgument):
        await ctx.send("Invalid user")
 

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def unmute(self, ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send("Unmuted the user")

  @mute.error
  async def unmute_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Missing Required Permissions")

  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def lock(self, ctx, channel: discord.TextChannel=None):
      channel = channel or ctx.channel

      if ctx.guild.default_role not in channel.overwrites:
          overwrites = {
          ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
          await channel.edit(overwrites=overwrites)
          await ctx.send(f"I have put `{channel.name}` on lockdown.")
      elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
          overwrites = channel.overwrites[ctx.guild.default_role]
          overwrites.send_messages = False
          await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
          await ctx.send(f"I have put `{channel.name}` on lockdown.")

  @lock.error
  async def lock_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("Missing Required Permissions")
    else:
      if isinstance(error, commands.BadArgument):
        await ctx.send("Channel doesnt exist")


  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def unlock(self, ctx, channel: discord.TextChannel=None):
      channel = channel or ctx.channel
      overwrites = channel.overwrites[ctx.guild.default_role]
      overwrites.send_messages = True
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
      await ctx.send(f"I have removed `{channel.name}` from lockdown.")

  @unlock.error
  async def unlock_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("Missing Required Permissions")
    else:
      if isinstance(error, commands.BadArgument):
        await ctx.send("Channel doesnt exist")

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def rolecreate(self, ctx, rolename):
    guild = ctx.guild
    await guild.create_role(name=f"{rolename}", colour=discord.Colour(random.randint(1, 16777215)))
    await ctx.send(f'"{rolename}" role has been created')

  @rolecreate.error
  async def rolecreate_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Missing Required Permissions")
    else:
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("What role would you like me to make?")

  @rolecreate.error
  async def rolecreate_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("What role would you like me to make?")

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def roledelete(self, ctx, *, role: discord.Role):
    await role.delete()
    await ctx.send(f'"{role}" got yeeted')

  @roledelete.error
  async def roledelete_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("Missing Required Permissions")
    else:
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Which role do you want me to delete?")

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def roleadd(self, ctx, member: discord.Member, *, role):
    if member == None:
      member = ctx.message.author
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=f"{role}")
    await member.add_roles(role)
    await ctx.send(f'"{role}" role has been added')

  @roleadd.error
  async def roleadd_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.send("Either the role doesnt exist or you used the command in the wrong way. Correct way: {prefix}roleadd <member> <role name>")
    else:
      if isinstance(error, commands.MissingPermissions):
        await ctx.send("Missing Required Permission")
      else:
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("What role would you like me to add and to whom?")

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def roleremove(self, ctx, member: discord.Member=None,*, roles):
      role = discord.utils.get(ctx.guild.roles, name=f"{roles}")
      await member.remove_roles(role)
      await ctx.send(f"\"{roles}\" role has been removed")
      if member == None:
        await ctx.send("Ok I'll remove roles but from who tho??")

  @roleremove.error
  async def roleremove_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.send("Either the role doesnt exist or you used the command in the wrong way. Correct way: {prefix}roleremove <member> <role name>")
    else:
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Which role would you like me to remove and from whom?")
      else:
        if isinstance(error, commands.MissingPermissions):
          await ctx.send("Missing Required Permissions")


def setup(bot):
  bot.add_cog(Moderation(bot))