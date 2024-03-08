import discord
import asyncio
import pytz
from datetime import datetime, timezone, timedelta

# Define all intents
intents = discord.Intents.all()

# Initialize the Discord client with intents
client = discord.Client(intents=intents)

# Your Discord bot token
TOKEN = ''

# The time to ping (in 24-hour format)
target_hour = 7
target_minute = 27

# ID of the channel where the bot will send messages
channel_id = 1102288754607136786  # Replace this with your desired channel ID

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

    # Start the background task
    await ping_role_at_target_time()

async def ping_role_at_target_time():
    while True:
        # Get current UTC time
        current_time_utc = datetime.now(timezone.utc)

        # Get a list of all timezones
        all_timezones = pytz.all_timezones

        for timezone_str in all_timezones:
            # Convert UTC time to the target timezone
            target_timezone_obj = timezone(timedelta(hours=get_timezone_offset(timezone_str)))
            current_time_target = current_time_utc.astimezone(target_timezone_obj)

            # Check if it's the target time
            if current_time_target.hour == target_hour and current_time_target.minute == target_minute:
                # Fetch the guild
                guild = client.get_guild(1102288753164296233)

                # Fetch the role to ping
                role = discord.utils.get(guild.roles, name='dead chat moment')

                # Fetch the channel to send the message
                channel = client.get_channel(channel_id)

                if channel:
                    await channel.send(f"{role.mention}, it's {current_time_target.strftime('%I:%M %p')} somewhere in the world! WYSI!!!!")
                else:
                    print("Channel not found!")

                # Sleep to avoid spamming the channel
                await asyncio.sleep(60)  # Sleep for a minute

        # Sleep for a second before checking the time again
        await asyncio.sleep(1)

def get_timezone_offset(timezone_str):
  # Get the timezone offset in hours
  tz = pytz.timezone(timezone_str)
  return int(tz.utcoffset(datetime.utcnow()).total_seconds() / 3600)
# Run the bot
client.run(TOKEN)
