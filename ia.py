import requests
import os

# URL de l'API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
DISCORD_IA_TOKEN = os.getenv('DISCORD_IA_TOKEN')

# Vérifie que le token de l'IA est défini
if not DISCORD_IA_TOKEN:
    raise ValueError("Le token API Hugging Face est manquant. Définissez-le dans les variables d'environnement.")

def obtenir_reponse(prompt):
    """
    Appelle l'API Hugging Face avec le prompt donné et retourne la réponse générée.
    """
    headers = {"Authorization": f"Bearer {DISCORD_IA_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200},  # Limite la longueur de la réponse
        "options": {"wait_for_model": True}
    }

    try:
        # Envoi de la requête à l'API
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Vérifie les erreurs HTTP

        result = response.json()
        if result and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return "Désolé, je n'ai pas pu générer de réponse valide. Essaie encore !"
    except Exception as e:
        print(f"Erreur lors de l'appel à l'IA : {e}")
        return f"Une erreur est survenue : {str(e)}"
