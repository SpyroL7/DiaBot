import discord
import time
import asyncio
from discord.ext import commands
import random

client = commands.Bot(description="Please don't sue us over our advice", command_prefix="$")

@client.event
async def on_ready():
    print('DiaBot Ready')
    print(client.user.name)
    print(client.user.id)
    client.loop.create_task(status_task())
    print('_-_-_-_-_-_-_-_')

async def status_task():
    while True:
        activity = discord.Game(name="providing legit medical advice")
        await client.change_presence(status=discord.Status.idle, activity=activity)
        await asyncio.sleep(30)
        activity = discord.Game(name="created by SpyroL7")
        await client.change_presence(status=discord.Status.idle, activity=activity)
        await asyncio.sleep(30)

async def chat(channel, message=None, tts=False, embed=None):
    if message == None and embed == None:
        return False
    else:
        try:
            msg = await message.channel.send(channel, message=message, tts=tts, embed=embed)
            return msg
        except discord.errors.Forbidden:
            print('The bot is not allowed to send messages to this channel')
            return None

@client.event
async def on_message(message):
    if message.content == "$setup":
        embed = discord.Embed(title="Set Up", description="Use these commands to set up DiaBot!", color=0X1BC2F8)
        embed.add_field(name="$carbratio [number]", value="enter in how many carbs per 1 unit of insulin")
        embed.add_field(name="$resolution [0.1, 0.5 or 1]", value="enter to what granularity your insulin doser can administer")
        embed.add_field(name="$bloodratio [number]", value="enter how many mmol/L 1 unit of insulin brings you down")
        embed.add_field(name="$bgl [number]", value="enter how many mmol/L your BG is at currently")
        embed.add_field(name="IMPORTANT", value="please use all of these commands IN THIS ORDER!")
        #embed.add_field(name="$discounts", value="set discounts with percentage decreases")
        #embed.add_field(name="$increases", value="set increases with percentage increases")
        await message.channel.send(content=None, embed=embed)
    if message.content.startswith("$carbratio"):
        carbRatio = message.content[10:]
        embed = discord.Embed(title = "Carb Ratio", description = "Saved! your ratio is 1:" + carbRatio, colour=0X1BC2F8)
        f = open("data.txt", "w")
        f.write(carbRatio + "\n")
        f.close()
        await message.channel.send(content=None, embed=embed)
    if message.content.startswith("$resolution"):
        resolution = message.content[11:]
        embed = discord.Embed(title = "Resoluition", description = "Saved! your resolution is" + resolution, colour=0X1BC2F8)
        f = open("data.txt", "a")
        f.write(resolution + "\n")
        f.close()
        await message.channel.send(content=None, embed=embed)
    if message.content.startswith("$bloodratio"):
        bloodRatio = message.content[11:]
        embed = discord.Embed(title = "Blood Ratio", description = "Saved! your ratio is 1:" + bloodRatio, colour=0X1BC2F8)
        f = open("data.txt", "a")
        f.write(bloodRatio + "\n")
        f.close()
        await message.channel.send(content=None, embed=embed)
    if message.content.startswith("$bgl"):
        bloodGlucose = message.content[4:]
        embed = discord.Embed(title = "Blood Glucose Level", description = "Saved! your BGL is " + bloodGlucose, colour=0X1BC2F8)
        f = open("data.txt", "a")
        f.write(bloodGlucose)
        f.close()
        await message.channel.send(content=None, embed=embed)
    if message.content.startswith("$calculate"):
        try:
            carbs = message.content[10:]
            f = open("data.txt", "r")
            carbRatio = f.readline()
            resolution = f.readline()
            bloodRatio = f.readline()
            bloodGlucose = f.readline()
            f.close()
            carbUnits = int(carbs)/int(carbRatio)
            hypo = False
            correctionNeeded = False
            if float(bloodGlucose) < 4:
                embed = discord.Embed(title = "HYPO ALERT", description = "Don't take insulin! You're having a hypo", color=0Xff0000)
                hypo = True
                correctionNeeded = False
            elif float(bloodGlucose) >= 4 and float(bloodGlucose) < 7:
                correctionNeeded = False
            else:
                correction = (float(bloodGlucose) - 5.5)/float(bloodRatio)
                correctionNeeded = True
            if correctionNeeded == False:
                totalUnits = carbUnits
            else:
                totalUnits = carbUnits + correction
            if resolution == "1":
                totalUnits = round(totalUnits)
            elif resolution == "0.5":
                totalUnits = round(totalUnits*2)/2
            elif resolution == "0.1":
                totalUnits = round(totalUnits, 1)
            if hypo == False:
                embed = discord.Embed(title = "Insulin Units Calculation", description = "Our recomended dosage based on your data is " + str(totalUnits) + "u", colour=0X1BC2F8)
        except:
            embed = discord.Embed(title = "~ERROR~", description = "Something went wrong! Are you sure you have already entered your BGL, resolution, blood ratio and carb ratio in ther right order? Did you input a valid number for each variable?", color=0Xff0000)
        await message.channel.send(content=None, embed=embed)
        


client.run('XXXXXXXXXXXXXXXXXXXXXX')
