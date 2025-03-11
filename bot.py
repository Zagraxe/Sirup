import os
from discord.ext import commands

# Initialisation du bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Événement : Le bot est prêt
@bot.event
async def on_ready():
    print(f"{bot.user} est prêt et en ligne !")
    print(f"ID du bot : {bot.user.id}")

# Commande Ping (Test)
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send("Pong ! Tout est opérationnel. 🏓")

# Lancer le bot
token = os.getenv('DISCORD_BOT_TOKEN')
if token:
    print("Le token a été trouvé.")  # Debug
    bot.run(token)
else:
    print("Erreur : Le token du bot Discord n'est pas défini.")
