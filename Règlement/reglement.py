import discord
from discord.ext import commands, tasks
import os
import asyncio

# Définir les intents nécessaires pour le bot
intents = discord.Intents.default()
intents.message_content = True

# Initialisation du bot avec les intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Parties du règlement
reglement_part1 = """
**1️⃣ Français Seulement** :
Les membres ne peuvent parler qu'en français.

**2️⃣ Jurons** :
Les jurons sont interdits.

**3️⃣ Usurpation d'identité** :
Se faire passer pour quelqu'un est interdit.
"""

reglement_part2 = """
**4️⃣ Ne pas demander à être modérateur** :
Demander ou mendier pour être modérateur n'est pas autorisé. Pour devenir modérateur, vous devez être choisi ou postuler lorsque les candidatures sont ouvertes.

**5️⃣ Violation des règles de Discord ToS** :
Vous devez avoir 13 ans ou plus et ne pas enfreindre les conditions d'utilisation de Discord. Le faire pourrait entraîner un bannissement permanent et un signalement à Discord.

**6️⃣ Respectez tout le monde** :
Soyez gentil avec les autres, ne soyez pas impoli ou toxique.
"""

reglement_part3 = """
**7️⃣ Publicité** :
Pas de publicité dans le serveur et dans les messages privés.

**8️⃣ Racisme** :
Aucun racisme dans le serveur. Être raciste envers quelqu'un pourrait entraîner un bannissement.

**9️⃣ Pas de contenu NSFW** :
Le faire entraîne un bannissement permanent !
"""

reglement_part4 = """
**🔟 Partage d'informations personnelles** :
Aucun partage d'informations personnelles ! La confidentialité est très importante. Si quelqu'un demande des informations personnelles, ouvrez un ticket ou envoyez un message privé à un membre du personnel immédiatement !

**1️⃣1️⃣ Tout contenu lié à H*tler ou au nazisme** :
Tout contenu lié à H*tler ou au nazisme est un bannissement permanent.

**1️⃣2️⃣ Ne partagez pas de contenu qui glorifie ou promeut le suicide ou l'automutilation** :
Cela inclut toute incitation à se couper ou à adopter des troubles alimentaires tels que l'anorexie ou la boulimie.
"""

reglement_part5 = """
**1️⃣3️⃣ Veuillez ne pas abuser du format de texte large “#”**.

**1️⃣4️⃣ Pas de partage ou de jugement des opinions**.
"""

reglement_part6 = """
**_Enfreindre l'une des directives de Discord sera signalé à Discord, entraînant un bannissement permanent._**
"""

# Dictionnaire pour suivre les temps d'utilisation des commandes
cooldown_users = {}

# Durée de cooldown en secondes
COOLDOWN_DURATION = 30

# Commande pour afficher le règlement avec un cooldown
@bot.command()
async def reglement(ctx):
    current_time = asyncio.get_event_loop().time()
    user_id = ctx.message.author.id

    if user_id in cooldown_users:
        last_time = cooldown_users[user_id]
        if current_time - last_time < COOLDOWN_DURATION:
            wait_time = COOLDOWN_DURATION - (current_time - last_time)
            await ctx.send(f"Vous devez attendre {wait_time:.2f} secondes avant d'utiliser cette commande à nouveau.")
            return

    cooldown_users[user_id] = current_time

    embed = discord.Embed(title="Règlement du Serveur", color=discord.Color.blue())
    embed.add_field(name="", value=reglement_part1, inline=False)
    embed.add_field(name="", value=reglement_part2, inline=False)
    embed.add_field(name="", value=reglement_part3, inline=False)
    embed.add_field(name="", value=reglement_part4, inline=False)
    embed.add_field(name="", value=reglement_part5, inline=False)
    embed.add_field(name="Informations importantes", value=reglement_part6, inline=False)
    await ctx.send(embed=embed)

# Utilise la variable d'environnement pour le jeton
token = os.getenv('DISCORD_BOT_TOKEN')
if token:
    bot.run(token)
else:
    print("Erreur : Le jeton du bot Discord n'est pas défini")

print("Le bot est en train de démarrer...")

# Fin du bot règlement
