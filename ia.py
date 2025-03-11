import requests
import os

# URL de l'API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
DISCORD_IA_TOKEN = os.getenv("DISCORD_IA_TOKEN")  # Utilise le nom correct

if not DISCORD_IA_TOKEN:
    raise ValueError("Le token API Hugging Face est manquant. Assurez-vous qu'il est défini dans les variables d'environnement.")

def obtenir_reponse(prompt):
    headers = {
        "Authorization": f"Bearer {DISCORD_IA_TOKEN}"  # Utilise la bonne variable
    }
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        print(f"Statut API : {response.status_code}")  # Log du statut HTTP
        print(f"Réponse brute : {response.text}")  # Log de la réponse brute

        if response.status_code == 200:
            result = response.json()
            return result[0].get("generated_text", "Aucune réponse générée.")
        else:
            print(f"Erreur API : {response.status_code}, {response.json()}")
            return f"Je suis désolé, une erreur est survenue avec l'API : {response.status_code}."

    except Exception as e:
        print(f"Erreur lors de l'appel à l'API : {e}")  # Log des exceptions
        return f"Une erreur est survenue avec l'API : {e}"
