# commands/post_theme.py

import discord
from discord.ext import commands
from db import themes, users
import random
import string


class PostThemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="post_theme")
    async def post_theme(self, ctx, *, prompt):
        if not prompt or len(prompt.strip()) < 5:
            await ctx.send("⚠️ Your theme must be more detailed.")
            return

        short_id = generate_short_id()  # ✅ Generate the ID here

        theme_doc = {
            "user_id": ctx.author.id,
            "username": ctx.author.name,
            "prompt": prompt,
            "short_id": short_id,  # ✅ store it
            "channel_id": ctx.channel.id,
            "thread_id": None,
            "followers": [],
            "created_at": discord.utils.utcnow()
        }
        theme_id = themes.insert_one(theme_doc).inserted_id

        thread = await ctx.channel.create_thread(
            name=f"Theme: {prompt[:30]}",
            type=discord.ChannelType.public_thread,
            auto_archive_duration=1440
        )

        themes.update_one({"_id": theme_id}, {"$set": {"thread_id": thread.id}})

        users.update_one(
            {"user_id": ctx.author.id},
            {"$inc": {"points": 5}, "$set": {"username": ctx.author.name}},
            upsert=True
        )

        await thread.send(f"`{short_id}` 🌟 New theme from {ctx.author.mention}:\n**{prompt}**")
        await ctx.send(f"✅ Theme posted and thread created: {thread.mention}\nTheme ID: `{short_id}`")


# This is the key to load this Cog properly:
async def setup(bot):
    await bot.add_cog(PostThemeCog(bot))

def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))