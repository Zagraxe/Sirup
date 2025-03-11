import os
from discord.ext import commands
from ia import obtenir_reponse  # Fonction IA pour les réponses dynamiques
import discord

# Initialisation du bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Événement : Répondre aux messages où le bot est mentionné
@bot.event
async def on_message(message):
    # Ignore les messages envoyés par le bot lui-même
    if message.author == bot.user:
        return

    # Vérifie si le bot est mentionné
    if bot.user in message.mentions:
        try:
            # Nettoie le message pour enlever les mentions
            clean_content = message.content.replace(f"<@{bot.user.id}>", "").strip()
            prompt = f"Tu es Sirup, un chevalier médiéval inspirant et motivant. Réponds avec sagesse : {clean_content}"
            
            # Appel à l'IA pour une réponse
            reponse = obtenir_reponse(prompt)
            await message.channel.send(reponse)

        except Exception as e:
            # Gère les erreurs et informe l'utilisateur
            print(f"Erreur dans la génération IA : {e}")
            await message.channel.send("Je suis désolé, je n'ai pas pu répondre. Une erreur est survenue avec l'IA.")

    # Continue à traiter d'autres commandes
    await bot.process_commands(message)

# Événement : Message de bienvenue
@bot.event
async def on_ready():
    print(f"{bot.user} est prêt !")
    channel_id = 1147544010580303933  # Remplace par l'ID de ton salon de test
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("Salut à tous ! Je suis **Sirup**, votre chevalier inspirant et motivant. 🤖⚔️\n\n"
                           "Mentionnez-moi, et je vous répondrai avec honneur !")

# Lancer le bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
