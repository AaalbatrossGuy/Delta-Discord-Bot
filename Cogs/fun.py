# Coding=UTF8
# !python3
# /usr/bin/env python3

import discord, random, requests
from discord.ext import commands
import aiohttp, io

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.command(name="predict")
    async def predict(self, ctx, *, question:str):
        responses = [
            "yes", "ok", "i don't know", "no", "absolutely not"
        ]

        await ctx.channel.send(f"{random.random(responses)}")

    @commands.command(name='ytcomm')
    async def youtube_comment_fake(self, ctx, username: discord.Member, *, comment):
        avatar = username.avatar_url_as(format='png')
        # str(username).split('#')[0] strip the discriminator
        comment = comment.replace(" ", "+")
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/youtube-comment?username={str(username).split("#")[0]}&comment={comment}&avatar={avatar}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "ytcomment.png")
                    em = discord.Embed(
                        title="Nice Comment ;)",
                        color=discord.Color.dark_red(),
                    )
                    em.set_image(url="attachment://ytcomment.png")
                    await ctx.send(embed=em, file=file)
                    
                else:
                    await ctx.send('Oops! An error occured. Please Try Again Later.')
                await session.close()

    @commands.command(name="twt")
    async def tweet_fake(self, ctx, username: discord.Member, *, comment):
        avatar = username.avatar_url_as(format='png')
        comment = comment.replace(" ", "+")
        if username.nick == None : nick_name = str(username).split("#")[0]
        else: nick_name = username.nick
        #url = "https://some-random-api.ml/canvas/tweet?avatar=https://cdn.discordapp.com/avatars/560789882738573324/bc220b0eeeabbe234026e4881f3c3b9c.png&username=Telk&displayname=TAl&comment=Hello"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/tweet?avatar={avatar}&username={str(username).split("#")[0]}&displayname={nick_name}&comment={comment}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "tweet.png")
                    em = discord.Embed(
                        title="Nice Tweet ;)",
                        color=discord.Color.dark_red(),
                    )
                    em.set_image(url="attachment://tweet.png")
                    await ctx.send(embed=em, file=file)
                    
                else:
                    await ctx.send('Oops! An error occured. Please Try Again Later.')
                await session.close()

def setup(client):
    client.add_cog(Fun(client))