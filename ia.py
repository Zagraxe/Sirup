import requests
import os

# URL de l'API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"

# Token d'accès (récupéré via les secrets GitHub ou en local pour les tests)
API_TOKEN = os.getenv("DISCORD_IA_TOKEN")

# Fonction pour obtenir une réponse de l'API
def obtenir_reponse(prompt):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"  # Authentification avec le token
    }
    payload = {
        "inputs": prompt,  # Le message à envoyer au modèle
        "options": {"wait_for_model": True}  # Attendre le chargement si nécessaire
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            print(f"Erreur API : {response.status_code}, {response.json()}")
            return "Je suis désolé, une erreur est survenue lors de la génération de la réponse."
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API : {e}")
        return "Une erreur est survenue. Veuillez réessayer plus tard."
