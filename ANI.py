# Importations des modules externes
import tkinter as tk
from tkinter import StringVar, colorchooser, messagebox
import os, json, sys
from datetime import datetime
from PIL import ImageGrab, Image, ImageTk

class ANIMATION():
    def __init__(self, root):
        assets_path = get_assets_path()
        if not os.path.exists(assets_path):
            os.makedirs(assets_path)
            print(f"📁 Dossier {assets_path} créé. Ajoutez-y vos dossiers Avatar_<prenom>.")

        # Vérifie que le dossier data/ existe
        data_path = get_data_path()
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            print(f"📁 Dossier {data_path} créé.")

        self.label = {}
        self.radiobuttons = {}
        self.a = {} # Dictionnaire de frames contenant numéro, entrée et choix couleurs
        self.e = {i: "" for i in range(1, 7)}  # Initialise e[1] à e[6] # Dictionnaire d'entrées

        self.root = root 
        tk.Label(self.root, text=f"Animation d'un appel", 
                 font=("Comic Sans MS", 18)).pack(side=tk.TOP, pady=10)
        
        self.chemin = "put_avatar.json"

        # Simulation de l'appel avec différents personnages
        self.image_appel = tk.Frame(root, width=800, height=360, bg="black")
        self.image_appel.place(x=350, y=225)
    
        self.Avatar_L1 = tk.Label(master=self.image_appel)
        self.Avatar_L2 = tk.Label(master=self.image_appel)
        self.Avatar_L3 = tk.Label(master=self.image_appel)
        self.Avatar_L4 = tk.Label(master=self.image_appel)
        self.Avatar_L5 = tk.Label(master=self.image_appel)
        self.Avatar_L6 = tk.Label(master=self.image_appel)

        self.Avatar_1 = None
        self.Avatar_2 = None
        self.Avatar_3 = None
        self.Avatar_4 = None
        self.Avatar_5 = None
        self.Avatar_6 = None
    
        self.avatar = [self.Avatar_L1, self.Avatar_L2, self.Avatar_L3, self.Avatar_L4, self.Avatar_L5, self.Avatar_L6]
        for label in self.avatar:
            label.pack_propagate(False)

        self.données = lire_fichier_json("put_avatar.json")
        self.bg_colors = {i: "black" for i in range(1, 7)}
        
        self.avatarn = {self.e[1]: self.Avatar_1, self.e[2]: self.Avatar_2, self.e[3]: self.Avatar_3, 
                        self.e[4]: self.Avatar_4, self.e[5]: self.Avatar_5, self.e[6]: self.Avatar_6}
        self.frames = {self.e[1]: self.Avatar_L1, self.e[2]: self.Avatar_L2, self.e[3]: self.Avatar_L3, 
                        self.e[4]: self.Avatar_L4, self.e[5]: self.Avatar_L5, self.e[6]: self.Avatar_L6}

        self.value2 = StringVar()
        self.selected_person = StringVar()
        
        # Zone de modification
        self.ruban_outils = tk.Frame(self.root)
        self.ruban_outils.place(x=375, y=620)
        self.yeux = tk.Button(self.ruban_outils, bg=
        "white", fg="black", relief="groove",
            text="Yeux ouverts", font=("Comic Sans MS", 12), command=self.update_yeux)
        self.yeux.pack(side=tk.LEFT, padx=10)
        self.bouche = tk.Button(self.ruban_outils, bg="white", fg="black", relief="groove",
            text="Bouche (0)", font=("Comic Sans MS", 12), command=self.update_bouche)
        self.bouche.pack(side=tk.LEFT, padx=10)
        self.miroir = tk.Button(self.ruban_outils, bg="white", fg="black", relief="groove",
            text="Effet miroir désactivé", font=("Comic Sans MS", 12), command=self.update_miroir)
        self.miroir.pack(side=tk.LEFT, padx=10)
        screenshot = tk.Button(self.ruban_outils, bg="white", fg="black", relief="groove",
            text="Capture d'écran", font=("Comic Sans MS", 12), command=self.screenshot)
        screenshot.pack(side=tk.LEFT, padx=10)

        fermer = tk.Button(self.ruban_outils, bg="red", fg="white", relief="groove",
            text="Fermer", font=("Comic Sans MS", 12), command=lambda: self.root.destroy())
        fermer.pack(side=tk.LEFT, padx=10)

        # Zone de paramètres
        zone_para = tk.Frame(self.root)
        zone_para.place(x=50, y=100)
        tk.Label(zone_para, text=f"Définis les paramètres de l'appel:", font=("Comic Sans MS", 12)).pack(side=tk.TOP)
        text_id = tk.Label(zone_para, text=f"Nombre de personnes:", font=("Comic Sans MS", 12)).pack()
        for i in range(1, 7):
            self.radiobuttons[i]= tk.Radiobutton(zone_para, text=str(i), variable=self.value2, value=i, font=("Comic Sans MS", 12))
            self.radiobuttons[i].pack(anchor=tk.CENTER)
        self.value2.set("2")
        tk.Label(zone_para, text=f"Numero - Nom - Arrière-plan", font=("Comic Sans MS", 12)).pack()
        for i in range(1, 7):
            self.a[i] = tk.Frame(zone_para)
            self.a[i].pack(pady=5)
            tk.Label(self.a[i], text=str(i), font=("Comic Sans MS", 12)).pack(side=tk.LEFT, padx=5)
            self.e[i] = tk.Entry(self.a[i], textvariable=str, width=10, font=("Comic Sans MS", 12))
            self.e[i].pack(side=tk.LEFT)
            btn = tk.Button(
                self.a[i],
                text="bg",
                font=("Comic Sans MS", 12),
                fg="black",
                relief="groove",
                bg="white",
                command=lambda i=i: self.choose_bg_color(i)  # Passe l'index i
            )
            btn.pack(side=tk.LEFT, padx=5)
        tk.Button(zone_para, text="Valider", command=self.place_pers, font=("Comic Sans MS", 12), 
                  fg="black", relief="groove", bg="white").pack()

        # Zone de sélection
        self.zone_select = tk.Frame(self.root)
        self.zone_select.place(x=1225, y=150)
        tk.Label(self.zone_select, text=f"Sélectionner un personnage:", font=("Comic Sans MS", 12)).pack(side=tk.TOP)

        # Bouton aide :
        help_button = tk.Button(
            self.ruban_outils,
            text="Aide",
            font=("Comic Sans MS", 12),
            command=self.show_help
        )
        help_button.pack(side=tk.LEFT, padx=10)

    def show_help(self):
        help_text = """
        📌 Comment utiliser ce logiciel :

        1. Dans `assets/`, créez un dossier pour chaque oc :
        - Nom : `Avatar_<prenom>` (ex: `Avatar_Alice`).
        2. Dans chaque dossier, placez les images :
        - Ouverts.png, Fermés.png (les yeux)
        - 1.png, 2.png, 3.png (les bouches)

        Il faut que chaque image soit dans un format 533*460.
        Utilisez une application pour supprimer l'arrière plan de chaque image et pour les images des bouches, ne gardez que la bouche.

        3. Sélectionner le nombre de personnes dans l'appel
        4. Taper les prénoms dont vous avez besoin (Attention, ils doivent correspondre aux prénoms dans `Avatar_<prenom>`)
        5. Appuyer sur "Valider"
        6. Pour modifier les oc, sélectionner l'oc à gauche, puis appuyer sur les différents boutons (Yeux, Bouche, Miroir)
        7. Pour faire une capture d'écran, appuyer sur "Screenshots".

        """
        tk.messagebox.showinfo("Aide", help_text)

    def create_avatar(self, prenom: str):
        """Fonction permettant de mettre les avatars selon des caractéristiques
        Args:
            prenom: Nom du personnage (str).
        Returns:
            ImageTk.PhotoImage: Image combinée de l'avatar et de la bouche.
        """
        assets_path = get_assets_path()
        chemin_avatar_dir = os.path.join(assets_path, f"Avatar_{prenom}")

        # Vérifie que le dossier existe
        if not os.path.exists(chemin_avatar_dir):
            print(f"⚠️ Dossier introuvable : {chemin_avatar_dir}")
            # Retourne une image vide avec un message d'erreur
            img = Image.new("RGBA", (266, 230), (255, 0, 0, 255))  # Image rouge
            return ImageTk.PhotoImage(img)

        # Charge les données par défaut (si elles existent)
        type_yeux = self.données[prenom]["type_yeux"] # Valeur par défaut
        type_bouche = self.données[prenom]["type_bouche"]      # Valeur par défaut
        miroir = self.données[prenom]["miroir"]         # Valeur par défaut

        # Charge les images
        try:
            chemin_yeux = os.path.join(chemin_avatar_dir, f"{type_yeux}.png")
            if not os.path.exists(chemin_yeux):
                chemin_yeux = os.path.join(chemin_avatar_dir, "Ouverts.png")  # Essaye un nom alternatif
            Avatar = Image.open(chemin_yeux).convert("RGBA")
            Avatar = Avatar.resize((266, 230), Image.LANCZOS)
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement des yeux pour {prenom} : {e}")
            img = Image.new("RGBA", (266, 230), (255, 0, 0, 255))  # Image rouge
            return ImageTk.PhotoImage(img)

        # Ajoute la bouche si nécessaire
        if type_bouche != "0":
            try:
                chemin_bouche = os.path.join(chemin_avatar_dir, f"{type_bouche}.png")
                if not os.path.exists(chemin_bouche):
                    chemin_bouche = os.path.join(chemin_avatar_dir, f"{type_bouche}.png")  # Essaye un nom alternatif
                Bouche = Image.open(chemin_bouche).convert("RGBA")
                Bouche = Bouche.resize((266, 230), Image.LANCZOS)
                Avatar.paste(Bouche, (0, 0), Bouche)
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement de la bouche pour {prenom} : {e}")

        # Applique l'effet miroir si nécessaire
        if miroir == 1:
            Avatar = Avatar.transpose(Image.FLIP_LEFT_RIGHT)

        return ImageTk.PhotoImage(Avatar)

    def choose_bg_color(self, index):
        """Ouvre la boîte de dialogue pour choisir la couleur de fond de l'avatar."""
        color = choisir_couleur()
        if color:
            # Met à jour self.bg_colors
            self.bg_colors[index] = color

            # Récupère le prénom correspondant
            prenom = self.e[index].get()
            if not prenom:
                return  # Pas de prénom, on ne fait rien

            self.données[prenom]["bg"] = color

            # Sauvegarde le JSON
            ecrire_fichier_json(self.chemin, self.données)

            # Met à jour le bg du Label de l'avatar
            self.avatar[index-1].configure(bg=color)

            # Met à jour le bg de l'avatar affiché (Avatar_L1, Avatar_L2, etc.)
            if index == 1 and self.Avatar_1:
                self.Avatar_L1.configure(bg=color)
            elif index == 2 and self.Avatar_2:
                self.Avatar_L2.configure(bg=color)
            elif index == 3 and self.Avatar_3:
                self.Avatar_L3.configure(bg=color)
            elif index == 4 and self.Avatar_4:
                self.Avatar_L4.configure(bg=color)
            elif index == 5 and self.Avatar_5:
                self.Avatar_L5.configure(bg=color)
            elif index == 6 and self.Avatar_6:
                self.Avatar_L6.configure(bg=color)

    def screenshot(self):
        """
        Faire la capture d'écran de l'appel
        """
        self.root.update_idletasks()
        x = 440
        y = 285
        w = 1435
        h = 720

        screenshot = ImageGrab.grab(bbox=(x, y, w, h))
        now = datetime.now()
        new_now = now.strftime("%Y%m%d%H%M%S")
        che = fr"Screenshot_{new_now}_python.png"
        screenshot.save(che)

    def place_pers(self):
        """Selon le nombre de personnes, positionner les avatars."""
        self.refresh_avatars()
        # Efface les anciens avatars
        for label in self.avatar:
            label.place_forget()

        # Récupère les paramètres
        nb_pers = int(self.value2.get())
        wi = self.image_appel.winfo_width()
        hi = self.image_appel.winfo_height()
        list_entry = [self.e[i].get() for i in range(1, 7)]

        # Place les avatars en fonction du nombre de personnes
        if nb_pers <= 3:
            avatar_width = wi // nb_pers
            avatar_height = hi
        else:
            avatar_width = wi // 3
            avatar_height = hi // 2

        # Place les avatars
        if nb_pers >= 1 and list_entry[0]:
            self.Avatar_1 = self.create_avatar(list_entry[0])
            bg_color = self.données.get(list_entry[0], {}).get("bg", "black")
            self.bg_colors[1] = bg_color
            self.Avatar_L1.configure(
                bg=bg_color,
                image=self.Avatar_1,
                width=avatar_width,
                height=avatar_height,
                font=("Reem Kufi", 14),
                fg="white"
            )
            self.Avatar_L1.image = self.Avatar_1
            self.Avatar_L1.place(x=0, y=0)

        if nb_pers >= 2 and list_entry[1]:
            self.Avatar_2 = self.create_avatar(list_entry[1])
            bg_color = self.données.get(list_entry[1], {}).get("bg", "black")
            self.bg_colors[2] = bg_color
            self.Avatar_L2.configure(
                bg=bg_color,
                image=self.Avatar_2,
                width=avatar_width,
                height=avatar_height,
            )
            self.Avatar_L2.image = self.Avatar_2
            self.Avatar_L2.place(x=avatar_width, y=0)

        if nb_pers >= 3 and list_entry[2]:
            self.Avatar_3 = self.create_avatar(list_entry[2])
            bg_color = self.données.get(list_entry[2], {}).get("bg", "black")
            self.bg_colors[3] = bg_color
            self.Avatar_L3.configure(
                bg=bg_color,
                image=self.Avatar_3,
                width=avatar_width,
                height=avatar_height,
            )
            self.Avatar_L3.image = self.Avatar_3
            self.Avatar_L3.place(x=2 * avatar_width, y=0)

        # Pour 4+ personnes : deuxième ligne
        if nb_pers >= 4 and list_entry[3]:
            self.Avatar_4 = self.create_avatar(list_entry[3])
            bg_color = self.données.get(list_entry[3], {}).get("bg", "black")
            self.bg_colors[4] = bg_color
            self.Avatar_L4.configure(
                bg=bg_color,
                image=self.Avatar_4,
                width=avatar_width,
                height=avatar_height,
            )
            self.Avatar_L4.image = self.Avatar_4
            # Positionne en bas à gauche
            if nb_pers == 4:
                self.Avatar_L4.place(x=avatar_width//3, y=hi//2)
            elif nb_pers == 5:
                self.Avatar_L4.place(x=avatar_width-(avatar_width//2), y=hi//2)
            else:
                self.Avatar_L4.place(x=0, y=hi//2)
            
        if nb_pers >= 5 and list_entry[4]:
            self.Avatar_5 = self.create_avatar(list_entry[4])
            bg_color = self.données.get(list_entry[4], {}).get("bg", "black")
            self.bg_colors[5] = bg_color
            self.Avatar_L5.configure(
                bg=bg_color,
                image=self.Avatar_5,
                width=avatar_width,
                height=avatar_height,
            )
            self.Avatar_L5.image = self.Avatar_5
            # Positionne en bas au centre (pour 5 personnes)
            if nb_pers == 5:
                self.Avatar_L5.place(x=(avatar_width//2)+avatar_width, y=hi//2)
            else:
                self.Avatar_L5.place(x=avatar_width, y=hi//2)

        if nb_pers >= 6 and list_entry[5]:
            self.Avatar_6 = self.create_avatar(list_entry[5])
            bg_color = self.données.get(list_entry[5], {}).get("bg", "black")
            self.bg_colors[6] = bg_color
            self.Avatar_L6.configure(
                bg=bg_color,
                image=self.Avatar_6,
                width=avatar_width,
                height=avatar_height,
            )
            self.Avatar_L6.image = self.Avatar_6
            # Positionne en bas à droite
            self.Avatar_L6.place(x=2 * avatar_width, y=hi//2)
        # Met à jour la zone de sélection
        for widget in self.zone_select.winfo_children():
            widget.destroy()  # Efface les anciens radiobuttons

        tk.Label(
            self.zone_select,
            text="Sélectionner un personnage:",
            font=("Comic Sans MS", 12)
        ).pack(side=tk.TOP)

        for i in range(nb_pers):
            prenom = list_entry[i]
            if prenom:  # Si le prénom n'est pas vide
                tk.Radiobutton(
                    self.zone_select,
                    text=prenom,
                    variable=self.selected_person,
                    value=prenom,
                    font=("Comic Sans MS", 12)
                ).pack(anchor=tk.W)
                
        # Définit le premier personnage comme sélectionné par défaut
        if list_entry:
            self.selected_person.set(list_entry[0])

    def update_yeux(self):
        """Met à jour le type de yeux du personnage sélectionné."""
        nom = self.selected_person.get()
        if not nom:
            return

        # Trouve l'index du personnage
        list_entry = [self.e[i].get() for i in range(1, 7)]
        try:
            index = list_entry.index(nom)
        except ValueError:
            return

        # Trouve le Label correspondant
        avatar_label = self.avatar[index]

        # Met à jour les données
        text = self.yeux.cget("text")
        if text == "Yeux ouverts":
            self.données[nom]["type_yeux"] = "Fermés"
            self.yeux.config(text="Yeux fermés")
        elif text == "Yeux fermés":
            self.données[nom]["type_yeux"] = "Ouverts"
            self.yeux.config(text="Yeux ouverts")
        ecrire_fichier_json(self.chemin, self.données)

        # Recharge l'avatar
        bg_color = self.données.get(nom, {}).get("bg", "black")
        new_avatar = self.create_avatar(nom)
        avatar_label.configure(
            bg=bg_color, image=new_avatar,
        )
        avatar_label.image = new_avatar

    def update_bouche(self):
        """Met à jour le type de bouche du personnage sélectionné."""
        nom = self.selected_person.get()
        if not nom:
            return

        # Trouve l'index du personnage
        list_entry = [self.e[i].get() for i in range(1, 7)]
        try:
            index = list_entry.index(nom)
        except ValueError:
            return

        # Trouve le Label correspondant
        avatar_label = self.avatar[index]

        # Met à jour les données
        text = self.bouche.cget("text")
        if text == "Bouche (0)":
            self.données[nom]["type_bouche"] = "1"
            self.bouche.config(text="Bouche (1)")
        elif text == "Bouche (1)":
            self.données[nom]["type_bouche"] = "2"
            self.bouche.config(text="Bouche (2)")
        elif text == "Bouche (2)":
            self.données[nom]["type_bouche"] = "3"
            self.bouche.config(text="Bouche (3)")
        elif text == "Bouche (3)":
            self.données[nom]["type_bouche"] = "0"
            self.bouche.config(text="Bouche (0)")
        ecrire_fichier_json(self.chemin, self.données)

        # Recharge l'avatar
        bg_color = self.données.get(nom, {}).get("bg", "black")
        new_avatar = self.create_avatar(nom)
        avatar_label.configure(
            bg=bg_color, image=new_avatar,
        )
        avatar_label.image = new_avatar

    def update_miroir(self):
        """Active ou désactive l'effet miroir du personnage sélectionné."""
        nom = self.selected_person.get()
        if not nom:
            return

        # Trouve l'index du personnage
        list_entry = [self.e[i].get() for i in range(1, 7)]
        try:
            index = list_entry.index(nom)
        except ValueError:
            return

        # Trouve le Label correspondant
        avatar_label = self.avatar[index]

        # Met à jour les données
        text = self.miroir.cget("text")
        if text == "Effet miroir désactivé":
            self.données[nom]["miroir"] = 1
            self.miroir.config(text="Effet miroir activé")
        elif text == "Effet miroir activé":
            self.données[nom]["miroir"] = 0
            self.miroir.config(text="Effet miroir désactivé")
        ecrire_fichier_json(self.chemin, self.données)

        # Recharge l'avatar
        bg_color = self.données.get(nom, {}).get("bg", "black")
        new_avatar = self.create_avatar(nom)
        avatar_label.configure(
            bg=bg_color, image=new_avatar,
        )
        avatar_label.image = new_avatar

    def refresh_avatars(self):
        """Recharge les avatars pour les personnages actuels."""
        nb_pers = int(self.value2.get())
        list_entry = [self.e[i].get() for i in range(1, 7)]

        for i in range(nb_pers):
            prenom = list_entry[i]
            if not prenom:
                continue

            # Charge ou initialise les données pour ce prénom
            if prenom not in self.données:
                self.données[prenom] = {
                    "type_yeux": "Ouverts",
                    "type_bouche": "0",
                    "miroir": 0,
                    "bg": "black"
                }
                ecrire_fichier_json("put_avatar.json", self.données)

            # Recharge l'avatar
            avatar_img = self.create_avatar(prenom)

            # Met à jour le Label de l'avatar
            self.avatar[i].configure(
                image=avatar_img,
                bg=self.données[prenom].get("bg", "black")
            )
            self.avatar[i].image = avatar_img

def get_assets_path():
    """Retourne le chemin du dossier assets/ relatif à l'exécutable."""
    if getattr(sys, 'frozen', False):
        # Si on est dans un exécutable (PyInstaller)
        application_path = sys.executable
    else:
        # Si on est dans un script Python
        application_path = os.path.abspath(__file__)
    return os.path.join(os.path.dirname(application_path), "assets")

def get_data_path():
    """Retourne le chemin du dossier data/ relatif à l'exécutable."""
    if getattr(sys, 'frozen', False):
        application_path = sys.executable
    else:
        application_path = os.path.abspath(__file__)
    data_path = os.path.join(os.path.dirname(application_path), "data")
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path

def ecrire_fichier_json(chemin_fichier, donnees):
    try:
        with open(chemin_fichier, "w", encoding="utf-8") as fichier:
            json.dump(donnees, fichier, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erreur : {e}")

def lire_fichier_json(chemin_fichier):
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
            donnees = json.load(fichier)
        return donnees
    except FileNotFoundError:
        print(f"Erreur : Le fichier {chemin_fichier} n'a pas été trouvé.")
        return {}
    except Exception as e:
        print(f"Erreur : {e}")
        return {}

def choisir_couleur():
    """
    Ouvre la boîte de dialogue de choix de couleur et applique la couleur choisie
    au fond de la fenêtre.
    Args:
        root: fenêtre.
        color: texte vide avec couleur choisie.
    """
    try:
        # Ouvre le sélecteur de couleur
        couleur = colorchooser.askcolor(title="Choisissez une couleur")

        # couleur est un tuple : ((R, G, B), "#rrggbb")
        if couleur[1] is None:
            messagebox.showinfo("Info", "Aucune couleur sélectionnée.")
            return

        rgb, hex_code = couleur

        # Appliquer la couleur choisie au fond de la fenêtre
        return hex_code
    
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


if __name__ == "__main__":
    mod = tk.Tk()
    mod.geometry("+0+0")
    mod.title("Module pour animer un appel")
    mod.attributes("-fullscreen", False)
    app = ANIMATION(mod)
    mod.mainloop()