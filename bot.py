import os
import asyncio
from discord.ext import commands
from ia import obtenir_reponse
import discord

# Initialisation du bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ID du salon pour les messages périodiques
TEST_CHANNEL_ID = 123456789012345678  # Remplace avec l'ID réel de ton salon

# Tâche périodique
async def envoyer_message_periodique():
    await bot.wait_until_ready()
    channel = bot.get_channel(TEST_CHANNEL_ID)
    if channel:
        await channel.send("Nobles âmes, quelqu'un souhaite-t-il discuter ? ⚔️")

bot.loop.create_task(envoyer_message_periodique())

# Gestion des mentions
@bot.event
async def on_message(message):
    if bot.user in message.mentions:  # Si le bot est mentionné
        prompt = f"Tu es Sirup, un chevalier médiéval. Réponds avec courtoisie : {message.content}"
        reponse = obtenir_reponse(prompt)
        await message.channel.send(reponse)

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
