import os
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

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
intents.members = True
intents.message_content = True

# Initialisation du bot avec les intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Nous sommes connectés en tant que {bot.user}')
    print(f'ID du bot: {bot.user.id}')

@bot.event
async def on_member_join(member):
    print("Nouveau membre détecté!")
    await send_welcome_message(member)

@bot.command()
@commands.has_permissions(administrator=True)  # Restriction aux administrateurs
async def testewelcom(ctx):
    if ctx.author.guild_permissions.administrator:
        print("Commande de test exécutée!")
        await send_welcome_message(ctx.author)
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")

async def send_welcome_message(member):
    print(f"Envoi du message de bienvenue pour {member.display_name}")
    # Utiliser l'ID réel du canal
    channel_id = 123456789012345678  # Remplace '123456789012345678' par l'ID de ton canal
    channel = bot.get_channel(channel_id)

    if channel is not None:
        print("Téléchargement de l'avatar...")
        avatar_url = member.display_avatar.url
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA")

        # Créer un masque circulaire parfait pour l'avatar
        mask = Image.new('L', (70, 70), 0)  # Créer une image en niveaux de gris de 70x70 pixels
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 70, 70), fill=255)  # Dessiner un cercle plein

        # Appliquer le masque à l'avatar et redimensionner
        avatar = avatar.resize((70, 70))
        avatar.putalpha(mask)  # Appliquer le masque pour rendre l'avatar circulaire

        print("Création de l'image de bienvenue...")
        background = Image.open('bienvenu/Roboto.png').convert("RGBA")

        # Positionner l'avatar à la position (20, 10)
        avatar_x = 20
        avatar_y = 10

        # Ajouter l'avatar sur l'arrière-plan
        background.paste(avatar, (avatar_x, avatar_y), avatar)

        # Ajouter le texte du pseudo à la position (115, 25)
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype('bienvenu/Roboto-Bold.ttf', 45)
        text = member.display_name

        # Positionner le texte selon les nouvelles coordonnées (115, 25)
        text_x = 115
        text_y = 25

        # Dessiner le texte en blanc brillant
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

        background.save('welcome.png')

        print("Envoi du message de bienvenue...")
        embed = discord.Embed(color=0x8aa8aa)  # Vert d'eau doux
        embed.set_image(url="attachment://welcome.png")
        embed.description = f'Bienvenue parmi nous, {member.mention} !'
        await channel.send(embed=embed, file=discord.File('welcome.png'))
    else:
        print("Canal non trouvé.")

bot.run(token)
