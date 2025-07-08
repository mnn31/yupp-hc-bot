# commands/leaderboard.py

import discord
from discord.ext import commands
from db import users, themes, follows

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def calculate_points(self, user_id):
        # Count themes created by the user
        theme_cursor = themes.find({"user_id": user_id})
        theme_count = 0
        total_followers = 0
        for theme in theme_cursor:
            theme_count += 1
            total_followers += len(theme.get("followers", []))

        # Count follow-ups made by the user
        followup_count = follows.count_documents({"follower_id": user_id})

        # Calculate total points
        return {
            "themes": theme_count,
            "followups": followup_count,
            "responses_received": total_followers,
            "total": (4 * theme_count) + (2 * followup_count) + (2 * total_followers)
        }

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx):
        user_scores = []
        seen_ids = set()

        # Go through users who posted themes
        for theme_doc in themes.find():
            uid = theme_doc["user_id"]
            if uid not in seen_ids:
                seen_ids.add(uid)
                score_data = self.calculate_points(uid)
                user_scores.append((uid, score_data))

        # Go through users who followed up
        for follow_doc in follows.find():
            uid = follow_doc["follower_id"]
            if uid not in seen_ids:
                seen_ids.add(uid)
                score_data = self.calculate_points(uid)
                user_scores.append((uid, score_data))

        # Sort by total points, descending
        sorted_users = sorted(user_scores, key=lambda x: x[1]["total"], reverse=True)[:10]

        # Build display
        embed = discord.Embed(title="🏆 Yupp HYPERCHARGED Leaderboard", color=discord.Color.gold())
        for rank, (uid, data) in enumerate(sorted_users, 1):
            user_data = users.find_one({"user_id": uid})
            username = user_data.get("username", f"<@{uid}>")
            embed.add_field(
                name=f"#{rank} - {username}",
                value=f'**{data["total"]} pts** | Themes: {data["themes"]}, Follow-ups: {data["followups"]}, Replies Received: {data["responses_received"]}',
                inline=False
            )

        await ctx.send(embed=embed)

# Required setup
async def setup(bot):
    await bot.add_cog(LeaderboardCog(bot))
