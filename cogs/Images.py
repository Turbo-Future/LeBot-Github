import discord
import os
import random
import time
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trash(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/trash.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((130, 134))
        pfp2 = pfp2.resize((105, 109))
        im = im.copy()
        im.paste(pfp, (330, 185))
        im.paste(pfp2, (160, 30))
        im.save('./Images/trash2.jpg')
        await ctx.send(file=discord.File('./Images/trash2.jpg'))

    @commands.command()
    async def slap(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/slap.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((300, 300))
        pfp2 = pfp2.resize((300, 300))
        im = im.copy()
        im.paste(pfp, (808, 350))
        im.paste(pfp2, (500, 60))
        im.save('./Images/slapped.jpg')
        await ctx.send(file=discord.File('./Images/slapped.jpg'))

    @commands.command()
    async def delete(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/deletememe.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        #width and then length
        pfp = pfp.resize((88, 86))
        im = im.copy()
        im.paste(pfp, (53, 60))
        im.save('./Images/deletedmeme.jpg')
        await ctx.send(file=discord.File('./Images/deletedmeme.jpg'))

    @commands.command()
    async def tweet(self, ctx, *, text=None):
      if text == None:
        await ctx.send("What are you gonna tweet out?")
        #Profile Picuture
      image = Image.open('./Images/tweet.jpg')
      asset = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((88, 86))
      image = image.copy()
      image.paste(pfp, (25, 20))
      #display name
      font = ImageFont.truetype(r'./Fonts/ARIAL.TTF', 30)
      d = ImageDraw.Draw(image)
      d.text((130, 20), ctx.author.display_name, fill=(0,0,0), font=font)
      #username
      font2 = ImageFont.truetype(r'./Fonts/ARIAL.TTF', 27)
      d.text((125, 55), f"@{ctx.author.name}", fill=(128,128,128), font=font2)
      #tweet content
      font3 = ImageFont.truetype(r'./Fonts/ARIAL.TTF', 35)
      d.text((25, 125), text, fill=(0,0,0), font=font3)
      #retweets
      font4 = ImageFont.truetype(r'./Fonts/ARIAL.TTF', 25)
      d.text((15, 402), f"{random.randrange(2500, 7001)}",fill=(0,0,0), font=font4)
      #quote tweets
      d.text((190, 402), f"{random.randrange(2000, 5001)}", fill=(0,0,0), font=font4)
      #likes
      d.text((422, 402), f"{random.randrange(5000, 15001)}", fill=(0,0,0), font=font4)
      #Time + Device
      d.text((24,337), f"{time.strftime('%X')} UTC" ,fill=(128,128,128), font=font2)
      #Image
      image.save('./Images/tweeted.jpg')
      await ctx.send(file=discord.File('./Images/tweeted.jpg'))

    @commands.command()
    async def opinion(self, ctx, *, opinion=None):
      if opinion == None:
        await ctx.send("What is your opinion?")
      else:
        image = Image.open('./Images/opinion.jpg')
        font = ImageFont.truetype(r'./Fonts/ARIAL.TTF', 50)
        d = ImageDraw.Draw(image)
        d.text((300,560), f"{opinion}", fill=(0,0,0), font=font)

        image.save("./Images/opinion2.jpg")
        await ctx.send(file=discord.File("./Images/opinion2.jpg"))

    @commands.command()
    async def spank(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/spank.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp2 = Image.open(data)
        asset2 = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
        data2 = BytesIO(await asset2.read())
        pfp = Image.open(data2)
        pfp = pfp.resize((120, 134))
        pfp2 = pfp2.resize((105, 109))
        im = im.copy()
        im.paste(pfp, (150, 69))
        im.paste(pfp2, (269, 202))
        im.save('./Images/spanked.jpg')
        await ctx.send(file=discord.File('./Images/spanked.jpg'))

def setup(bot):
    bot.add_cog(image(bot))