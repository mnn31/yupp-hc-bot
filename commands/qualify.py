import discord
from discord.ext import commands
from db import users, themes, follows
from datetime import datetime, timedelta

class QualifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="qualify")
    async def qualify(self, ctx):
        user_id = ctx.author.id
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)

        # Count follow-ups in last week
        recent_followups = follows.count_documents({
            "follower_id": user_id,
            "timestamp": {"$gte": week_ago}
        })

        # Count themes posted in last week
        recent_themes = themes.count_documents({
            "user_id": user_id,
            "created_at": {"$gte": week_ago}
        })

        user_doc = users.find_one({"user_id": user_id}) or {}
        claimed_weeks = user_doc.get("bonus_claims", [])
        current_week = now.isocalendar().week

        bonus_text = ""
        bonus_awarded = False

        if current_week in claimed_weeks:
            bonus_text = "You've already claimed your bonus this week."
        elif recent_followups >= 6 and recent_themes >= 2:
            users.update_one(
                {"user_id": user_id},
                {
                    "$inc": {"points": 15},
                    "$addToSet": {"bonus_claims": current_week},
                    "$set": {"username": ctx.author.name}
                },
                upsert=True
            )
            bonus_awarded = True
            bonus_text = "✅ Bonus granted: +15 points for posting 2+ themes and 6+ follow-ups this week."
        else:
            bonus_text = "You do not yet qualify for the bonus."

        embed = discord.Embed(
            title="🎯 Qualification Status",
            color=discord.Color.red() if not bonus_awarded else discord.Color.green()
        )
        embed.description = bonus_text
        embed.add_field(name="Weekly Follow-ups", value=f"{recent_followups} (Need 6)", inline=True)
        embed.add_field(name="Themes Posted", value=f"{recent_themes} (Need 2)", inline=True)

        await ctx.send(embed=embed)

# Required setup
async def setup(bot):
    await bot.add_cog(QualifyCog(bot))
