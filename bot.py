import asyncio
import gogo_scraper
import discord
from discord.ext import commands
import redis
from discord.ext import tasks
import os

from dotenv import load_dotenv

load_dotenv()
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

# redis_server = redis.Redis()
# AUTH_TOKEN = str(redis_server.get('AUTH_TOKEN').decode('utf-8'))

bot = commands.Bot(command_prefix='!')

BASE_URL = 'https://gogoanime.so/'  # Change this if this link to gogoanime goes down

tasks = {}


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='ping', help='Outputs ping to bot. Mainly used to check whether bot is live')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms ')


@bot.command(name='findAnime', help='Find anime based on search query')
async def findAnime(ctx, anime_name: str, base_url: str = BASE_URL):
    search = gogo_scraper.search(anime_name, base_url)

    if (search is None) or (len(search) == 0):
        await ctx.send(f'Could not find anything.')
        return

    for res in search:
        anime = res
        output = f'''\n

                    Here is an anime I found:\n
                    Title: {anime['name']}
                    Released: {anime['released']}
                    link: {anime['link']}
                '''
        await ctx.send(output)

        await ctx.send('\nIs this the right anime? (Type "yes" to stop command, everything else shows the next result)')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        msg = str(msg.content).lower()

        if msg == 'yes' or msg == 'yeah' or msg == 'yup':
            break
        else:
            await ctx.send('Showing next result...')


@bot.command(name='latestEpisode', help='Get Latest episode of input anime. Please input the exact name'
                                        'which could be found using the "findAnime" command')
async def showLatestEpisode(ctx, anime: str, base_url: str = BASE_URL):
    latest = gogo_scraper.getLastEpisode(anime, base_url)
    latest_ep = latest['num']

    output = f'''\n
                Latest episode: \n
                Episode number: {latest_ep}
                Episode link: {latest["link"]}
                
            '''
    await ctx.send(output)


@bot.command(name='getEpisode', help='Find whether a given episode is available. Please input the exact name'
                                     'which could be found using the "findAnime" command')
async def whetherEpisodeAvailable(ctx, anime: str, ep_num: int, base_url: str = BASE_URL):
    episode = gogo_scraper.getEpisode(anime, ep_num, base_url)

    if episode is not None:
        await ctx.send(f'I was able to find the episode: {episode}')
    else:
        await ctx.send(f'Episode could not be found')


# This assumes that the incoming "anime" is a valid anime
# Task function that is used to check for new episodes of an anime
async def checkForNewEpisode(ctx, anime, ep, timeout, channel):
    try:
        while True:
            episode = gogo_scraper.getEpisode(anime, ep)
            if episode is not None:
                output = f'''\n
                        New episode of {anime} has been released \n
                        Episode number: {ep}
                        Link: {episode['link']}
                        '''
                await channel.send(output)
                print(f'New episode has been found for {anime}')
                ep += 1
            else:
                print(f'New episode (ep={ep}) has not yet been found for {anime}')

            await asyncio.sleep(timeout)

    except asyncio.CancelledError:
        print(f'Alert for {anime} is cancelled')
        raise


@bot.command(name='addAnimeAlert', help='Create an alert whenever a new episode of the provided anime is released on Gogoanime')
async def alert(ctx, anime:str, timeout:int=100, channel_name:str='anime_alerts', base_url:str=BASE_URL):

    guild = ctx.guild
    channel = discord.utils.get(guild.channels, name=channel_name)

    # Create a new alerts channel if it already does not exist
    if channel is None:
        try:
            await guild.create_text_channel(channel_name)
            channel = discord.utils.get(guild.channels, name=channel_name)

        except:
            await ctx.send(f'Could not create {channel_name} channel. Please create it manually or give permission to'
                           f' me.')
            return

    if anime in tasks:
        print('An alert for this anime already exists')
        await ctx.send("An alert for this anime already exists")
        return

    lastEpisode = gogo_scraper.getLastEpisode(anime, base_url)
    if lastEpisode is None:
        print('This anime is either not a valid gogoanime anime title, or no episodes exist. Cannot create alerts')
        await ctx.send('This anime is either not a valid gogoanime anime title, or no episodes exist. Cannot create alerts')
        return

    await channel.send(f'Watching for new episodes of {anime}')
    latest_ep = lastEpisode['num']
    output = f'''\n
                        Latest episode of {anime} is: \n
                        Episode number: {latest_ep}
                        Link: {lastEpisode['link']}
                    '''
    await channel.send(output)

    nextEpisodeNumber = latest_ep
    nextEpisodeNumber += 1

    task = bot.loop.create_task(checkForNewEpisode(ctx, anime, nextEpisodeNumber, timeout, channel))
    tasks[anime] = {"task":task, "channel":channel}


@bot.command(name='stopAnimeAlert', help='Stop sending alerts for new episodes of the provided anime')
async def stopEpisodeWatch(ctx, anime: str):
    if anime in tasks:
        task = tasks[anime]
        task['task'].cancel()

        guild = ctx.guild
        channel = discord.utils.get(guild.channels, name=task['channel'])

        if channel is not None:
            await channel.send(f'Stopping alerts for new episodes of {anime}')
        print(f'Stopping alters for new episodes of {anime}')

        del tasks[anime]

    else:
        print('Could not find task')
        await ctx.send('Could not find task to stop')


bot.run(AUTH_TOKEN)
