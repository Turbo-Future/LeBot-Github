import discord
import json
import random
from discord.ext import commands

#Functions
#Work

youtuber = {}

def youtube():
  global youtuber
  try:
    with open ('./Jobs/youtuber.json', "r") as f:
      youtuber = json.load(f)
  except FileNotFoundError:
    print("File not found")

developer = {}

def developing():
  global developer
  try:
    with open('./Jobs/developer.json', "r") as f:
        developer = json.load(f)
  except FileNotFoundError:
        print("Error")

scientist = {}

def science():
  global scientist
  try:
    with open('./Jobs/scientist.json', "r") as f:
        scientist = json.load(f)
  except FileNotFoundError:
        print("Error")

passive = {}

def passive_nub():
  global passive
  try:
    with open("passive.json") as f:
        passive = json.load(f)
  except FileNotFoundError:
        print("Error")

#Money

async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

        with open("bank.json", "w") as f:
            json.dump(users, f)
        return True

async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)

        return users

async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("bank.json", "w") as f:
        json.dump(users, f)

    bal = users[str(user.id)]["wallet"], users[str(user.id)]["bank"]
    return bal

#Shop
  
async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("bank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked"]


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.9 * item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("bank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "wallet")

    return [True, "Worked"]

async def use_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            break

    if name_ == None:
        return [False, 1]

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("bank.json", "w") as f:
        json.dump(users, f)

    return [True, "Worked"]

mainshop = [{
    "name": "Cookie",
    "price": 10,
    "description": "Grandma's tasty cookies! Yum"
}, {
    "name": "Laptop",
    "price": 500,
    "description": "Post some dank meme's"
}]

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        science()
        developing()
        youtube()
        passive_nub()


    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        elif member.bot == True:
            await ctx.send("I don't think bot's have balance's")
            return

        await open_account(member)
        users = await get_bank_data()

        wallet_amt = users[str(member.id)]["wallet"]
        bank_amt = users[str(member.id)]["bank"]

        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name="Wallet:", value=round(wallet_amt), inline=False)
        embed.add_field(name="Bank:", value=round(bank_amt), inline=False)
        embed.add_field(
            name="Total:", value=round(bank_amt + wallet_amt), inline=False)
        embed.set_author(
            name=f"{member.name}'s balance's",
            url=discord.Embed.Empty,
            icon_url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, amount=None):
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter an amount to withdraw")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return
            if amount == 0:
                await ctx.send("Can't withdraw nothing!")
                return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")

        await ctx.send(f"You withdrew {amount} coins")

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount=None):
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter an amount to deposit")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return

        await update_bank(
            ctx.author,
            -1 * amount,
        )
        await update_bank(ctx.author, amount, "bank")

        await ctx.send(f"You deposited {amount} coins")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        earnings = random.randrange(101, 500)

        beg_response = [
            f"Someone gave you {earnings} coins. Gee I wonder who",
            f"LeBot Dev just donated {earnings} coins.",
            f"Taylor Swift just donated {earnings} coins.",
            f"Lelouch just donated {earnings} coins.",
            f"Avi just gave you {earnings} coins. I wonder who he is",
            f"Snoop Dogg just donated {earnings} coins.",
            f"Pewdiepie just donated {earnings} coins to you!! Brofist!!",
            f"Eminem has donated {earnings} coins to you",
            f"Danny Devito: **No money for you**"
        ]
        rand_beg = random.choice(beg_response)

        await ctx.send(rand_beg)
        
        users[str(user.id)]["wallet"] += earnings

        with open("bank.json", "w") as f:
            json.dump(users, f)

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Your on a cooldown!", color=discord.Color.blue())
            embed.add_field(
                name="\u200b",
                value=
                f"Slow down will ya?\n Wait for {round(error.retry_after)} seconds"
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["claim"])
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        amount = round(5000)
        await open_account(ctx.author)
        await update_bank(ctx.author, amount, "wallet")
        embed = discord.Embed(
            title="You daily claim!!",
            colour=discord.Colour(random.randint(1, 1627777)))
        embed.add_field(
            name="Your daily amount!",
            value="5000 coins have been sent to you in your wallet")
        embed.set_footer(text="The command can only be used once per day")
        await ctx.send(embed=embed)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="You're on a cooldown!", color=discord.Color.blue())

            cd = round(error.retry_after)
            hours = str(cd // 3600)
            minutes = str(cd % 3600 // 60)
            s = str(cd % 3600 % 60)

            embed.add_field(
                name="\u200b",
                value=
                f"Slow down will ya?\n Wait for `{self.leadingZero(hours)}hours{self.leadingZero(minutes)}minutes`"
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def send(self, ctx, amount=None, *, member: discord.Member):
        await open_account(ctx.author)
        await open_account(member)

        if member.bot == True:
            await ctx.send("I don't think bot's have balance's")
            return

        if amount == None:
            await ctx.send("Please enter an amount to send")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return
        if amount == 0:
            await ctx.send(
                "Sending 0 coins is the equilavent of sending nothing.")
            return

        await update_bank(ctx.author, -1 * amount, "wallet")
        await update_bank(member, amount, "wallet")

        await ctx.send(f"You gave {amount} coins to {member.name}")

    @send.error
    async def send_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Member doesnt exist")
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Your on a cooldown!", color=discord.Color.blue())
        embed.add_field(
            name="\u200b",
            value=
            f"Slow down will ya?\n Wait for {round(error.retry_after)} seconds"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["steal"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx, *, member: discord.Member):
        await open_account(ctx.author)
        await open_account(member)
        #variables 
        id = str(ctx.author.id)
        user_id = str(member.id)
        bal = await update_bank(member)
        user_bal = await update_bank(ctx.author)
        #Bot check
        if member.bot == True:
            await ctx.send("I don't think bot's have balance's")
            return
        #Passive mode check
        if id in passive:
          await ctx.send("You cannot rob others when you are in passive mode.")
          return
        if user_id in passive:
          await ctx.send("You cannot rob user's who are in passive mode.")
        #Poor check
        if user_bal[0] < 250:
            await ctx.send("You need more than 250 coins to rob someone else!")
            return
        if bal[0] < 250:
            await ctx.send(
                "Member doesn't have atleast 250 coins in their wallet. Not worth it."
            )
            return
        #If user is not poor
        earnings = random.randrange(0, bal[0])

        await update_bank(ctx.author, earnings, "wallet")
        await update_bank(member, -1 * earnings, "wallet")

        await ctx.send(f"You robbed {member.name} and got {earnings} coins")

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Member doesnt exist")
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="You're on a cooldown!", color=discord.Color.blue())

            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)

            embed.add_field(
                name="\u200b",
                value=
                f"Slow down will ya?\nWait for `{self.leadingZero(minutes)}mins{self.leadingZero(seconds)}secs`."
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["bankrob"])
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def heist(self, ctx, *, member: discord.Member):
        await open_account(ctx.author)
        await open_account(member)
        #variables 
        id = str(ctx.author.id)
        user_id = str(member.id)
        bal = await update_bank(member)
        user_bal = await update_bank(ctx.author)
        #Bot check
        if member.bot == True:
            await ctx.send("I don't think bot's have balance's")
            return
        #Passive mode check
        if id in passive:
          await ctx.send("You cannot rob others when you are in passive mode.")
          return
        if user_id in passive:
          await ctx.send("You cannot rob user's who are in passive mode.")
        #Poor check
        if user_bal[0] < 1000:
            await ctx.send("You need more than 1000 coins to rob someone else!")
            return
        if bal[1] < 2500:
            await ctx.send(
                "Member doesn't have atleast 2500 coins in their wallet. Not worth it."
            )
            return
        #If user is not poor
        earnings = random.randrange(0, bal[1])

        await update_bank(ctx.author, earnings, "wallet")
        await update_bank(member, -1 * earnings, "bank")

        await ctx.send(f"You robbed {member.name} and got {earnings} coins")

    @heist.error
    async def heist_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Member doesnt exist")
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="You're on a cooldown!", color=discord.Color.blue())

            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)

            embed.add_field(
                name="\u200b",
                value=
                f"Slow down will ya?\nWait for `{self.leadingZero(minutes)}mins{self.leadingZero(seconds)}secs`."
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def slots(self, ctx, amount=None):
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter an amount")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return

        final = []
        for i in range(3):
            a = random.choice([":apple:", ":star:", ":full_moon:"])

            final.append(a)

        if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
          await update_bank(ctx.author, 2 * amount)
          embed = discord.Embed(title="Result", color=discord.Color.green())
          embed.add_field(name="The result", value=final)
          embed.add_field(name="\u200b", value=f"You won {2*amount} coins", inline=False)
          await ctx.send(embed=embed)
        elif final[0] == final[1] and final[0] == final[2] and final[1] == final[
                2]:
          embed = discord.Embed(title="Result", colour=discord.Color.green())
          embed.add_field(name="The result", value=final)
          embed.add_field( name="\u200b",value=f"You won {3*amount} coins. Woah, dude 3 in row? That's sick",inline=False)
          await ctx.send(embed=embed)
          await update_bank(ctx.author, 3 * amount)
        else:
          await update_bank(ctx.author, -1 * amount)
          embed = discord.Embed(title="Result", color=discord.Color.red())
          embed.add_field(name="The result", value=final)
          embed.add_field(
                name="\u200b",
                value=f"You lost {-1*amount} coins",
                inline=False)
          await ctx.send(embed=embed)

    @slots.error
    async def slots_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Your on a cooldown!", color=discord.Color.blue())
        embed.add_field(
            name="\u200b",
            value=
            f"Slow down will ya?\n Wait for {round(error.retry_after)} seconds"
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def gamble(self, ctx, amount=None):
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("Please enter an amount")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return

        user_guess = random.randrange(1,6)
        leguess = random.randrange(1,6)
        
        #Win
        if user_guess > leguess:
          await update_bank(ctx.author, 2 * amount)
          embed = discord.Embed(title=f"{ctx.author.name} gambling result", color=discord.Color.green())
          embed.add_field(name="\u200b", value=f"You won {round(2*amount)} coins.", inline=False)
          embed.add_field(name="\u200b", value=f"You now have {round(2*amount+bal[0])}", inline=False)
          embed.add_field(name=f"{ctx.author.name}", value=f"Rolled {user_guess}")
          embed.add_field(name=f"LeBot Beta", value=f"Rolled {leguess}", inline=True)
          await ctx.send(embed=embed)
          #Tie
        elif user_guess == leguess:
          await update_bank(ctx.author, -0.5 * amount)
          embed = discord.Embed(title=f"{ctx.author.name} gambling result", color=discord.Color.gold())
          embed.add_field(name="\u200b", value=f"You tied and lost {round(-0.5*amount)} coins.", inline=False)
          embed.add_field(name="\u200b", value=f"You now have {round(-0.5*amount+bal[0])}", inline=False)
          embed.add_field(name=f"{ctx.author.name}", value=f"Rolled {user_guess}", inline=False)
          embed.add_field(name=f"LeBot Beta", value=f"Rolled {leguess}", inline=True)
          await ctx.send(embed=embed)
          #Loss
        elif user_guess < leguess:
          await update_bank(ctx.author, -1 * amount)
          embed = discord.Embed(title=f"{ctx.author.name} gambling result", color=discord.Color.red())
          embed.add_field(name="\u200b", value=f"You lost {round(-1*amount)} coins.", inline=False)
          embed.add_field(name="\u200b", value=f"You now have {round(-1*amount+bal[0])}", inline=False)
          embed.add_field(name=f"{ctx.author.name}", value=f"Rolled {user_guess}", inline=False)
          embed.add_field(name=f"LeBot Beta", value=f"Rolled {leguess}", inline=False)
          await ctx.send(embed=embed)

    @gamble.error
    async def gamble_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Your on a cooldown!", color=discord.Color.blue())
        embed.add_field(
            name="\u200b",
            value=
            f"Slow down will ya?\n Wait for {round(error.retry_after)} seconds"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Shop")

        for item in mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            embed.add_field(name=name, value=f"${price} | {desc}")

        await ctx.send(embed=embed)

    @commands.command(aliases=["inv", "inventory"])
    async def bag(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em = discord.Embed(title=f"{user.name}'s Inventory", color=discord.Colour.dark_gold())
        for item in bag:
            name = item["item"].capitalize()
            amount = item["amount"]

            if amount == 0:
                em.add_field(
                    name="You don't have any items!",
                    value=
                    "Use {prefix}shop to find out what's available on the shop!"
                )
            else:
                em.add_field(name=name, value=amount, inline=False)

        await ctx.send(embed=em)

    @commands.command()
    async def buy(self, ctx, item, amount=1):
        await open_account(ctx.author)

        res = await buy_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("That Object isn't there!")
                return
            if res[1] == 2:
                await ctx.send(
                    f"You don't have enough money in your wallet to buy {amount} {item}"
                )
                return

        await ctx.send(f"You just bought {amount} {item}")

    @commands.command()
    async def sell(self, ctx, item, amount=1):
        await open_account(ctx.author)

        res = await sell_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("That Object isn't there!")
                return
            if res[1] == 2:
                await ctx.send(f"You don't have {amount} {item} in your bag.")
                return
            if res[1] == 3:
                await ctx.send(f"You don't have {item} in your bag.")
                return

        await ctx.send(f"You just sold {amount} {item}.")

    @commands.command()
    async def use(self, ctx, item_name, amount=1):
      await open_account(ctx.author)
      #Making sure the thing works
      res = await use_this(ctx.author, item_name, amount)

      if not res[0]:
          if res[1] == 1:
            await ctx.send("Item doesnt even exist in the mainshop smh.")
            return
          if res[1] == 2:
            await ctx.send(f"You don't have that many {item_name}'s in your inventory.")
            return
          if res[1] == 3:
            await ctx.send(f"You don't have {item_name} in your bag.")
            return

      for item in mainshop:
        item_name = item["name"].lower()
        if item_name == "cookie":
          await ctx.send("You ate cookie. It was tasty")

    @commands.command()
    async def search(self, ctx):
        await open_account(ctx.author)

        place1 = ["couch", "park", "road", "coat"]
        place2 = ["dog", "tree", "car", "trashcan"]
        place3 = ["discord", "grass", "pocket", "workplace"]

        places = [
            random.choice(place1),
            random.choice(place2),
            random.choice(place3)
        ]
        placesToSearch = ', '.join([f"`{x.title()}`" for x in places])

        await ctx.send(
            f"Where do you wanna search? Pick from the list below.\n {placesToSearch}"
        )
        response = await self.bot.wait_for(
            'message', check=lambda message: message.author == ctx.author)

        if response.content.lower() in places:
            earnings = random.randrange(301)
            await update_bank(ctx.author, earnings, "wallet")
            await ctx.send(f"You just found {earnings} coins. Cool")   
        else:
            await ctx.send("Thats not a part of the list tho?")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
      await open_account(ctx.author)
      #Cooldown reset
      #Variables
      salary = 2200
      id = str(ctx.author.id)
      #If user is unemployed :laughard:
      if id not in developer and id not in scientist and id not in youtuber:
        self.work.reset_cooldown(ctx)
        await ctx.send("Your unemployed, You can work as a `developer` or a `scientist` or a `youtuber` . Pick one.\n\nNote: All jobs have the same amount of salary")
        message = await self.bot.wait_for('message', check=lambda message : message.author == ctx.author)
        #Developer
        if message.content == "developer":
          developer[id] = 1
          with open('./Jobs/developer.json', 'w') as f:
            json.dump(developer, f) 
          await ctx.send("Congratualations! You now work as a developer!")
          return
        #youtuber
        elif message.content == "youtuber":
          youtuber[id] = 1
          with open('./Jobs/scientist.json', 'w') as f:
            json.dump(scientist, f, )
            await ctx.send("Congratualations! You now work as a youtuber!")
            return
        #scientist
        elif message.content == "scientist":
          scientist[id] = 1
          with open('./Jobs/youtuber.json', 'w') as f:
            json.dump(youtuber, f, ) 
          await ctx.send("Congratualations! You now work as a scientist!")
        else:
          await ctx.send("That's not a part of the list.")
          return
      #Dev work
      elif id in developer:
        dev_work = ["Type the following: `Python is the best. Everything else is trash.`", "Type the following: `Time to steal some code.`", "Answer the following question: `Which is the best bot in the world?`"]
        rand_dev = random.choice(dev_work)
        await ctx.send(rand_dev)
        message = await self.bot.wait_for('message', check=lambda message : message.author == ctx.author)
        if rand_dev == dev_work[0]:
          if message.content == "Python is the best. Everything else is trash.":
            if id in passive:
              await ctx.send("You have earned 2000 coins!")
              await update_bank(ctx.author, salary-600, "wallet")
            else:
              await ctx.send("You have earned 2200 coins!")
              await update_bank(ctx.author, salary, "wallet")
          else:
            await ctx.send("You can't even type a sentence properly? You get 0 coins")
            return
        elif rand_dev == dev_work[1]:
          if message.content == "Time to steal some code.":
            if id in passive:
              await ctx.send("You have earned 2000 coins!")
              await update_bank(ctx.author, salary-600, "wallet")
            else:
              await ctx.send("You have earned 2200 coins!")
              await update_bank(ctx.author, salary, "wallet")
          else:
            await ctx.send("You can't even type a sentence properly? Dumb")
            return
        elif rand_dev == dev_work[2]:
          if message.content == "LeBot":
            if id in passive:
              await ctx.send("You have earned 2000 coins!")
              await update_bank(ctx.author, salary-600, "wallet")
            else:
              await ctx.send("You have earned 2200 coins!")
              await update_bank(ctx.author, salary, "wallet")
          else:
            await ctx.send("It's LeBot......")
            return
      #Youtube work
      elif id in youtuber:
        youtuber_work = ["Type the following: `I wish I had 100mil sub's like pewdiepie.`", "Type the following: `The Hair Trilogy is the best trilogy to ever exist.`", "Type the following: `Papa Franku please come back.`"]
        rand_youtube = random.choice(youtuber_work)
        await ctx.send(rand_dev)
        message = await self.bot.wait_for('message', check=lambda message : message.author == ctx.author)
        if rand_youtube == youtuber_work[0]:
          if message.content == "I wish I had 100mil sub's like pewdiepie.":
            if id in passive:
              await ctx.send("You have earned 2000 coins!")
              await update_bank(ctx.author, salary-600, "wallet")
            else:
              await ctx.send("You have earned 2200 coins!")
              await update_bank(ctx.author, salary, "wallet")
          else:
            await ctx.send("You can't even type a sentence properly? Dumb")
            return
        elif rand_youtube == youtuber_work[1]:
          if message.content == "The Hair Trilogy is the best trilogy to ever exist.":
            if id in passive:
              await ctx.send("You have earned 2000 coins!")
              await update_bank(ctx.author, salary-600, "wallet")
            else:
              await ctx.send("You have earned 2200 coins!")
              await update_bank(ctx.author, salary, "wallet")
          else:
            await ctx.send("You can't even type a sentence properly? Dumb")
            return
        elif rand_youtube == youtuber_work[2]:
          if message.content == "Papa Franku please come back.":
            if id in passive:
              await ctx.send("You have earned 2000 coins!")
              await update_bank(ctx.author, salary-600, "wallet")
            else:
              await ctx.send("You have earned 2200 coins!")
              await update_bank(ctx.author, salary, "wallet")
          else:
            await ctx.send("You can't even type a sentence properly?")
            return
      #scientist work
      elif id in scientist:
        science_work = ["Type the following: `I wonder if waterproof spray can make me walk on water.`", "Type the following: `Don't trust atoms! They make everything up!`", "Type the following: `No I'm not Elon Musk, I can't make a rocket land by itself.`", "Type the following: `Why are the molecules overreacting?`"]
        rand_science = random.choice(science_work)
        await ctx.send(rand_science)
        message = await self.bot.wait_for('message', check=lambda message : message.author == ctx.author)
        if rand_science == science_work[0]:
          if message.content == "I wonder if waterproof spray can make me walk on water.":
            if id in passive:
              await ctx.send("You have earned 2000 coins!")
              await update_bank(ctx.author, salary-600, "wallet")
            else:
              await ctx.send("You have earned 2200 coins!")
              await update_bank(ctx.author, salary, "wallet")
          else:
            await ctx.send("You can't even type a sentence properly? Dumb")
            return
        elif rand_science == science_work[1]:
          if message.content == "Don't trust atoms! They make everything up!":
            if id in passive:
              await ctx.send("You have earned 2000 coins!")
              await update_bank(ctx.author, salary-600, "wallet")
            else:
              await ctx.send("You have earned 2200 coins!")
              await update_bank(ctx.author, salary, "wallet")
          else:
            await ctx.send("You can't even type a sentence properly? Dumb")
            return
        elif rand_science == science_work[2]:
          if message.content == "No I'm not Elon Musk, I can't make a rocket land by itself.":
            if id in passive:
              await ctx.send("You have earned 2000 coins!")
              await update_bank(ctx.author, salary-600, "wallet")
            else:
              await ctx.send("You have earned 2200 coins!")
              await update_bank(ctx.author, salary, "wallet")
          else:
            await ctx.send("You can't even type a sentence properly?")
            return
        elif rand_science == science_work[3]:
          if message.content == "Why are the molecules overreacting?":
            if id in passive:
              await ctx.send("You have earned 2000 coins!")
              await update_bank(ctx.author, salary-600, "wallet")
            else:
              await ctx.send("You have earned 2200 coins!")
              await update_bank(ctx.author, salary, "wallet")
          else:
            await ctx.send("You can't even type a sentence properly?")
            return  

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after)
            hours = str(cd // 3600)
            minutes = str(cd % 3600 // 60)
            s = str(cd % 3600 % 60)
            embed = discord.Embed(title="Your on a cooldown!", color=discord.Color.blue())
        embed.add_field(name="\u200b",value=f"Slow down will ya?\n Wait for `{self.leadingZero(hours)}hr{self.leadingZero(minutes)}mins`")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def resign(self, ctx):
      id = str(ctx.message.author.id)
      global contract
      #If user is unemployed :laughard:
      if (id not in developer) and (id not in scientist) and (id not in youtuber):
        await ctx.send("How do you resign if you don't have a job?")
        return
      #If the user has a job
      #developer
      if id in developer:
        del developer[id]
        with open('./Jobs/developer.json', 'w+') as f:
          json.dump(developer, f)
        await ctx.send("Congrats! You're unemployed")
      #scientist
      elif id in scientist:
        del scientist[id]
        with open('./Jobs/scientist.json', 'w+') as f:
          json.dump(scientist, f)
          await ctx.send("Congrats! You're unemployed")
      #youtuber
      elif id in youtuber:
        del youtuber[id]
        with open('./Jobs/youtuber.json', 'w+') as f:
          json.dump(youtuber, f)
          await ctx.send("Congrats! You're unemployed")
    
    @resign.error
    async def resign_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Your on a cooldown!", color=discord.Color.blue())
        embed.add_field(
            name="\u200b",
            value=
            f"Slow down will ya?\n Wait for {round(error.retry_after)} seconds"
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def passive(self, ctx):
      id = str(ctx.author.id)
      if id in passive:
        await ctx.send("Are you sure you want to leave passive mode?")
      else:
        await ctx.send("Are you sure you want to join passive mode?")
      message = await self.bot.wait_for('message', check=lambda message : message.author == ctx.author)
      #If no
      if message.content.lower() == "no":
        await ctx.send("Ok, guess not")
        return
        #If yes
      elif message.content.lower() == "yes":
        #Id not in passive
        if id not in passive:
          passive[id] = 1
          await ctx.send("You are now in passive mode.")
          with open("passive.json", "w+") as f:
            json.dump(passive, f)
            #Id in passive
        elif id in passive:
          del passive[id]
          await ctx.send("You're no longer in passive mode")
          with open("passive.json", "w+") as f:
            json.dump(passive, f)

    @passive.error
    async def passive_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Your on a cooldown!", color=discord.Color.blue())
        embed.add_field(
            name="\u200b",
            value=
            f"Slow down will ya?\n Wait for {round(error.retry_after)} seconds"
        )
        await ctx.send(embed=embed)

    """Cooldown related"""

    def leadingZero(self, time: str):
        if len(time) > 1:
            return time

        return "0" + time



def setup(bot):
    bot.add_cog(Economy(bot))
