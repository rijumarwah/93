import discord
from discord.ext import commands
import requests
import json
import praw
import random
import aiohttp
import datetime
import asyncio
import requests
from requests import get
import json
from json import loads
from bs4 import BeautifulSoup


def check(author):
    def inner_check(message):
        return message.author == author

    return inner_check


emoji = ":coin:"
yellow = 0xf7ff8a
gray = 0xc9c9c9


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("./storage/mainbank.json", "w") as f:
        json.dump(users, f)

    return True


async def get_bank_data():
    with open("./storage/mainbank.json", "r") as f:
        users = json.load(f)

    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("./storage/mainbank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]

    return bal


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        usage='<showerthought',
        brief="Returns random shower thoughts"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def showerthought(self, ctx):
        reddit = praw.Reddit(client_id = "D3_kdqla6zxekw",
        client_secret = "E5iQm1WvPLNUEyMy9TfYUPAWewE",
        username = "SK_47DEstROyeR42069",
        password = "uncrackablepassword",
        user_agent = "pythonpraw")
        sub = reddit.subreddit("showerthoughts")
        hot = sub.hot(limit = 50)
        posts = []
        for subs in hot:
            posts.append(subs)
        rand_post = random.choice(posts)
        name = rand_post.title 

        embed = discord.Embed(
        )
        embed.add_field(name="Shower thoughts", value=name)
        await ctx.send(embed= embed)


    @commands.command(
        usage='<trivia',
        brief="Cool trivia questions"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def trivia(self, ctx):

        urls = ["https://opentdb.com/api.php?amount=1&difficulty=easy&type=multiple", "https://opentdb.com/api.php?amount=1&difficulty=medium&type=multiple"]

        url = random.choice(urls)

        response = requests.request("GET", url).json()

        results = response['results'][0]

        correct = str(results['correct_answer'])
        correct = correct.replace("&quot;", "'")
        incorrect_a = str(results['incorrect_answers'][0])
        incorrect_a = incorrect_a.replace("&quot;", "'")
        incorrect_b = str(results['incorrect_answers'][1])
        incorrect_b = incorrect_b.replace("&quot;", "'")
        incorrect_c = str(results['incorrect_answers'][2])
        incorrect_c = incorrect_c.replace("&quot;", "'")

        options = [correct, incorrect_a, incorrect_b, incorrect_c]

        shuffled = random.sample(options, len(options))

        category = results['category']
        diff = str(results['difficulty'])
        diff = diff.capitalize()
        ques = str(results['question'])
        ques = ques.replace("&quot;", "'")
        ques = ques.replace("&#039;", "'")

        desc = f" :small_orange_diamond: a) {shuffled[0]}\n:small_orange_diamond:  b) {shuffled[1]}\n:small_orange_diamond:  c) {shuffled[2]}\n:small_orange_diamond:  d) {shuffled[3]}"

        em = discord.Embed(title=f":question: {ctx.author.display_name}'s trivia question", description=f"{ques}\n\n{desc}\n\nType your choice (a, b, c or d)\n")

        em.add_field(name="Category", value=f"{category}")
        em.add_field(name="Difficulty", value=f"{diff}")
        em.set_footer(text="You have 20 seconds to answer")

        await ctx.send(embed=em)

        try:
            ida = await self.client.wait_for('message', check=check(ctx.author), timeout=20)
            choice = str(ida.content)
            choice = choice.lower()

            if choice == "a":
                chosen = shuffled[0]

            elif choice == "b":
                chosen = shuffled[1]

            elif choice == "c":
                chosen = shuffled[2]

            elif choice == "d":
                chosen = shuffled[3]

            else:
                chosen = "dummy"

            yup = ['You got it!', 'Correct!', 'Yup, you got it', "That's right!"]
            nope = ["That's not right!", "Nope!", "Bruh,", "Oops!"]

            if chosen == correct:
                await ctx.send(f"✅ {random.choice(yup)}")
            else:
                await ctx.send(f"❌ {random.choice(nope)} It was: **{correct}**")

        except asyncio.TimeoutError:
            await ctx.send(f":clock10: Too slow! Your time is up. The answer was: **{correct}**")


    @commands.command(
        usage='<animetrivia',
        brief="Anime trivia questions"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def animetrivia(self, ctx):

        url = "https://opentdb.com/api.php?amount=1&category=31&type=multiple"

        response = requests.request("GET", url).json()

        results = response['results'][0]

        correct = str(results['correct_answer'])
        correct = correct.replace("&quot;", "'")
        incorrect_a = str(results['incorrect_answers'][0])
        incorrect_a = incorrect_a.replace("&quot;", "'")
        incorrect_b = str(results['incorrect_answers'][1])
        incorrect_b = incorrect_b.replace("&quot;", "'")
        incorrect_c = str(results['incorrect_answers'][2])
        incorrect_c = incorrect_c.replace("&quot;", "'")

        options = [correct, incorrect_a, incorrect_b, incorrect_c]

        shuffled = random.sample(options, len(options))

        category = results['category']
        diff = str(results['difficulty'])
        diff = diff.capitalize()
        ques = str(results['question'])
        ques = ques.replace("&quot;", "'")
        ques = ques.replace("&#039;", "'")

        desc = f"<:1382_dot:772666700117573652> a) {shuffled[0]}\n<:1382_dot:772666700117573652> b) {shuffled[1]}\n<:1382_dot:772666700117573652> c) {shuffled[2]}\n<:1382_dot:772666700117573652> d) {shuffled[3]}"

        em = discord.Embed(title=f":cherry_blossom: {ctx.author.display_name}'s trivia question", description=f"{ques}\n\n{desc}\n\nType your choice (a, b, c or d)\n")

        em.add_field(name="Category", value=f"{category}")
        em.add_field(name="Difficulty", value=f"{diff}")
        em.set_footer(text="You have 20 seconds to answer")

        await ctx.send(embed=em)

        try:
            ida = await self.client.wait_for('message', check=check(ctx.author), timeout=20)
            choice = str(ida.content)
            choice = choice.lower()

            if choice == "a":
                chosen = shuffled[0]

            elif choice == "b":
                chosen = shuffled[1]

            elif choice == "c":
                chosen = shuffled[2]

            elif choice == "d":
                chosen = shuffled[3]

            else:
                chosen = "dummy"

            yup = ['You got it!', 'Correct!', 'Yup, you got it', "That's right!"]
            nope = ["That's not right!", "Nope!", "Bruh,", "Oops!"]

            if chosen == correct:
                await ctx.send(f"✅ {random.choice(yup)}")
            else:
                await ctx.send(f"❌ {random.choice(nope)} It was: **{correct}**")

        except asyncio.TimeoutError:
            await ctx.send(f":clock10: Too slow! Your time is up. The answer was: **{correct}**")


    @commands.command(
        aliases=['8ball'],
        usage='<8ball [question]',
        brief="Returns random responses"
    )
    async def eball(self, ctx, *, question):
        responses = ['Absolutely.',
                    'Definitely not.',
                    'It is certain.',
                    'Not at all.',
                    'My sources say no',
                    'Not sure',
                    'Yeah',
                    'Very doubtful',
                    "Don't count on it",
                    'Outlook not so good',
                    'Most likely',
                    'Without a doubt',
                    "That's for sure",
                    'As I see it, yes',
                    'Yup',
                    'Yeah lol',
                    "Lmao yeah",
                    'Why not',
                    "Yes, but actually no.",
                    "Yes and no.",
                    "No",
                    "Nah",
                    "Sure",
                    ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    

    @commands.command(
        usage='<rps [rock/paper/scissors]',
        brief="Play rock, paper, scissors"
    )
    async def rps(self, ctx, arg=None):

        if not arg:
            await ctx.send(f"You didn't tell me what you chose, valid choices: `rock`, `paper`, `scissors`")
            return

        rpschoice = [
            "rock",
            "paper",
            "scissors",
        ]

        if arg not in rpschoice:
            await ctx.send(f"Invalid choice, valid choices: `rock`, `paper`, `scissors`")
            return

        choicebot = random.choice(rpschoice)

        if choicebot == "rock":
            emoji = "<:rock:783941279771262986>"
        elif choicebot == "paper":
            emoji = "<:paper:783941281285799958>"
        else:
            emoji = "<:scissors:783941282019934219>"

        if arg == "rock":

            if choicebot == "rock":
                await ctx.send(f"{emoji} I chose: {choicebot}, Tie!")
            elif choicebot == "paper":
                await ctx.send(f"{emoji} I chose: {choicebot}, I win!")
            else:
                await ctx.send(f"{emoji} I chose: {choicebot}, You win!")
        elif arg == "paper":

            if choicebot == "rock":
                await ctx.send(f"{emoji} I chose: {choicebot}, You win!")
            elif choicebot == "paper":
                await ctx.send(f"{emoji} I chose: {choicebot}, Tie")
            else:
                await ctx.send(f"{emoji} I chose: {choicebot}, I win!")
        elif arg == "scissors":

            if choicebot == "rock":
                await ctx.send(f"{emoji} I chose: {choicebot}, I win!")
            elif choicebot == "paper":
                await ctx.send(f"{emoji} I chose: {choicebot}, You win!")
            else:
                await ctx.send(f"{emoji} I chose: {choicebot}, Tie!")



    @commands.command(
        usage='<reddit [subreddit]',
        brief="Fetches random posts from sub"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def reddit(self, ctx, sub):
        url = f"https://api.ksoft.si/images/rand-reddit/{sub}"

        headers = {
            'Authorization': 'Bearer 93975db5189747204706b9186e267adaa689e865',
        }

        para = {
            'remove_nsfw': True,
            'span': 'day',
        }

        response = requests.request("GET", url, headers=headers, params=para).json()

        try:
            em = discord.Embed(title=f"{response['title']}", url=f"{response['source']}"

                            )

            em.set_image(url=f"{response['image_url']}")

            em.set_footer(text=f"{response['upvotes']} 👍 ・ {response['author']}")

            await ctx.send(embed=em)

        except:
            embed = discord.Embed(
                description=f"**{ctx.author}** Unable to get posts, make sure the subreddit exists and it isn't NSFW",
                )
            await ctx.send(embed=embed)


    @commands.command(
        usage='<fml',
        brief="F*ck my life posts from reddit"
    )
    async def fml(self, ctx):
        url = "https://api.alexflipnote.dev/fml"

        head = {
            'Authorization': 'j0EturyFQ8WPB5JHfzb2B0LyNVZQ0T7Rod9GRVoh',
        }

        r = requests.request('GET', url, headers=head).json()

        await ctx.send(f"{r['text']}")

        
    @commands.command(
        usage='<irc',
        brief="Bash IRC chats"
    )
    async def irc(self, ctx):
        url = "http://bash.org/?random1"
        page = requests.get(url)
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            q = soup.find('p', class_='qt').text
            await ctx.send(f"```{q}\n\nbash.org```")
        except:
            await ctx.send("API error")
            
            
    @commands.command(
        aliases=['neverhaveiever'],
        usage='<nhie',
        brief="Returns random nhie questions"
    )
    async def nhie(self, ctx):
        url = "https://never-have-i-ever-online.com/"
    
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            quote = soup.find('span', id='ajaxQuestion').text
    
            em = discord.Embed(
                description=f"Never have I ever {quote}"
            )
    
            await ctx.send(embed=em)
    
        except:
            await ctx.send("API error")

    
    @commands.command(
        aliases=['$', 'bal'],
        usage='<balance [member/none]',
        brief='Returns user balance'
    )
    async def balance(self, ctx, member: discord.Member=None):
        await open_account(ctx.author)

        users = await get_bank_data()

        if not member:
            user = ctx.author
        else:
            user = member

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        embed = discord.Embed(
            description=f"**{user}** has {round(wallet_amt)} coins in their wallet and {round(bank_amt)} coins in the bank",
            colour=yellow)
        await ctx.send(embed=embed)


    @commands.command(
        usage='<beg',
        brief='Adds random amounts to account'
    )
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        earnings = random.randrange(101)

        users[str(user.id)]["wallet"] += earnings

        embed = discord.Embed(
            description=f"**{ctx.author}** You begged and got {earnings} coins. You can beg once every 15 minutes",
            color=gray)
        await ctx.send(embed=embed)

        with open("./storage/mainbank.json", "w") as f:
            json.dump(users, f)


    @commands.command(
        usage='<timely',
        brief='Collects timely reward'
    )
    @commands.cooldown(1, 10800, commands.BucketType.user)
    async def timely(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        earnings_timely = 500

        users[str(user.id)]["wallet"] += earnings_timely

        embed = discord.Embed(
            description=f"**{ctx.author}** You collected your timely reward of 500 coins. Come back after 3 hours.",
            color=yellow)
        await ctx.send(embed=embed)

        with open("./storage/mainbank.json", "w") as f:
            json.dump(users, f)


    @commands.command(
        aliases=['w', 'with'],
        usage='<withdraw [amount]',
        brief='Withdraw amount from bank'
    )
    async def withdraw(self, ctx, amount=None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("Please enter an amount to withdraw")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send("You don't have enough money")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")

        embed = discord.Embed(
            description=f"**{ctx.author}** You withdrew {amount} coins from your bank account",
            color=gray)
        await ctx.send(embed=embed)


    @commands.command(
        aliases=['d', 'dep'],
        usage='<deposit [amount]',
        brief='Deposit amount to bank'
    )
    async def deposit(self, ctx, amount: str=None):
        await open_account(ctx.author)
        users = await get_bank_data()
        wallet_amt = users[str(ctx.author.id)]["wallet"]
        if amount == None:
            await ctx.send("Please enter an amount")
            return

        if amount == "all" or amount == "All":
            amount = wallet_amt

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[0]:
            await ctx.send("You don't have that much money")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return

        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, "bank")

        embed = discord.Embed(description=f"You deposited {amount} coins to your bank",
                              color=gray)
        await ctx.send(embed=embed)


    @commands.command(
        aliases=['s'],
        usage='<send [member] [amount]',
        brief='Send amount to a user'
    )
    async def send(self, ctx, member: discord.Member=None, amount=None):
        if not member:
            return await ctx.send("No member parameter given")

        await open_account(ctx.author)
        await open_account(member)
        if amount == None:
            await ctx.send("Please enter an amount")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send("You don't have enough money!")
            return
        if amount < 0:
            await ctx.send("amount must be positive!")
            return

        await update_bank(ctx.author, -1 * amount, "bank")
        await update_bank(member, amount, "bank")

        embed = discord.Embed(
            description=f"**{ctx.author}** You gave **{member.mention}** {amount} coins",
            color=yellow)

        await ctx.send(embed=embed)


    @commands.command(
        aliases=["bflip"],
        usage='<betflip [amount] [h/t]',
        brief='Bet flip a coin'
    )
    async def betflip(self, ctx, amt: int, choice: str):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        wallet_amt = users[str(user.id)]["wallet"]

        if amt <= 0:
            await ctx.send(f"Please choose a great amount!")

        elif amt > wallet_amt:
            await ctx.send(f"You don't have enough money in your wallet!")

        else:
            ch = [
                'h', 't', ]

            bot_ch = random.choice(ch)

            if choice == "h":
                if bot_ch == "h":
                    embed = discord.Embed(
                        description=f"**{ctx.author}** You guessed it right! You win {amt * 2} coins",
                        color=yellow,
                    )
                    embed.set_image(url='https://i.imgur.com/zCRK8FG.png')
                    await ctx.send(embed=embed)
                    await update_bank(ctx.author, amt)

                else:
                    embed = discord.Embed(
                        description=f"**{ctx.author}** You lost {amt} coins better luck next time ^_^",
                        color=gray)
                    embed.set_image(url='https://i.imgur.com/eG2XLck.png')
                    await ctx.send(embed=embed)
                    await update_bank(ctx.author, -1 * amt)

            elif choice == "t":
                if bot_ch == "t":
                    embed = discord.Embed(
                        description=f"**{ctx.author}** You guessed it right! You win {amt * 2} coins",
                        color=yellow)
                    embed.set_image(url='https://i.imgur.com/eG2XLck.png')
                    await ctx.send(embed=embed)
                    await update_bank(ctx.author, amt)
                else:
                    embed = discord.Embed(
                        description=f"**{ctx.author}** You lost {amt} coins better luck next time ^_^",
                        color=gray)
                    embed.set_image(url='https://i.imgur.com/zCRK8FG.png')
                    await ctx.send(embed=embed)
                    await update_bank(ctx.author, -1 * amt)

            else:
                embed = discord.Embed(
                    description=f"**{ctx.author}** Usage: <bf <amt> <h/t>",
                    color=gray)
                await ctx.send(embed=embed)


    @commands.command(
        aliases=['br', 'broll'],
        usage='<betroll [amount]',
        brief='Bet roll an amount'
    )
    async def betroll(self, ctx, amt: int=None):

        if not amt:
            return await ctx.send("No amount given to roll")

        ch = ['↘️', '↙️', '↖️', '↗️', '⬇️', '⬆️', '➡️', '⬅️']

        ran_ch = random.choice(ch)

        msg = f"""**[ 0.7 ] ‎  [ 1.2 ]‎  ‎ [ 1.7 ]**\n\n**[ 0.2]**   ‎ ‎‎‎ ‎ {ran_ch}  ‎‎‎‎ ‎‎‎  **[ 0.9 ]**\n\n**[ 1.2 ]  ‎  [ 0.5 ]  ‎ [ 1.3 ]**"""

        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        wallet_amt = users[str(user.id)]["wallet"]

        if amt <= 0:
            await ctx.send(f"Please choose a greater amount")

        elif amt > wallet_amt:
            await ctx.send(f"You don't have enough money in your wallet")

        else:
            amt = round(amt)
            if ran_ch == ch[0]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 1.3 * amt)
                winning = 1.3 * amt
            elif ran_ch == ch[1]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 1.2 * amt)
                winning = 1.2 * amt
            elif ran_ch == ch[2]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 0.7 * amt)
                winning = 0.7 * amt
            elif ran_ch == ch[3]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 1.7 * amt)
                winning = 1.7 * amt
            elif ran_ch == ch[4]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 0.5 * amt)
                winning = 0.5 * amt
            elif ran_ch == ch[5]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 1.2 * amt)
                winning = 1.2 * amt
            elif ran_ch == ch[6]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 0.9 * amt)
                winning = 0.9 * amt
            elif ran_ch == ch[7]:
                await update_bank(ctx.author, -1 * amt)
                await update_bank(ctx.author, 0.2 * amt)
                winning = 0.2 * amt

            em = discord.Embed(
                title=f"{ctx.author} won {winning} coins", description=msg, color=yellow
            )

            await ctx.send(embed=em)


    @commands.command(
        aliases=["lb"],
        usage='<leaderboard',
        brief='Returns the global economy leaderboard'
    )
    async def leaderboard(self, ctx, x=9):
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)

        em = discord.Embed(title=f"Global Leaderboard")
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.client.get_user(id_)
            name = member.name
            em.add_field(name=f"{index}. {name}", value=f"{amt} :coin:", inline=True)
            if index == x:
                break
            else:
                index += 1

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Fun(client))
