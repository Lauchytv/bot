import httpx,requests, gc,discord,time,calendar, traceback,threading, socks, random, json, tracemalloc, asyncio; from discord.utils import get;from discord import Member; from dotenv import load_dotenv; from discord.ext import commands
tracemalloc.start()

def get_config():
    config_file = open("config.json","r", encoding="utf8")
    configx = config_file.read()
    config_file.close()
    return configx

def get_prefix():
    config_file = get_config()
    config = json.loads(config_file)
    prefix = config['bot_config']["prefix"] 
    return prefix
    
config_file = get_config()
config = json.loads(config_file)
prefix = config['bot_config']["prefix"]
token = config['bot_config']["token"]

queue = []

load_dotenv()
intents = discord.Intents().all()
bot = commands.AutoShardedBot(command_prefix=get_prefix(), help_command=None, intents=intents)

def init():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run(token))
    threading.Thread(target=loop.run_forever).start()


@bot.command()
async def stock(ctx):
 if ctx.channel.type != discord.ChannelType.private:
        filefile = open('ttoken_follow.txt')
        fnum_lines = sum(1 for line in filefile)
        filefile.close()
        filefile = open('ttoken_spam.txt')
        snum_lines = sum(1 for line in filefile)
        filefile.close()
        embed=discord.Embed(title="Stock",color=16777215, description=f"Twitch Stock:\n \nSpam: **{snum_lines}**\nFollow: **{fnum_lines}** ")
        await ctx.send(embed=embed)

def get_id(user):

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept-Language': 'en-US',
        'sec-ch-ua-mobile': '?0',
        'Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Client-Session-Id': '51789c1a5bf92c65',
        'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        'X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.twitch.tv',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.twitch.tv/',
    }
    data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
    try:
        response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
        id = response.json()[0]['data']['user']['id']
        return id
    except:
        return None
    
@bot.command()
async def bronze(ctx):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]
    embed=discord.Embed(title="Free Bronze",color=16777215, description=f"**set .gg/JTG in status, you will automatically get a rank Bronze**")
    await ctx.send(embed=embed)




@bot.event
async def on_member_update(before, after):
    role_id = 922780377427353640
    role = get(before.guild.roles, id=role_id)
    if '.gg/JTG' in str(before.activities):
      if '.gg/JTG' in str(after.activities):
        pass
      else:
        await after.remove_roles(role)
        channel = bot.get_channel(933209028010577940)
        embed=discord.Embed(description=f"Bronze has been removed from {after.mention}", color=discord.Color.red())
        await channel.send(embed=embed)

    if '.gg/JTG' in str(after.activities):
        await after.add_roles(role)
        channel = bot.get_channel(933209028010577940)
        embed=discord.Embed(description=f"{after.mention} has claimed Bronze!", color=discord.Color.green())
        await channel.send(embed=embed)