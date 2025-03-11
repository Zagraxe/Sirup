import os
from discord.ext import commands
from ia import obtenir_reponse  # Fonction IA pour les réponses dynamiques
import discord

# Initialisation du bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Répondre automatiquement aux mentions
@bot.event
async def on_message(message):
    # Vérifie si le bot est mentionné
    if bot.user in message.mentions:
        # Log pour débogage
        print(f"Message reçu : {message.content}")

        # Gérer les réponses via l'IA
        try:
            # Préparation du prompt pour l'IA
            prompt = f"Tu es Sirup, un chevalier médiéval inspirant et motivant. Réponds avec sagesse : {message.content}"
            reponse = obtenir_reponse(prompt)

            # Envoyer la réponse de l'IA dans le salon
            await message.channel.send(reponse)

        except Exception as e:
            # Gère les erreurs et informe l'utilisateur
            print(f"Erreur dans la génération IA : {e}")
            await message.channel.send("Je suis désolé, je n'ai pas pu répondre. Une erreur est survenue avec l'IA.")

    # Assure-toi que les autres commandes du bot fonctionnent
    await bot.process_commands(message)

# Message de bienvenue
@bot.event
async def on_ready():
    print(f"{bot.user} est prêt !")
    channel_id = 1147544010580303933  # Remplace avec l'ID du salon de test
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("Salut à tous ! Je suis **Sirup**, votre chevalier inspirant et motivant. 🤖⚔️\n\n"
                           "Mentionnez-moi, et je vous répondrai avec honneur !")

# Lancer le bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
