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
      d.text((24,337), f"{time.strftime('%X')}",fill=(128,128,128), font=font2)
      #Image
      image.save('./Images/tweeted.jpg')
      await ctx.send(file=discord.File('./Images/tweeted.jpg'))

    @commands.command()
    async def text(self, ctx, *, text=None):
      if text == None:
        text = "What's the text my dood"
      #First value the in the line below shows the width, and the second value shows the length
      img = Image.new('RGB', (500, 100), color = (73, 109, 137))
  
      font = ImageFont.truetype(r'./Fonts/ARIAL.TTF', 17)
      d = ImageDraw.Draw(img)
      #Value one is pixel stuff. Fill, is the RGB color
      d.text((10,10), f"{text}", fill=(255,255,0), font=font)

      img.save('./Images/hello.jpg')
      await ctx.send(file=discord.File('./Images/hello.jpg'))

def setup(bot):
    bot.add_cog(image(bot))