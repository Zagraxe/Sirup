import requests
import os

# URL de l'API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"

# Token API (injecté via les secrets GitHub)
API_TOKEN = os.getenv("DISCORD_IA_TOKEN")

# Fonction pour obtenir une réponse de l'API
def obtenir_reponse(prompt):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"  # Authentification via le token
    }
    payload = {
        "inputs": prompt,  # Message envoyé au modèle
        "options": {"wait_for_model": True}  # Attente si le modèle n'est pas chargé
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            print(f"Erreur API : {response.status_code}, {response.json()}")
            return "Je suis désolé, une erreur est survenue."
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API : {e}")
        return "Une erreur est survenue, veuillez réessayer plus tard."
