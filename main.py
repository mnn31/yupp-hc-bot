# main.py

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from db import users, themes, follows  # optional if unused right now

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

# Async load of extensions
async def load_extensions():
    try:
        await bot.load_extension("commands.post_theme")
        await bot.load_extension("commands.follow_up")
        await bot.load_extension("commands.score")
        await bot.load_extension("commands.leaderboard")
        await bot.load_extension("commands.qualify")
        await bot.load_extension("commands.event_info")
        print("✅ Loaded post_theme, follow_up, score, leaderboard, qualify, and event_info commands")
    except Exception as e:
        print(f"❌ Failed to load post_theme: {e}")
        print(f"❌ Failed to load follow_up: {e}")
        print(f"❌ Failed to load score: {e}")

# Main async runner
async def main():
    await load_extensions()
    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
