import discord
import requests
import asyncio
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PULSOID_TOKEN = os.getenv("PULSOID_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_heart_rate():
    headers = {"Authorization": f"Bearer {PULSOID_TOKEN}"}
    response = requests.get("https://dev.pulsoid.net/api/v1/data/heart_rate", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("heart_rate", None)
    return None

async def post_heart_rate():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    while not client.is_closed():
        hr = get_heart_rate()
        if hr:
            await channel.send(f"❤️ Ritmo cardíaco actual: **{hr} bpm**")
        else:
            await channel.send("⚠️ No se pudo obtener el pulso.")
        await asyncio.sleep(15)

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')

client.loop.create_task(post_heart_rate())
client.run(DISCORD_TOKEN)
