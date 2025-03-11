import os
from discord.ext import commands
from ia import obtenir_reponse  # Fonction IA pour les réponses dynamiques
import discord

# Initialisation du bot
intents = discord.Intents.default()
intents.voice_states = False  # Désactiver les fonctionnalités vocales
bot = commands.Bot(command_prefix='!', intents=intents)

# ID du salon où le bot est actif (remplace avec ton ID réel)
TEST_CHANNEL_ID = 123456789012345678  # Remplace cet ID

# Fonction pour répondre dynamiquement aux mentions
@bot.event
async def on_message(message):
    if bot.user in message.mentions:  # Si le bot est mentionné
        # Vérifie si le message contient une question sur le créateur
        contenu_message = message.content.lower()
        if "qui t'a créé" in contenu_message or "qui est ton créateur" in contenu_message:
            await message.channel.send("Je suis fier de dire que j'ai été créé par **Zagraxe** ! ⚔️💻")
        else:
            # Réponse normale avec l'IA
            prompt = f"Tu es Sirup, un chevalier médiéval inspirant et motivant. Réponds avec sagesse : {message.content}"
            reponse = obtenir_reponse(prompt)  # Génération de réponse via l'IA
            await message.channel.send(reponse)

    await bot.process_commands(message)  # Permet d'exécuter d'autres commandes si nécessaires

# Message de présentation au démarrage
@bot.event
async def on_ready():
    channel = bot.get_channel(TEST_CHANNEL_ID)  # Remplace cet ID par celui de ton salon principal
    if channel:
        await channel.send("Salut à tous ! Je suis **Sirup**, votre chevalier inspirant et motivant. 🤖⚔️\n\n"
                           "Posez-moi vos questions, et je suis là pour y répondre avec honneur !")

# Lancer le bot avec le token Discord
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
