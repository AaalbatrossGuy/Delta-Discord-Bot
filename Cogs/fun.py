# Coding=UTF8
# !python3
# /usr/bin/env python3

import discord, random, requests
from discord.ext import commands, tasks
import aiohttp, io, asyncio, asyncpraw
from discord_components import DiscordComponents, Select, SelectOption
from datetime import timedelta
from decouple import config


Reddit = asyncpraw.Reddit(client_id=f"{config('REDDIT_CLIENTID')}", client_secret=f"{config('REDDIT_SECRET')}", username=f"{config('REDDIT_USERNAME')}", password=f"{config('REDDIT_PASSWORD')}", user_agent="pythonpraw")
meme = []
futurology = []
pshop = []
wallpaper = []


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def get_memes():
        sub = await Reddit.subreddit("memes")
        top = sub.top(limit=300)
        hot = sub.hot(limit=300)
        new = sub.new(limit=300)
        async for submissions in random.choice([top, hot, new]):
            meme.append(submissions) 
        print('get_memes completed')
        #print(meme)
    
    async def get_futurology():
        sub = await Reddit.subreddit("Futurology")
        top = sub.top(limit=300)
        hot = sub.hot(limit=300)
        new = sub.new(limit=300)
        async for submissions in random.choice([top, hot, new]):
            futurology.append(submissions)
        print('get_futurology completed')


    async def get_pshop():
        sub = await Reddit.subreddit("photoshopbattles")
        top = sub.top(limit=300)
        hot = sub.hot(limit=300)
        new = sub.new(limit=300)
        async for submissions in random.choice([top, hot, new]):
            pshop.append(submissions)
        print('get_pshop completed')

    async def get_wallpaper():
        sub = await Reddit.subreddit("wallpaper")
        top = sub.top(limit=300)
        hot = sub.hot(limit=300)
        new = sub.new(limit=300)
        async for submissions in random.choice([top, hot, new]):
            wallpaper.append(submissions)
        print('get_wallpaper completed')


    @staticmethod 
    @tasks.loop(minutes=30)
    async def get_posts():
        print('getpost')
        #print(Fun.meme)
        await Fun.get_memes()
        await Fun.get_futurology()
        await Fun.get_pshop()
        await Fun.get_wallpaper()
        #print(meme)

    @commands.command(name='ytcomm')
    async def youtube_comment_fake(self, ctx, username: discord.Member, *, comment):
        avatar = username.avatar_url_as(format='png')
        # str(username).split('#')[0] strip the discriminator
        comment = comment.replace(" ", "+")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://some-random-api.ml/canvas/youtube-comment?username={str(username).split("#")[0]}&comment={comment}&avatar={avatar}'
                    ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "ytcomment.png")
                    em = discord.Embed(
                        title="Nice Comment ;)",
                        color=discord.Color.dark_red(),
                    )
                    em.set_image(url="attachment://ytcomment.png")
                    await ctx.reply(embed=em, file=file, mention_author=False)

                else:
                    await ctx.reply('Oops! An error occured. Please Try Again Later.')
                await session.close()

    @commands.command(name="twt")
    async def tweet_fake(self, ctx, username: discord.Member, *, comment):
        avatar = username.avatar_url_as(format='png')
        comment = comment.replace(" ", "+")
        if username.nick == None:
            nick_name = str(username).split("#")[0]
        else:
            nick_name = username.nick
        # url = "https://some-random-api.ml/canvas/tweet?avatar=https://cdn.discordapp.com/avatars/560789882738573324/bc220b0eeeabbe234026e4881f3c3b9c.png&username=Telk&displayname=TAl&comment=Hello"

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://some-random-api.ml/canvas/tweet?avatar={avatar}&username={str(username).split("#")[0]}&displayname={nick_name}&comment={comment}'
                    ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "tweet.png")
                    em = discord.Embed(
                        title="Nice Tweet ;)",
                        color=discord.Color.dark_red(),
                    )
                    em.set_image(url="attachment://tweet.png")
                    await ctx.reply(embed=em, file=file, mention_author=False)

                else:
                    await ctx.reply('Oops! An error occured. Please Try Again Later.')
                await session.close()

    @commands.command(name="pet")
    async def petpat(self, ctx, *, username: discord.Member = None):
        username = username or ctx.author
        avatar = username.avatar_url_as(format='png')
        url = f"https://some-random-api.ml/premium/petpet?avatar={avatar}&key=KdRrQKvpk35OfxNGIm997pEvC"
        # print(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "petpat.gif")
                    await ctx.reply(file=file, mention_author=False)

                else:
                    await ctx.reply('Oops! An error occured. Please Try Again Later.')
                    await session.close()

    @commands.command(name="fact")
    async def animal_facts(self, ctx):
        embed = discord.Embed(title="<a:panda:871255104735567912> Animal Facts", timestamp=ctx.message.created_at,
                              color=discord.Color.dark_orange(),
                              description="Click on the drop down menu and select what fact do you want to know.")
        embed.set_thumbnail(url='https://media.wired.com/photos/593261cab8eb31692072f129/master/pass/85120553.jpg')
        embed.set_author(name="Love animals",
                         icon_url='https://cdn.discordapp.com/attachments/831369746855362590/831369994474094622/Logo.jpg')

        urlPanda = "https://some-random-api.ml/animal/panda"
        responsePanda = requests.request("GET", url=urlPanda)
        dataPanda = responsePanda.json()
        imagePanda = dataPanda['image']
        factPanda = dataPanda['fact']

        embedPanda = discord.Embed(title="A Panda Fact", timestamp=ctx.message.created_at,
                                   color=discord.Color.dark_theme(), description=factPanda)
        embedPanda.set_footer(text='Delta Δ is the fourth letter of the Greek Alphabet', icon_url=ctx.author.avatar_url)
        embedPanda.set_image(url=imagePanda)

        urlDog = "https://some-random-api.ml/animal/dog"
        responseDog = requests.request("GET", url=urlDog)
        imageDog = responseDog.json()['image']
        factDog = responseDog.json()['fact']

        embedDog = discord.Embed(title="A Dog Fact", timestamp=ctx.message.created_at, color=discord.Color.dark_grey(),
                                 description=factDog)
        embedDog.set_footer(text="Delta Δ is the fourth letter of the Greek Alphabet", icon_url=ctx.author.avatar_url)
        embedDog.set_image(url=imageDog)

        urlFox = "https://some-random-api.ml/animal/fox"
        responseFox = requests.request("GET", url=urlFox)
        imageFox = responseFox.json()['image']
        factFox = responseFox.json()['fact']

        embedFox = discord.Embed(title="A Fox Fact", timestamp=ctx.message.created_at, color=discord.Color.dark_blue(),
                                 description=factFox)
        embedFox.set_footer(text="Delta Δ is the fourth letter of the Greek Alphabet", icon_url=ctx.author.avatar_url)
        embedFox.set_image(url=imageFox)

        urlKoala = "https://some-random-api.ml/animal/koala"
        responseKoala = requests.request("GET", url=urlKoala)
        imageKoala = responseKoala.json()['image']
        factKoala = responseKoala.json()['fact']

        embedKoala = discord.Embed(title="A Koala Fact", timestamp=ctx.message.created_at,
                                   color=discord.Color.dark_gold(), description=factKoala)
        embedKoala.set_footer(text="Delta Δ is the fourth letter of the Greek Alphabet", icon_url=ctx.author.avatar_url)
        embedKoala.set_image(url=imageKoala)

        urlBird = "https://some-random-api.ml/animal/birb"
        responseBird = requests.request("GET", url=urlBird)
        imageBird = responseBird.json()['image']
        factBird = responseBird.json()['fact']

        embedBird = discord.Embed(title="A Bird Fact", timestamp=ctx.message.created_at,
                                  color=discord.Color.dark_purple(), description=factBird)
        embedBird.set_footer(text='Delta Δ is the fourth letter of the Greek Alphabet', icon_url=ctx.author.avatar_url)
        embedBird.set_image(url=imageBird)

        tdelta = ctx.message.created_at + timedelta(minutes=1)

        await ctx.reply(embed=embed, components=[
            Select(
                placeholder="Select a Fact Category",
                min_values=1,
                options=[
                    SelectOption(label="🐼 Panda", value="panda"),
                    SelectOption(label="🐶 Dog", value="dog"),
                    SelectOption(label="🦊 Fox", value="fox"),
                    SelectOption(label="🐨 Koala", value="koala"),
                    SelectOption(label="🐦 Bird", value="bird")
                ],
            ),
        ])

        interaction = await self.client.wait_for("select_option", timeout=60)
        if interaction.author.id == ctx.author.id and interaction.message.embeds[0].timestamp < tdelta:
            check_for = interaction.values[0]
            if check_for.lower() == 'panda':
                await interaction.respond(embed=embedPanda, ephemeral=False)
            elif check_for.lower() == 'dog':
                await interaction.respond(embed=embedDog, ephemeral=False)
            elif check_for.lower() == 'fox':
                await interaction.respond(embed=embedFox, ephemeral=False)
            elif check_for.lower() == 'koala':
                await interaction.respond(embed=embedKoala, ephemeral=False)
            elif check_for.lower() == 'bird':
                await interaction.respond(embed=embedBird, ephemeral=False)
                
   @commands.command(name="r_memes")
    async def reddit_memes(self, ctx):
        randompost = random.choice(meme)
       # meme.append(randompost)
        #print(randompost)
        name = randompost.title if len(randompost.title)<34 else f"{randompost.title[:34]}..."
        base_img = randompost.url 
        img = randompost.url
        #print(f"before - {img}")
        if not img.endswith('.jpg') and not img.endswith('.png') and not img.endswith('.jpeg'):
            #print('executed')
            img = 'https://cdn.discordapp.com/attachments/907133573172170833/907975316859920394/noimage.png'
        elif base_img.endswith('.jpeg') or base_img.endswith('.png') or base_img.endswith('.jpg'):
            img = randompost.url
        link = randompost.permalink
        comments = randompost.num_comments
        likes = randompost.score
        embed=discord.Embed(title=f"<:reddit:870239682775121980> {name}", color=ctx.author.color, timestamp=ctx.message.created_at, url=f"https://reddit.com{link}")
        embed.set_image(url=img)
        embed.set_footer(text=f"👍 {likes} 💬 {comments}")
        #embed.set_thumbnail(url="https://sm.mashable.com/mashable_in/news/r/reddit-is-/reddit-is-secretly-exploring-a-clubhouse-like-voice-chat-fea_nqpz.jpg")
        await ctx.channel.send(embed=embed)
        #print(len(meme))
        
    @commands.command(name="r_futurology")
    async def reddit_futurology(self, ctx):
        randompost = random.choice(futurology)
        name = randompost.title
        base_img = randompost.url 
        img = randompost.url
        #print(f"before - {img}")
        if not img.endswith('.jpg') and not img.endswith('.png') and not img.endswith('.jpeg'):
            #print('executed')
            img = 'https://cdn.discordapp.com/attachments/907133573172170833/907975316859920394/noimage.png'
        elif base_img.endswith('.jpeg') or base_img.endswith('.png') or base_img.endswith('.jpg'):
            img = randompost.url
            #print(f"after - {img}")
        link = randompost.permalink
        comments = randompost.num_comments
        likes = randompost.score
        embed=discord.Embed(title=f"<:reddit:870239682775121980> {name}", color=ctx.author.color, timestamp=ctx.message.created_at, url=f"https://reddit.com{link}")
        embed.set_image(url=img)
        embed.set_footer(text=f"👍 {likes} 💬 {comments}")
        #embed.set_thumbnail(url="https://sm.mashable.com/mashable_in/news/r/reddit-is-/reddit-is-secretly-exploring-a-clubhouse-like-voice-chat-fea_nqpz.jpg")
        await ctx.channel.send(embed=embed)
        #print(len(futurology))

    @commands.command(name="r_pshop")
    async def reddit_pshop(self, ctx):
        randompost = random.choice(pshop)
        name = randompost.title
        base_img = randompost.url 
        img = randompost.url
        #print(type(img))
        #print(f"before - {img}")
        if not img.endswith('.jpg') and not img.endswith('.png') and not img.endswith('.jpeg'):
            #print('executed')
            img = 'https://cdn.discordapp.com/attachments/907133573172170833/907975316859920394/noimage.png'
        elif base_img.endswith('jpeg') or base_img.endswith('png') or base_img.endswith('jpg'):
             #print('else executed')
             img = randompost.url
             #print(f"after - {img}")
        link = randompost.permalink
        comments = randompost.num_comments
        likes = randompost.score
        embed=discord.Embed(title=f"<:reddit:870239682775121980> {name}", color=ctx.author.color, timestamp=ctx.message.created_at, url=f"https://reddit.com{link}")
        embed.set_image(url=img)
        embed.set_footer(text=f"👍 {likes} 💬 {comments}")
        #embed.set_thumbnail(url="https://sm.mashable.com/mashable_in/news/r/reddit-is-/reddit-is-secretly-exploring-a-clubhouse-like-voice-chat-fea_nqpz.jpg")
        await ctx.channel.send(embed=embed)

    @commands.command(name="r_wallpaper")
    async def reddit_wallpaper(self, ctx):
        randompost = random.choice(wallpaper)
        name = randompost.title
        base_img = randompost.url 
        img = randompost.url
        #print(type(img))
        #print(f"before - {img}")
        if not img.endswith('.jpg') and not img.endswith('.png') and not img.endswith('.jpeg'):
            #print('executed')
            img = 'https://cdn.discordapp.com/attachments/907133573172170833/907975316859920394/noimage.png'
        elif base_img.endswith('jpeg') or base_img.endswith('png') or base_img.endswith('jpg'):
             #print('else executed')
             img = randompost.url
             #print(f"after - {img}")
        link = randompost.permalink
        comments = randompost.num_comments
        likes = randompost.score
        embed=discord.Embed(title=f"<:reddit:870239682775121980> {name}", color=ctx.author.color, timestamp=ctx.message.created_at, url=f"https://reddit.com{link}")
        embed.set_image(url=img)
        embed.set_footer(text=f"👍 {likes} 💬 {comments}")
        #embed.set_thumbnail(url="https://sm.mashable.com/mashable_in/news/r/reddit-is-/reddit-is-secretly-exploring-a-clubhouse-like-voice-chat-fea_nqpz.jpg")
        await ctx.channel.send(embed=embed)

    # Error Handlers
    @youtube_comment_fake.error
    async def yt_fake_error_handling(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="<:hellno:871582891585437759> Missing Arguments",
                                  description="```ini\nMake sure you have run the command providing the [username]* and the [comment]```",
                                  timestamp=ctx.message.created_at, color=discord.Color.dark_grey())
            embed.set_footer(
                text="*Usernames mustn't contain spaces if they are typed instead of pinging or using id's",
                icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title="<:hellno:871582891585437759> Member Not Found",
                                  description="```ini\nMake sure you have run the command providing the [username]* and the [comment]```",
                                  timestamp=ctx.message.created_at, color=discord.Color.dark_grey())
            embed.set_footer(
                text="*Usernames mustn't contain spaces if they are typed instead of pinging or using id's",
                icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @tweet_fake.error
    async def tweet_fake_error_handling(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="<:hellno:871582891585437759> Missing Arguments",
                                  description="```ini\nMake sure you have run the command providing the [username]* and the [comment]```",
                                  timestamp=ctx.message.created_at, color=discord.Color.dark_grey())
            embed.set_footer(
                text="*Usernames mustn't contain spaces if they are typed instead of pinging or using id's",
                icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title="<:hellno:871582891585437759> Member Not Found",
                                  description="```ini\nMake sure you have run the command providing the [username]* and the [comment]```",
                                  timestamp=ctx.message.created_at, color=discord.Color.dark_grey())
            embed.set_footer(
                text="*Usernames mustn't contain spaces if they are typed instead of pinging or using id's",
                icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @petpat.error
    async def petpat_error_handling(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=discord.Embed(title="<:hellno:871582891585437759> Member Not Found",
                                               description="```ini\nMake sure you have run the command providing the [username]```",
                                               timestamp=ctx.message.created_at, color=discord.Color.dark_teal()))


def setup(client):
    Fun.get_posts().start()
    DiscordComponents(client)
    client.add_cog(Fun(client))
