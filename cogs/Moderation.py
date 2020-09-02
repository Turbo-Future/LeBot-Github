import discord
import json
from discord.ext import commands

class Moderation(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['purge'])
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, amount : int):
    await ctx.channel.purge(limit=amount+1)
      
  @clear.error
  async def clear_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        clear_error_2 = (f"You are missing the required permissions to use this command.")
        await ctx.send(clear_error_2)
      else:
        if isinstance(error, commands.MissingRequiredArgument):
            clear_error = (f"Incorrect usage of the command. Correct usage is leclear <amount of messages to clear>")
            await ctx.send(clear_error)
        
  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member : discord.Member, *, reason=""):
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

  @kick.error
  async def kick_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      kick_error_2 = (f"Who do you want me to boot?")
      await ctx.send(kick_error_2)

  @kick.error
  async def kick_error(self, ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
      await ctx.send(f"I do not have permissions to kick a user")

  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')
    if reason == None:
      reason1 = "for being a jerk!"
      await member.send(f"You have been banned from {ctx.guild.name} for {reason1}")
    else: 
      await member.send(f'You have been banned {ctx.guild.name} for "{reason}"')
    
  @ban.error
  async def ban_error(self,ctx, error):
    if isinstance(error, commands.MissingPermissions):
        ban_error_response = (f'Missing Required Permissions')
        await ctx.send(ban_error_response)
  
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
  @commands.has_permissions(manage_guild=True)
  async def prefix(self,ctx, prefix):

    with open('prefixes.json','r') as f:
      prefixes = json.load(f)

      prefixes[str(ctx.guild.id)] = prefix

      with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

        await ctx.send(f"Prefix changed to: {prefix}")
    
  @prefix.error
  async def prefix_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      prefix_error = ('Incorrect usage of the command. Proper usage is "leprefix {prefix}"')
      await ctx.send(prefix_error)
    if isinstance(error, commands.MissingPermissions):
      prefix_error = ("Missing Required Permissions")
      await ctx.send(prefix_error)

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def mute(self, ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name=["Muted", "shhh"])
    await member.add_roles(role)
    await ctx.send("Muted the user")

  @mute.error
  async def mute_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      mute_error = "Missing Required Permissions"
      await ctx.send(mute_error)

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def unmute(self, ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send("Unmuted the user")

  @mute.error
  async def unmute_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are not allowed to unmute people")

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

  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def unlock(self, ctx, channel: discord.TextChannel=None):
      channel = channel or ctx.channel
      overwrites = channel.overwrites[ctx.guild.default_role]
      overwrites.send_messages = True
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
      await ctx.send(f"I have removed `{channel.name}` from lockdown.")

  @lock.error
  async def lock_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("Missing Required Permissions")

  @unlock.error
  async def unlock_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("Missing Required Permissions")
        
def setup(bot):
  bot.add_cog(Moderation(bot))