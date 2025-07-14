# Yupp Hypercharged Bot

A Discord bot for managing themes, follow-ups, and scoring in a community setting.

## Features

- **Score System**: Track points based on theme creation, follow-ups, and reactions
- **Leaderboard**: View top performers in the community
- **Theme Management**: Post and manage themes with follow-up capabilities
- **Qualification System**: Check if users qualify for certain activities
- **Event Information**: Get details about current events

## Commands

- `!score [@user]` - View your score or another user's score
- `!leaderboard` - View the top scoring users
- `!post_theme <theme>` - Post a new theme
- `!follow_up <theme_id> <content>` - Add a follow-up to a theme
- `!qualify` - Check if you qualify for certain activities
- `!event_info` - Get information about current events

## Setup

1. Clone the repository
2. Install dependencies: `pip install discord.py pymongo`
3. Create a `.env` file with:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   MONGO_URI=your_mongodb_connection_string
   ```
4. Run the bot: `python main.py`

## Score Calculation

- Theme Creation: 4 points each
- Follow-ups: 2 points each  
- Reactions to Your Themes: 2 points each
- Bonus Points: 15 points per bonus claim

## Security

The `.env` file is excluded from version control to protect sensitive tokens and database credentials. 