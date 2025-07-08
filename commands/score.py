import discord
from discord.ext import commands
from db import users, themes, follows
from datetime import datetime

class ScoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="score")
    async def score(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        # Themes created by this user
        theme_cursor = themes.find({"user_id": member.id})
        theme_count = 0
        total_followers = 0

        for theme in theme_cursor:
            theme_count += 1
            total_followers += len(theme.get("followers", []))

        # Follow-ups made by this user
        followup_count = follows.count_documents({"follower_id": member.id})

        # Calculate base score
        base_score = (4 * theme_count) + (2 * followup_count) + (2 * total_followers)

        # Bonus points earned from bonus claims
        user_doc = users.find_one({"user_id": member.id}) or {}
        bonus_claims = user_doc.get("bonus_claims", [])
        bonus_points = len(bonus_claims) * 15

        total_points = base_score + bonus_points

        embed = discord.Embed(
            title=f"📊 Score for {member.display_name}",
            color=discord.Color.green()
        )
        embed.add_field(name="Total Points", value=f"**{total_points}**", inline=False)
        embed.add_field(name="– Theme Creation (4 pts each)", value=theme_count, inline=True)
        embed.add_field(name="– Follow-Ups (2 pts each)", value=followup_count, inline=True)
        embed.add_field(name="– Reactions to Your Themes (2 pts each)", value=total_followers, inline=True)
        embed.add_field(name="➕ Bonus Points", value=bonus_points, inline=False)

        await ctx.send(embed=embed)

# Required setup
async def setup(bot):
    await bot.add_cog(ScoreCog(bot))
