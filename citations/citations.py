import os
import discord
from discord.ext import commands, tasks
import random

print("Le bot démarre...")  # Message de debug

# Définir le token à partir des variables d'environnement
token = os.getenv('DISCORD_BOT_TOKEN')

# Vérifier que les variables d'environnement sont définies
if not token:
    print("Erreur : Token non défini.")
    exit(1)

# Définir les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True

# Initialisation du bot avec les intents
bot = commands.Bot(command_prefix='!', intents=intents)

channel_id = 1307995646388863018  # Ton ID de salon de tests

# Indicateur pour activer ou désactiver la fonctionnalité des mots-clés
keywords_enabled = True

@bot.event
async def on_ready():
    print(f'Nous sommes connectés en tant que {bot.user}')
    print(f'ID du bot: {bot.user.id}')
    send_daily_quote.start()

@tasks.loop(hours=24)
async def send_daily_quote():
    channel = bot.get_channel(channel_id)
    quote = get_random_quote()
    embed = create_embed("Citation du jour", quote)
    await channel.send(embed=embed)

@send_daily_quote.before_loop
async def before():
    await bot.wait_until_ready()
    print("Bot prêt à envoyer des citations quotidiennes")

def get_random_quote():
    # Lire les citations depuis le fichier citations/citation.txt
    with open('citations/citation.txt', 'r', encoding='utf-8') as f:
        quotes = f.readlines()
    return random.choice(quotes).strip()

def create_embed(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.orange())
    return embed

def load_keywords(file_path):
    keywords = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            key, message = line.strip().split(';')
            keywords[key.lower()] = message
    return keywords

# Charger les mots-clés
keywords = load_keywords('citations/keywords.txt')

@bot.command(name='citations')
async def citations(ctx):
    quote = get_random_quote()
    embed = create_embed("Citation du jour", quote)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    global keywords_enabled

    if message.author == bot.user:
        return

    if keywords_enabled:
        print(f"Message reçu : {message.content}")

        for keyword, response in keywords.items():
            if keyword in message.content.lower():
                print(f"Mot-clé détecté : {keyword}")
                await message.channel.send(response)
                break

    await bot.process_commands(message)

@bot.command(name='Siron')
@commands.has_permissions(administrator=True)
async def enable_keywords(ctx):
    global keywords_enabled
    keywords_enabled = True
    await ctx.send("JE SUIS PRÉSENT ! La fonctionnalité des mots-clés a été activée.")

@bot.command(name='Siroff')
@commands.has_permissions(administrator=True)
async def disable_keywords(ctx):
    global keywords_enabled
    keywords_enabled = False
    await ctx.send("Sir up a quitté. La fonctionnalité des mots-clés a été désactivée.")

# Démarrer le bot
if token:
    print("Le token a été trouvé.")  # Message de debug
    bot.run(token)
else:
    print("Erreur : Le jeton du bot Discord n'est pas défini")  # Message de debug

print("Le bot est en train de démarrer...")  # Message de debug
