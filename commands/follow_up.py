# commands/follow_up.py

import discord
from discord.ext import commands
from db import themes, users, follows
from bson import ObjectId

class FollowUpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="follow_up")
    async def follow_up(self, ctx, short_id: str = None):
        # Validate GIF attachment
        if not ctx.message.attachments:
            await ctx.send("⚠️ You must attach a GIF as part of your follow-up. BAN RISK.")
            return

        attachment = ctx.message.attachments[0]
        if not attachment.filename.lower().endswith(".gif"):
            await ctx.send("⚠️ Attachment must be a YUPP .gif file. BAN RISK.")
            return

        # Validate short theme ID
        if not short_id:
            await ctx.send("⚠️ You must provide a theme ID (printed when the theme was created).")
            return

        theme_doc = themes.find_one({"short_id": short_id})
        if not theme_doc:
            await ctx.send("⚠️ No theme found with that ID.")
            return

        if theme_doc["user_id"] == ctx.author.id:
            await ctx.send("⚠️ You can't follow up on your own theme. BAN RISK.")
            return

        existing = follows.find_one({"theme_id": theme_doc["_id"], "follower_id": ctx.author.id})
        if existing:
            await ctx.send("⚠️ You already followed up on this theme. BAN RISK.")
            return

        follows.insert_one({
            "theme_id": theme_doc["_id"],
            "follower_id": ctx.author.id,
            "username": ctx.author.name,
            "attachment_url": attachment.url,
            "timestamp": discord.utils.utcnow()
        })

        themes.update_one(
            {"_id": theme_doc["_id"]},
            {"$addToSet": {"followers": ctx.author.id}}
        )

        users.update_one(
            {"user_id": ctx.author.id},
            {"$inc": {"points": 2}, "$set": {"username": ctx.author.name}},
            upsert=True
        )
        users.update_one(
            {"user_id": theme_doc["user_id"]},
            {"$inc": {"points": 3}},
            upsert=True
        )

        # Post to thread if it exists
        try:
            thread = await ctx.guild.fetch_channel(theme_doc["thread_id"])
            await thread.send(f"🌀 {ctx.author.mention} followed up with a GIF:\n{attachment.url}")
        except:
            pass

        await ctx.send("✅ Follow-up recorded and points awarded!")


# Required setup function
async def setup(bot):
    await bot.add_cog(FollowUpCog(bot))
