import discord
import FaceSwap

client = discord.Client()
fs = FaceSwap.RandomFaceSwap(['imgs/gh.jpg'])


@client.event
async def on_ready():
    print("Logged in as", client.user)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!danielfy'):
        img_url = message.content

client.run("")
