import discord
import praw 
import os
import random
import json
import aiohttp
from settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_USER_AGENT
from discord.ext import commands

reddit = praw.Reddit(client_id= REDDIT_CLIENT_ID,
                    client_secret=REDDIT_CLIENT_SECRET,
                    username=REDDIT_USERNAME,
                    password=REDDIT_PASSWORD,
                    user_agent=REDDIT_USER_AGENT)

class Praw(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=["memes"])
  async def meme(self, ctx):
    subreddit = reddit.subreddit("memes")
    all_subs = []

    hot = subreddit.hot(limit= 100)

    for submission in hot:
      all_subs.append(submission)
      
    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url
    all_comments = submission.comments.list()

    embed = discord.Embed(title = name, colour=discord.Colour(random.randint(1, 16777215)))
    embed.add_field(name="\u200b", value=f":+1: {random_sub.score}")
    embed.add_field(name="\u200b", value=f":speech_balloon: {len(all_comments)}")
    embed.set_image(url = url)
    await ctx.send(embed=embed)

  @commands.command(aliases=["wmemes"])
  async def wholesomememes(self, ctx):
    subreddit = reddit.subreddit("wholesomememes")
    all_subs = []

    hot = subreddit.hot(limit= 50)

    for submission in hot:
      all_subs.append(submission)
      
    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url
    all_comments = submission.comments.list()

    embed = discord.Embed(title = name, colour=discord.Colour(random.randint(1, 16777215)))
    embed.add_field(name="\u200b", value=f":+1: {random_sub.score}")
    embed.add_field(name="\u200b", value=f":speech_balloon: {len(all_comments)}")
    embed.set_image(url = url)

    await ctx.send(embed=embed)

  @commands.command(aliases=["sthoughts"])
  async def showerthoughts(self, ctx):
    subreddit = reddit.subreddit("showerthoughts")
    all_subs = []

    hot = subreddit.hot(limit= 100)

    for submission in hot:
      all_subs.append(submission)
      
    random_sub = random.choice(all_subs)

    name = random_sub.title

    await ctx.send(f"**{name}**")

  @commands.command()
  async def food(self, ctx):
    subreddit = reddit.subreddit("food")
    all_subs = []

    hot = subreddit.hot(limit= 50)

    for submission in hot:
      all_subs.append(submission)
      
    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url
    all_comments = submission.comments.list()

    embed = discord.Embed(title = name, colour=discord.Colour(random.randint(1, 16777215)))
    embed.add_field(name="\u200b", value=f":+1: {random_sub.score}")
    embed.add_field(name="\u200b", value=f":speech_balloon: {len(all_comments)}")

    embed.set_image(url = url)

    await ctx.send(embed=embed)


def setup(bot):
  bot.add_cog(Praw(bot))