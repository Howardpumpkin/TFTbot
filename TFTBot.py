from TFTfunc import getMorePlayedTraits,getKey
import discord
from discord.ext import commands
from jsonFileHandle import readJsonFile

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # 確保能讀取訊息內容
bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = getKey("DBToken")

@bot.command()
async def check(ctx,gameName:str,tagLine:int):
    await ctx.send("查詢中...")
    try:
        morePlayed = getMorePlayedTraits(gameName, tagLine)
        message = ""
        for player, traits in morePlayed.items():
            for trait, count in traits.items():
                message += f"{player} 玩了 {trait} {count} 次\n"
        await ctx.send(message)
    except Exception as e:
        await ctx.send(f"Error: {e}")
bot.run(TOKEN)