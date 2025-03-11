import requests
import os

# URL de l'API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
API_TOKEN = os.getenv("DISCORD_IA_TOKEN")

if not API_TOKEN:
    raise ValueError("Le token API Hugging Face est manquant. Assurez-vous qu'il est défini dans les variables d'environnement.")

def obtenir_reponse(prompt):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result[0].get("generated_text", "Aucune réponse générée.")
        else:
            print(f"Erreur API : {response.status_code}, {response.json()}")
            return "Je suis désolé, une erreur est survenue avec l'API."

    except Exception as e:
        error_message = f"Erreur lors de l'appel à l'API Hugging Face : {str(e)}"
        print(error_message)
        return "Une erreur est survenue. Contactez l'administrateur du bot pour plus d'informations."
