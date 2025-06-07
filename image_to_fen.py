from PIL import Image
from chess_diagram_to_fen import get_fen
import os
import time
import sys
import pyperclip  # Ajout du module pour le presse-papiers

def watch_directory(directory_path):
    # Ensemble pour stocker les fichiers déjà vus
    processed_files = set()

    while True:
        try:
            # Liste tous les fichiers du répertoire
            current_files = set(os.listdir(directory_path))

            # Vérifie les nouveaux fichiers par rapport à ceux déjà traités
            new_files = current_files - processed_files

            for filename in new_files:
                # Vérifie si le fichier est une image
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    file_path = os.path.join(directory_path, filename)

                    # Attend que le fichier soit complètement écrit
                    time.sleep(1)

                    try:
                        # Ouvre et traite l'image
                        img = Image.open(file_path)
                        result = get_fen(
                            img=img,
                            num_tries=10,
                            auto_rotate_image=True,
                            auto_rotate_board=True
                        )
                        # Copie le FEN dans le presse-papiers
                        pyperclip.copy(result.fen)
                        print(f"FEN pour {filename}: {result.fen} (copié dans le presse-papiers)")

                        # Ajoute le fichier à ceux déjà traités
                        processed_files.add(filename)

                    except Exception as e:
                        print(f"Erreur lors du traitement de {filename}: {str(e)}")

        except Exception as e:
            print(f"Erreur lors de la surveillance du répertoire: {str(e)}")

        # Pause avant la prochaine vérification
        time.sleep(2)

if __name__ == "__main__":
    # Vérifie si un paramètre a été passé
    if len(sys.argv) != 2:
        print("Utilisation: python script.py chemin/vers/repertoire")
        sys.exit(1)

    directory_to_watch = sys.argv[1]

    # Vérifie si le répertoire existe
    if not os.path.exists(directory_to_watch):
        print(f"Le répertoire '{directory_to_watch}' n'existe pas!")
        sys.exit(1)

    print(f"Surveillance du répertoire: {directory_to_watch}")
    watch_directory(directory_to_watch)
