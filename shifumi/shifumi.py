import os
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv

print("Le bot Shifumi démarre...")  # Message de debug

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Définir le token à partir des variables d'environnement
token = os.getenv('DISCORD_BOT_TOKEN')

# Vérifier que la variable d'environnement est définie
if not token:
    print("Erreur : Token non défini.")
    exit(1)
else:
    print("Token défini correctement.")

# Définir les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True

# Initialisation du bot avec les intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialisation des scores
scores = {"bot": {'win': 0, 'loss': 0, 'draw': 0}}

# Options pour le jeu
choices = ['pierre', 'papier', 'ciseaux']

@bot.event
async def on_ready():
    print(f'Nous sommes connectés en tant que {bot.user}')
    print(f'ID du bot: {bot.user.id}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) and ctx.command.name in ['shifumi', 'choisir']:
        await ctx.send(
            "Commande non trouvée. Assurez-vous d'utiliser les commandes correctes : !shifumi et !choisir [ton choix]."
        )
        print(f"Erreur : {error}")
    else:
        # Laisser la gestion des erreurs standard de discord.py s'occuper des autres commandes
        raise error

@bot.command(name='shifumi')
async def shifumi(ctx):
    if ctx.author.id not in scores:
        scores[ctx.author.id] = {'win': 0, 'loss': 0, 'draw': 0}
    embed = discord.Embed(title="Shifumi - Pierre, Papier, Ciseaux", color=discord.Color.blue())
    embed.add_field(name="Choisis : pierre, papier ou ciseaux", value="Tape !choisir suivi de ton choix")
    print("Commande !shifumi appelée.")
    await ctx.send(embed=embed)

@bot.command(name='choisir')
async def choisir(ctx, choix: str):
    print(f"Commande !choisir appelée par {ctx.author.name} avec le choix {choix}")
    choix = choix.lower()
    if choix not in choices:
        await ctx.send("Choix invalide. Choisis parmi : pierre, papier, ou ciseaux.")
        print("Choix invalide reçu.")
        return
    bot_choice = random.choice(choices)
    if ctx.author.id not in scores:
        scores[ctx.author.id] = {'win': 0, 'loss': 0, 'draw': 0}
    if choix == bot_choice:
        result = "Égalité"
        scores[ctx.author.id]['draw'] += 1
    elif (choix == 'pierre' and bot_choice == 'ciseaux') or \
         (choix == 'papier' and bot_choice == 'pierre') or \
         (choix == 'ciseaux' and bot_choice == 'papier'):
        result = "Gagné"
        scores[ctx.author.id]['win'] += 1
    else:
        result = "Perdu"
        scores[ctx.author.id]['loss'] += 1
        scores['bot']['win'] += 1  # Ajouter une victoire au bot
    embed = discord.Embed(title="Shifumi - Résultat", color=discord.Color.green() if result == "Gagné" else discord.Color.red())
    embed.add_field(name="Ton choix", value=choix)
    embed.add_field(name="Choix du bot", value=bot_choice)
    embed.add_field(name="Résultat", value=result)
    embed.add_field(name="Score", value=f"Gagné: {scores[ctx.author.id]['win']}, Perdu: {scores[ctx.author.id]['loss']}, Égalité: {scores[ctx.author.id]['draw']}")
    embed.set_footer(text="Tape !Sscore pour voir le classement actuel")
    await ctx.send(embed=embed)

@bot.command(name='Sscore')
async def scoreshifumi(ctx):
    # Ajouter un utilisateur fictif pour le bot
    bot_user = type("BotUser", (object,), {"name": "Sir Up", "id": "bot"})
    sorted_scores = sorted(scores.items(), key=lambda x: (x[1]['win'] / max(1, x[1]['loss']), x[1]['win']), reverse=True)
    top_scores = sorted_scores[:5]
    while len(top_scores) < 5:
        top_scores.append(("N.A", {"win": "N.A", "loss": "N.A"}))
    embed = discord.Embed(title="Tableau des Scores Shifumi", color=discord.Color.magenta())
    lines = []
    for i, (user_id, score) in enumerate(top_scores, 1):
        if user_id == "bot":
            user = bot_user
        elif user_id == "N.A":
            user = type("NAUser", (object,), {"name": "N.A"})
        else:
            user = await ctx.bot.fetch_user(user_id)
        lines.append(f"Top {i}. {user.name}                {score['win']}/{score['loss']}")
    embed.add_field(name="Top Joueurs", value="\n".join(lines), inline=True)
    print("Commande !Sscore appelée.")
    await ctx.send(embed=embed)

# Démarrer le bot
bot.run(token)
