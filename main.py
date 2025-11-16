import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

sec_role = "King"
password = "Beans"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server!{member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    bad_words = ["shit", "fuck", "asshole", "bitch", "damn"]
    if any(word in message.content.lower() for word in bad_words):
        await message.delete()
        await message.channel.send(f"Hey {message.author.mention}, please don't use that language in the server.")
    await bot.process_commands(message)


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=sec_role)
    if role:
        await ctx.send("Please enter the password\n(the password is case sensitive and the Owner's favorite food😁):")
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            message = await bot.wait_for("message", check=check, timeout=40.0)
            if message.content == password:
                await ctx.author.add_roles(role)
                await ctx.send(f"Nice, you have been assigned the {role.name} role.")
            else:
                await ctx.send("Incorrect password.")
        except Exception:
            await ctx.send("Time's up or an error occurred. Try again later.")
    else:
        await ctx.send(f"The {sec_role} role does not exist.")



@bot.command()
async def unassign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=sec_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"You have been removed from the {role.name} role.")
    else:
        await ctx.send(f"The {sec_role} role does not exist.")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
