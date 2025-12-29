import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True 
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
    async def setup_hook(self):
        await self.load_extension('cogs.lewis_showdown')
        await self.load_extension('cogs.ai')
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f'{bot.user} is online.')
    print(f'Connected to {len(bot.guilds)} servers')
    
    # Debug: Print all registered slash commands
    print("\nRegistered slash commands:")
    for command in bot.tree.get_commands():
        print(f"  - /{command.name}: {command.description}")
    print()

bot.run(DISCORD_TOKEN)
