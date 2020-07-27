# Discord-Referral-Program
Bot for tracking how many people users on a Discord server invite to your server.

## Requirements
- Python 3.6+
- [discordpy](https://discordpy.readthedocs.io/en/latest/)

## Setup
1. Ensure all Requirements are met.
2. Add [Discord bot token](https://discord.com/developers/applications) and the specifiedChannelId to ./config/config.json.
3. Configure command prefix if you want to change from the default (r!).
4. run main.py
5. Type r!help in the Specified channel to begin.

# What is specifiedChannelId
This is the ID of the channel which you want your referral commands to be used it.  The bot will only allow commands to be used in the channel with this ID.  You can get this by enabling Discord (developer mode)[https://discordia.me/en/developer-mode#:~:text=Enabling%20Developer%20Mode%20is%20easy,the%20toggle%20to%20enable%20it.], then right clicking the text channel you wish to have the commands in and click "Copy ID".

# Reseting data
If for what ever reason you wish to reset your referral program data, you either edit the json files in ./data/ or you can run resetJSON.py.  This will reset all data json files to their starting empty formats.
