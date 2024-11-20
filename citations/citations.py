import os
import discord
from discord.ext import commands, tasks
import random

print("Le bot démarre...")  # Message de debug

# Définir les intents nécessaires pour le bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Assurez-vous que l'intent est activé

# Initialisation du bot avec les intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Remplace par l'ID de ton salon de citations
channel_id = 1290357742153764996

# Indicateur pour activer ou désactiver la fonctionnalité des mots-clés
keywords_enabled = True

# Indicateur pour activer ou désactiver l'envoi des citations quotidiennes
daily_quotes_enabled = True

@bot.event
async def on_ready():
    print(f'Nous sommes connectés en tant que {bot.user}')
    print(f'ID du bot: {bot.user.id}')
    send_daily_quote.start()

@tasks.loop(hours=24)
async def send_daily_quote():
    global daily_quotes_enabled
    if daily_quotes_enabled:
        channel = bot.get_channel(channel_id)
        quote = get_random_quote()
        embed = create_embed("Citation du jour", quote)
        await channel.send(embed=embed)

@send_daily_quote.before_loop
async def before():
    await bot.wait_until_ready()
    print("Bot prêt à envoyer des citations quotidiennes")

def get_random_quote():
    # Vérifier si le fichier existe
    file_path = 'citations/citations.txt'
    if not os.path.isfile(file_path):
        return "Erreur : Le fichier de citations n'existe pas."

    # Lire les citations depuis le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        quotes = f.readlines()
    return random.choice(quotes).strip()

def create_embed(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.orange())
    return embed

def load_keywords(file_path):
    if not os.path.isfile(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        return {}

    keywords = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            key, message = line.strip().split(';')
            keywords[key.lower()] = message
    return keywords

# Charger les mots-clés
keywords = load_keywords('citations/keywords.txt')

@bot.command(name='citation')
async def citation(ctx):
    quote = get_random_quote()
    if "Erreur" in quote:
        await ctx.send(quote)
    else:
        embed = create_embed("Citation du jour", quote)
        await ctx.send(embed=embed)

@bot.event
async def on_message(message):
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
    if not keywords_enabled:  # Vérifier si la fonctionnalité est déjà activée
        keywords_enabled = True
        await ctx.send("JE SUIS PRÉSENT ! La fonctionnalité des mots-clés a été activée.")

@bot.command(name='Siroff')
@commands.has_permissions(administrator=True)
async def disable_keywords(ctx):
    global keywords_enabled
    if keywords_enabled:  # Vérifier si la fonctionnalité est déjà désactivée
        keywords_enabled = False
        await ctx.send("Sir up a quitté. La fonctionnalité des mots-clés a été désactivée.")

@bot.command(name='Cion')
@commands.has_permissions(administrator=True)
async def enable_daily_quotes(ctx):
    global daily_quotes_enabled
    if not daily_quotes_enabled:  # Vérifier si la fonctionnalité est déjà activée
        daily_quotes_enabled = True
        await ctx.send("Les citations quotidiennes ont été activées.")

@bot.command(name='Cioff')
@commands.has_permissions(administrator=True)
async def disable_daily_quotes(ctx):
    global daily_quotes_enabled
    if daily_quotes_enabled:  # Vérifier si la fonctionnalité est déjà désactivée
        daily_quotes_enabled = False
        await ctx.send("Les citations quotidiennes ont été désactivées.")

# Utilisation du secret pour le token Discord
token = os.getenv('DISCORD_BOT_TOKEN')
if token:
    print("Le token a été trouvé.")  # Message de debug
    bot.run(token)
else:
    print("Erreur : Le jeton du bot Discord n'est pas défini")  # Message de debug

print("Le bot est en train de démarrer...")  # Message de debug
