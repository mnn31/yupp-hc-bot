# commands/event_info.py

import discord
from discord.ext import commands

class EventInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="event_info")
    async def event_info(self, ctx):
        embed = discord.Embed(
            title="📢 Yupp HYPERCHARGED Event Info",
            description=(
                "Welcome to the ultimate GIF-based community event. Your mission: post themes, respond with GIFs, and rack up points.\n\n"
                "🚫 **Abuse or irrelevance will get you banned. No exceptions.**"
            ),
            color=discord.Color.orange()
        )

        embed.add_field(
            name="🎯 Scoring Rules",
            value=(
                "• +4 points for every theme you post\n"
                "• +2 points for every valid GIF response you make\n"
                "• +2 points for every user who responds to your theme"
            ),
            inline=False
        )

        embed.add_field(
            name="🎁 Weekly Bonus",
            value=(
                "• Post **2 themes** AND make **6 follow-ups** in a week\n"
                "• Earn an extra **+15 points**\n"
                "• You can only claim this bonus once every 7 days"
            ),
            inline=False
        )

        embed.add_field(
            name="📌 Event Rules (Strict)",
            value=(
                "• Only post GIFs relevant to the theme. Off-topic = BAN\n"
                "• No spammy, low-effort, or nonsensical themes\n"
                "• Never respond to your own themes\n"
                "• Multiple violations = instant ban from all future events"
            ),
            inline=False
        )

        embed.add_field(
            name="🏆 Coming Soon",
            value="A leaderboard and custom rewards are on the way — stay active and climb the ranks!",
            inline=False
        )

        embed.set_footer(text="Yupp HYPERCHARGED — Built by the community, for the community ✨")

        await ctx.send(embed=embed)

# Required setup
async def setup(bot):
    await bot.add_cog(EventInfoCog(bot))
