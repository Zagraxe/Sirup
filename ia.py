import requests
import os

# URL de l'API Hugging Face pour le modèle Bloom
API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
DISCORD_IA_TOKEN = os.getenv("DISCORD_IA_TOKEN")  # Token API Hugging Face depuis les variables d'environnement

# Vérifie si le token est défini
if not DISCORD_IA_TOKEN:
    raise ValueError("Le token API Hugging Face est manquant. Assurez-vous qu'il est défini dans les variables d'environnement.")

def obtenir_reponse(prompt):
    """
    Appelle l'API Hugging Face avec le prompt donné et retourne la réponse générée.
    Gère les erreurs et vérifie les réponses vides.
    """
    headers = {
        "Authorization": f"Bearer {DISCORD_IA_TOKEN}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200},  # Permet des réponses détaillées
        "options": {"wait_for_model": True}  # Attend que le modèle soit prêt
    }

    try:
        # Appel à l'API Hugging Face
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Logs pour le débogage
        print(f"Statut API : {response.status_code}")
        print(f"Réponse brute : {response.text}")

        # Vérifie si la réponse est réussie
        if response.status_code == 200:
            try:
                result = response.json()
                # Vérifie que la réponse contient le texte généré
                if result and "generated_text" in result[0]:
                    response_text = result[0]["generated_text"]
                    # Vérifie si la réponse est identique au prompt
                    if response_text.strip() == prompt.strip():
                        return "Je suis désolé, je n'ai pas compris. Peux-tu reformuler ?"
                    return response_text
                else:
                    return "L'API n'a pas généré de texte valide. Réessaie plus tard."
            except ValueError as e:
                print(f"Erreur lors du parsing JSON : {e}")
                return "Une erreur est survenue lors de l'analyse de la réponse de l'IA."
        else:
            # Gestion des erreurs de l'API
            print(f"Erreur API : {response.status_code}, {response.text}")
            return f"Erreur API : {response.status_code}. Message : {response.text}"

    except Exception as e:
        # Gestion des exceptions critiques
        print(f"Erreur critique lors de l'appel à l'API : {e}")
        return f"Une erreur critique est survenue lors de la connexion à l'API : {e}"
