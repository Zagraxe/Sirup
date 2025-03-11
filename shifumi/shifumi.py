import os
import random
import discord
from discord.ext import commands

# Debug : Message pour indiquer le démarrage
print("Le bot Shifumi démarre...")

# Définir le token depuis les variables d'environnement
token = os.getenv('DISCORD_BOT_TOKEN')

# Vérifier que le token est défini
if not token:
    print("Erreur : Le token Discord n'est pas défini.")
    exit(1)
else:
    print("Token trouvé.")

# Initialisation des intents nécessaires pour le bot
intents = discord.Intents.default()
intents.message_content = True

# Création du bot avec les intents définis
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialisation des scores pour les utilisateurs
scores = {"bot": {"win": 0, "loss": 0, "draw": 0}}

# Options de jeu pour Shifumi
choices = ['pierre', 'papier', 'ciseaux']

# Événement : Le bot est prêt
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    print(f"ID du bot : {bot.user.id}")

# Gestionnaire d'erreur : Commandes non trouvées ou erreurs
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Commande non trouvée. Utilise `!shifumi` pour commencer ou `!choisir [ton choix]` pour jouer !"
        )
        print(f"Erreur : {error}")
    else:
        # Laisser discord.py gérer les autres erreurs
        raise error

# Commande principale pour démarrer une partie
@bot.command(name='shifumi')
async def shifumi(ctx):
    if ctx.author.id not in scores:
        scores[ctx.author.id] = {"win": 0, "loss": 0, "draw": 0}
    embed = discord.Embed(
        title="Shifumi - Pierre, Papier, Ciseaux",
        description="Choisis `pierre`, `papier`, ou `ciseaux` pour jouer ! Tape `!choisir [ton choix]`.",
        color=discord.Color.blue()
    )
    print("Commande !shifumi appelée.")
    await ctx.send(embed=embed)

# Commande pour faire un choix (pierre, papier ou ciseaux)
@bot.command(name='choisir')
async def choisir(ctx, choix: str):
    print(f"Commande !choisir appelée par {ctx.author.name} avec le choix {choix}")
    choix = choix.lower()
    
    # Vérification du choix de l'utilisateur
    if choix not in choices:
        await ctx.send("Choix invalide. Tu dois choisir entre `pierre`, `papier`, ou `ciseaux` !")
        return

    # Le bot fait un choix aléatoire
    bot_choice = random.choice(choices)

    # Initialiser le score si le joueur est nouveau
    if ctx.author.id not in scores:
        scores[ctx.author.id] = {"win": 0, "loss": 0, "draw": 0}

    # Déterminer le résultat
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
        scores["bot"]['win'] += 1

    # Créer un embed pour le résultat
    embed = discord.Embed(
        title="Shifumi - Résultat",
        color=discord.Color.green() if result == "Gagné" else discord.Color.red()
    )
    embed.add_field(name="Ton choix", value=choix, inline=True)
    embed.add_field(name="Choix du bot", value=bot_choice, inline=True)
    embed.add_field(name="Résultat", value=result, inline=False)
    embed.add_field(
        name="Ton score",
        value=f"Gagné: {scores[ctx.author.id]['win']}, Perdu: {scores[ctx.author.id]['loss']}, Égalité: {scores[ctx.author.id]['draw']}"
    )
    embed.set_footer(text="Tape `!Sscore` pour voir le classement actuel.")
    await ctx.send(embed=embed)

# Commande pour afficher les scores
@bot.command(name='Sscore')
async def scoreshifumi(ctx):
    sorted_scores = sorted(
        scores.items(),
        key=lambda x: (x[1]['win'], -x[1]['loss']),
        reverse=True
    )
    embed = discord.Embed(
        title="Tableau des Scores Shifumi",
        description="Voici le classement des meilleurs joueurs :",
        color=discord.Color.magenta()
    )
    for i, (user_id, score) in enumerate(sorted_scores, 1):
        user_name = "Bot" if user_id == "bot" else (await bot.fetch_user(user_id)).name
        embed.add_field(
            name=f"Top {i}",
            value=f"**{user_name}** - Gagné: {score['win']}, Perdu: {score['loss']}, Égalité: {score['draw']}",
            inline=False
        )
        if i >= 5:  # Limiter l'affichage aux 5 meilleurs
            break
    print("Commande !Sscore appelée.")
    await ctx.send(embed=embed)

# Démarrer le bot
bot.run(token)
