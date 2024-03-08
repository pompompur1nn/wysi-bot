import discord
import asyncio
from datetime import datetime, timezone, timedelta

# Your Discord bot token
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# The time to ping (in 24-hour format)
target_hour = 7
target_minute = 27

# Initialize the Discord client
client = discord.Client()

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
    all_timezones = [tz for tz in pytz.all_timezones]

    for timezone_str in all_timezones:
      # Convert UTC time to the target timezone
      target_timezone_obj = timezone(
          timedelta(hours=get_timezone_offset(timezone_str)))
      current_time_target = current_time_utc.astimezone(target_timezone_obj)

      # Check if it's the target time
      if current_time_target.hour == target_hour and current_time_target.minute == target_minute:
        # Fetch the guild
        guild = client.get_guild(YOUR_GUILD_ID_HERE)

        # Fetch the role to ping
        role = discord.utils.get(guild.roles, name='YOUR_ROLE_NAME_HERE')

        # Ping the role in a specific channel
        channel = guild.get_channel(YOUR_CHANNEL_ID_HERE)
        await channel.send(
            f"{role.mention}, it's {current_time_target.strftime('%I:%M %p')} in {timezone_str}!"
        )

        # Sleep to avoid spamming the channel
        await asyncio.sleep(60)  # Sleep for a minute

    # Sleep for a second before checking the time again
    await asyncio.sleep(1)


def get_timezone_offset(timezone_str):
  # Get the timezone offset in hours
  return int(
      timezone(timedelta(0),
               timezone(timezone_str)).utcoffset().total_seconds() / 3600)


# Run the bot
client.run(TOKEN)
