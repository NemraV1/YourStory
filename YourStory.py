import tkinter as tk
import os
import pygame
from pygame import mixer
import openai

# Initialisation de Pygame Mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Clé d'API OpenAI (remplacez par votre propre clé)
openai.api_key = "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"

# Fonction pour générer une histoire avec OpenAI
def generate_story():
    # Texte de départ pour l'interaction avec GPT-3.5 Turbo
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a story."}
    ]

    # Demandez à GPT-3.5 Turbo de générer la suite de l'histoire
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=100  # Vous pouvez ajuster ce nombre en fonction de la longueur souhaitée de l'histoire
    )

    # Obtenez la réponse générée par GPT-3.5 Turbo
    story_text = response.choices[0].message["content"]

    # Affichez le texte de l'histoire petit à petit à l'écran
    display_story(story_text)

# Fonction pour afficher l'histoire petit à petit
def display_story(story_text):
    # Affichez le texte de l'histoire petit à petit à l'écran
    story_label.config(text="", font=("Arial", 14), padx=20, pady=20, bg="black", fg="white")
    story_label.pack(side="top", fill="x")

    # Divisez le texte en plusieurs morceaux
    story_parts = story_text.split("\n")

    # Fonction pour afficher chaque morceau
    def display_next_part(part_index):
        if part_index < len(story_parts):
            story_label.config(text=story_parts[part_index])
            root.after(2000, lambda: display_next_part(part_index + 1))
        else:
            # L'histoire est terminée, affichez à nouveau les boutons
            play_button.pack(side="top", pady=10)
            credits_button.pack(side="top", pady=10)
            exit_button.pack(side="top", pady=10)
            language_button.pack(side="top", anchor="ne", padx=10, pady=10)

    display_next_part(0)

# Fonction pour afficher les crédits
def show_credits():
    # Ajoutez ici le code pour afficher les crédits lorsque le bouton "Crédits" est pressé
    # Par exemple, vous pouvez créer une nouvelle fenêtre avec les crédits
    credits_window = tk.Toplevel(root)
    credits_window.title("Crédits")
    credits_window.geometry("400x300")
    credits_label = tk.Label(credits_window, text="Crédits:\n\nDéveloppé par [Votre nom]\nMusique par [Nom de l'artiste]\n\n© 2023", font=("Arial", 14))
    credits_label.pack(expand=True)

# Fonction pour sélectionner la langue
def on_language_select():
    selected_language = language_var.get()
    if selected_language == "Français":
        label.config(text="Bienvenue dans le jeu !", font=("Arial", 24))
        language_var.set("English")  # Permet le changement en anglais
    else:
        label.config(text="Welcome to the game!", font=("Arial", 24))
        language_var.set("Français")  # Permet le changement en français

# Fonction pour démarrer le jeu
def start_game():
    # Supprimez les boutons du menu
    play_button.pack_forget()
    credits_button.pack_forget()
    exit_button.pack_forget()
    language_button.pack_forget()

    # Chargez l'image de fond de l'histoire
    story_background_image_path = os.path.join(current_directory, "Background5.png")
    story_bg_image = tk.PhotoImage(file=story_background_image_path)

    # Affichez l'image de fond de l'histoire
    story_bg_label = tk.Label(root, image=story_bg_image)
    story_bg_label.place(relwidth=1, relheight=1)

    # Générez et affichez l'histoire
    generate_story()

# Le reste du code reste inchangé...

# Obtenez le chemin absolu du fichier courant
current_directory = os.path.dirname(os.path.abspath(__file__))
background_image_path = os.path.join(current_directory, "Background4.png")

# Créez la fenêtre principale
root = tk.Tk()
root.title("Jeu de rôle interactif")
root.geometry("1920x1080")  # Ajustez la taille de la fenêtre selon vos préférences

# Fond personnalisé
bg_image = tk.PhotoImage(file=background_image_path)
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)  # Remplit toute la fenêtre

# Étiquette de bienvenue
label = tk.Label(root, text="", font=("Arial", 24), padx=20, pady=20, bg="black", fg="white")
label.pack(side="top", fill="x")

# Bouton pour sélectionner la langue
language_var = tk.StringVar()
language_var.set("Français")  # Langue par défaut
language_button = tk.Button(root, textvariable=language_var, command=on_language_select, font=("Arial", 12, "bold"), bg="black", fg="white", borderwidth=0, relief="solid", cursor="hand2")
language_button.pack(side="top", anchor="ne", padx=10, pady=10)

# Lecture de la musique de fond
mixer.music.load("MusicBackground.mp3")  # Assurez-vous que le fichier "MusicBackground.mp3" est dans la racine du projet
mixer.music.play(-1)  # Joue en boucle

# Boutons du menu
menu_frame = tk.Frame(root, bg="#1E90FF")  # Utilisez la couleur "#1E90FF" pour l'arrière-plan
menu_frame.place(relx=0.5, rely=0.5, anchor="center")

# Boutons avec police "Arial" (comme précédemment)
font = ("Arial", 16, "bold")

play_button = tk.Button(menu_frame, text="Play", command=start_game, font=font, bg="#1E90FF", fg="white", borderwidth=0, relief="solid", cursor="hand2")
credits_button = tk.Button(menu_frame, text="Crédits", command=show_credits, font=font, bg="#1E90FF", fg="white", borderwidth=0, relief="solid", cursor="hand2")
exit_button = tk.Button(menu_frame, text="Exit", command=root.quit, font=font, bg="#1E90FF", fg="white", borderwidth=0, relief="solid", cursor="hand2")

play_button.config(width=10, height=2, padx=10, pady=5)  # Ajustez la taille des boutons et l'espacement
credits_button.config(width=10, height=2, padx=10, pady=5)
exit_button.config(width=10, height=2, padx=10, pady=5)

play_button.pack(side="top", pady=10)
credits_button.pack(side="top", pady=10)
exit_button.pack(side="top", pady=10)

root.mainloop()
