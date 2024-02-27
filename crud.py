import mysql.connector
from mysql.connector import Error
from datetime import datetime

def connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='python'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None



def create_langage(nom, level, date, username):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO language (nom,date_creation,level) VALUES (%s,%s,%s)"
            cursor.execute(query, (nom,date,level))
            conn.commit()
            print(f"User '{nom}' added successfully.")
            log_action(f"L'utilisateur {username} a ajouté un langage : {nom}")
        except Error as e:
            print(f"Erreur lors de l'ajout de l'utilisateur: {e}")
        finally:
            cursor.close()
            conn.close()


def delete_langage(language_id, username):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM language WHERE id = %s"
            cursor.execute(query, (language_id,))
            conn.commit()
            print(f"User ID {language_id} has been deleted.")
            log_action(f"L'utilisateur {username} a supprimé un langage avec l'ID : {language_id}")
        except Error as e:
            print(f"Erreur lors de la suppression de l'utilisateur: {e}")
        finally:
            cursor.close()
            conn.close()

def update_user(langage_id,name,date_creation,level, username):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            if name != None and date_creation != None and level != None:
                query = "UPDATE language SET nom = %s, date_creation = %s, level = %s WHERE id = %s"
                cursor.execute(query, (name, date_creation,level,langage_id,))
                conn.commit()
                print(f"User ID {langage_id} has been updated to '{name}'.")
                log_action(f"L'utilisateur {username} a mis à jour le langage : {name} avec l'ID : {langage_id}")
            elif  name != None and date_creation != None and level == None:
                print("kfjgkfjgkfjgkfgjkfgjf")
                query = "UPDATE language SET nom = %s, date_creation = %s WHERE id = %s"
                cursor.execute(query, (name, date_creation, langage_id,))
                conn.commit()
                print(f"User ID {langage_id} has been updated to '{name}'.")
                log_action(f"L'utilisateur {username} a mis à jour le langage : {name} avec l'ID : {langage_id}")
            elif  name != None and date_creation == None and level == None:
                query = "UPDATE language SET nom = %s WHERE id = %s"
                cursor.execute(query, (name,  langage_id,))
                conn.commit()
                print(f"User ID {langage_id} has been updated to '{name}'.")
                log_action(f"L'utilisateur {username} a mis à jour le langage : {name} avec l'ID : {langage_id}")
        except Error as e:
            print(f"Erreur lors de la mise à jour de l'utilisateur: {e}")
        finally:
            cursor.close()
            conn.close()

def all_languages():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nom, date_creation FROM language")
            print()
            languages = cursor.fetchall()  # Fetch all rows from the cursor
            for language in languages:
                print(f"Nom : {language[0]}, Date : {language[1]}")
        except mysql.connector.Error as e:
            print(f"Erreur SQL lors de la lecture des langages: {e}")
            return None
        finally:
            conn.close()  # Close the connection when done with it
    else:
        print("Erreur de connexion à la base de données.")
        return None

def check_user_exists(username):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM user WHERE nom = %s"
            cursor.execute(query, (username,))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"Erreur lors de la recherche de l'utilisateur: {e}")
            return False
        finally:
            conn.close()

def log_action(message):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO log (message, timestamp) VALUES (%s, %s)"
            cursor.execute(query, (message, datetime.now()))
            conn.commit()
            print("Action logged successfully.")
        except Error as e:
            print(f"Erreur lors de la journalisation de l'action: {e}")
        finally:
            cursor.close()
            conn.close()

def display_logs():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT message, timestamp FROM log")
            logs = cursor.fetchall()
            print("Logs :")
            for log in logs:
                print(f"Message : {log[0]}, Date : {log[1]}")
        except Error as e:
            print(f"Erreur lors de la lecture des logs: {e}")
        finally:
            conn.close()

def menu(username):
    while True:
        print("\nMenu :")
        print("1. Ajouter un langage")
        print("2. Modifier un langage")
        print("3. Supprimer un langage")
        print("4. Afficher tous les languages")
        print("5. Afficher les logs")
        print("6. Quitter")

        choice = input("Choisissez une option : ")

        if choice == "1":
            add_language(username)
        elif choice == "2":
            update_language(username)
        elif choice == "3":
            delete_language(username)
        elif choice == "4":
            all_languages()
        elif choice == "5":
            display_logs()
        elif choice == "6":
            print("Au revoir.")
            break
        else:
            print("Option invalide.")

def add_language(username):
    language_name = input("Entrez le nom du langage que vous souhaitez ajouter : ")
    language_level = input("Entrez le niveau du langage : ")
    language_date = input("Entrez la date de création du langage : ")
    create_langage(language_name, language_level, language_date, username)

def update_language(username):
    all_languages()
    language_id = input("Entrez l'ID du langage que vous souhaitez modifier : ")
    language_name = input("Entrez le nouveau nom du langage (ou laissez vide pour ne pas modifier) : ")
    language_date = input("Entrez la nouvelle date de création du langage (ou laissez vide pour ne pas modifier) : ")
    language_level = input("Entrez le nouveau niveau du langage (ou laissez vide pour ne pas modifier) : ")
    update_user(language_id, language_name, language_date, language_level, username)

def delete_language(username):
    all_languages()
    language_id = input("Entrez l'ID du langage que vous souhaitez supprimer : ")
    delete_langage(language_id, username)

username = input("Entrez votre nom d'utilisateur : ")
if check_user_exists(username):
    menu(username)
else:
    print("Utilisateur non trouvé.")