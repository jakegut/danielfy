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
        try:
            img_url = message.content.split(" ")[1]
        except IndexError:
            await message.channel.send("Please supply a URL")
            return
        
        img = fs.face_swap(img_url)

        if isinstance(img, str):
            await message.channel.send(img)
            return
         
        await message.channel.send(file=discord.File(img, 'cool_image.png'))

client.run("")
