import os
import random
from discord.ext import commands
from ia import obtenir_reponse  # Fonction IA Hugging Face pour générer des réponses
import discord

# Initialisation du bot avec intents
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Liste des phrases motivantes
phrases_motivantes = [
    "Continue ! Le succès n'est qu'à un pas ! 🌟",
    "Chaque échec te rapproche de la réussite. 💪",
    "Tu es plus fort(e) que tu ne le penses. 🚀"
]

# Commande : Motivation
@bot.command()
async def motive(ctx):
    phrase = random.choice(phrases_motivantes)
    await ctx.send(phrase)

# Réponse dynamique : Mention directe du bot
@bot.event
async def on_message(message):
    if bot.user in message.mentions:  # Si le bot est mentionné
        contenu_message = message.content.lower()
        if "qui t'a créé" in contenu_message or "qui est ton créateur" in contenu_message:
            await message.channel.send("Je suis fier de dire que j'ai été créé par **Zagraxe** ! ⚔️💻")
        else:
            prompt = f"Tu es Sirup, un chevalier médiéval inspirant et motivant. Réponds avec sagesse : {message.content}"
            reponse = obtenir_reponse(prompt)
            await message.channel.send(reponse)

    await bot.process_commands(message)

# Événement : Message de bienvenue
@bot.event
async def on_ready():
    print(f"{bot.user} est prêt !")
    channel_id = 1147544010580303933  # Remplace par l'ID de ton salon principal
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("Salut à tous ! Je suis **Sirup**, votre chevalier inspirant et motivant. 🤖⚔️\n\n"
                           "Posez-moi vos questions, et je suis là pour y répondre avec honneur !")

# Lancer le bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
