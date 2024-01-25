#Script pour extraire les emplois efsafsdafasdfasdfsd df sdfsa asfsdafcorrespondants à nos préférences 
#du site du Cégep et qui nous envoie le résultds sd sdaf sd fsdat par email
#
#Importer les modules nécessaires pour faire du Wf sd sd sadfsdfsfseb Scraping
#

#conflit?sdfs s df 


import requests
from bs4 import BeautifulSoup
#pour le email
import smtplib, ssl
from email.message import EmailMessage
import pygame
import math
import colorsys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


print("texte")

#définir le site qu'on va examiner
URL = "https://cegepgim.ca/offres-emploi/"
#définir les mots clés qu'on recherche, défini comme une liste
Filtre = ["éolienne","foresterie","infirmier","test"]
#Borel borel borel borel borel borel borel borel borel bonjour
x = 15
#compte  jusquà x+10
for i in range(x, x+10):
    print(i)
print(x)
def main(): 
    print("étagère")
    ###### Main ######
    #extraire le contenu de la page
    Page = requests.get(URL)
    #La ligne suivante de williamb est complètement inutile
    Resultats = BeautifulSoup(Page.content, "html.parser")

    print("Hello World")
 

    #Examiner le contenu pour identifier les éléments qui nous pointent vers les informations
    #Dans le cas présent, une é.tude de la page nous a donné que la balise <DIV> a une classe "card-content" qui identifie les emplois
    Job_elements = Resultats.find_all("div", class_="card-content")

    #Dans chacune de ces sections, on extrait les éléments qui nous intéressent.  
    #Ici on a identifié que :
    #la balise <h2 class_="card-title title-4"> contient le titre de l'emploi
    #la balise <p class_="info"> contient la date et le numéro de l'affichage
    #la balise <p class_="campus-list icon-marker"> contient le campus
    #la balise <a contient le lien

    #initialiser la variable qui sert à construire notre liste
    Jobs=["<ul>\n"] #<UL> = UserList, balise HTML pour faire des listes avec "bullets"
    #extraire les informations pour chaque emploi
    for job_element in Job_elements:
        Titre = job_element.find("h2", class_="card-title title-4")
        Date = job_element.find("p", class_="info")
        Campus=job_element.find("p", class_="campus-list icon-marker")
        Lien = job_element.find("a")
        Lien_url = Lien["href"]
       
        #est-ce que cet emploi correspond à nos mots clés?
        #(tout comparer en minuscules pour s'assurer de ne rien manquer)
        #if any(x in Titre.text for x in Filtre):
        for Motclé in Filtre:
            if Motclé.lower() in Titre.text.lower():
                #Ajouter l'emploi à notre liste, en format HTML.  (<LI> = List Item, identifie un élement de la UserList)
                print (Titre.text)
                # string EmploiDetail
                EmploiDetail="<li><b>"+Titre.text.strip()+"</b><br>\n"
                EmploiDetail+=Date.text.strip()+"<br>\n"
                #La ligne suivante de williamb est complètement inutile
                EmploiDetail+=Campus.text.strip()+"<br>\n"
                EmploiDetail+="Plus de détails: <a href='"+Lien_url+"'>"+Lien_url+"</a></li>\n\n"
                Jobs.append(EmploiDetail) #Ajouter à la liste
            
    Jobs.append("\n</ul>")  #Fermer la balise UserList

    print(Jobs)
    #Envoyer le résultat par GMAIL
    #Avec GMAIL, depuis peu, il est beaucoup plus complexe d'envoyer des emails avec un script
    #Ils ont sécurisé grandement leurs API.  #La façon la MOINS COMPLIQUÉE est d'activer le 2 Steps authentication 
    #et de créer un mot de passe "application".  
    #Mais une fois activée votre Compte Gmail va dorénavant demander une 2e autentification
    #Référence: https://leimao.github.io/blog/2022-12-29-Python-Send-Gmail/
    #Pour les besoins de l'exercice, je vous recommande de créer un compte GMAIL à part

    port = 465  # Pour port SMTP SSL, port courriel sécurisé
    smtp_server = "smtp.gmail.com" #Adresse du serveur
    sender_email = "pcq.gaspe@gmail.com"  # Nom d'un compte qui est configuré avec 2 Steps authentication et mot de passe "application"
    receiver_email = "christianrioux69@gmail.com"  # Compte qui va recevoir le résultat
    with open("GoogleAPI.txt",'r') as file:
        password=file.read()
    #password = "pupfcpqeowakqyy" #Mot de passe "application" généré par Google

    msg = EmailMessage()
    msg['Subject'] = "Emplois CegepGIM"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Le magnifique donut
    pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
hue = 0

WIDTH = 1920
HEIGHT = 1080

x_start, y_start = 0, 0

x_separator = 10
y_separator = 20

rows = HEIGHT // y_separator
columns = WIDTH // x_separator
screen_size = rows * columns

x_offset = columns / 2
y_offset = rows / 2

A, B = 0, 0  # rotating animation

theta_spacing = 10
phi_spacing = 1 # for faster rotation change to 2, 3 or more, but first change 86, 87 lines as commented

chars = ".,-~:;=!*#$@"  # luminance index

screen = pygame.display.set_mode((WIDTH, HEIGHT))

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
# display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Donut')
font = pygame.font.SysFont('Arial', 18, bold=True)

def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def text_display(letter, x_start, y_start):
    text = font.render(str(letter), True, hsv2rgb(hue, 1, 1))
    display_surface.blit(text, (x_start, y_start))

# def text_display(letter, x_start, y_start):
#     text = font.render(str(letter), True, white)
#     display_surface.blit(text, (x_start, y_start))


run = True
while run:

    screen.fill((black))

    z = [0] * screen_size  # Donut. Fills donut space
    b = [' '] * screen_size  # Background. Fills empty space

    for j in range(0, 628, theta_spacing):  # from 0 to 2pi
        for i in range(0, 628, phi_spacing):  # from 0 to 2pi
            c = math.sin(i)
            d = math.cos(j)
            e = math.sin(A)
            f = math.sin(j)
            g = math.cos(A)
            h = d + 2
            D = 1 / (c * h * e + f * g + 5)
            l = math.cos(i)
            m = math.cos(B)
            n = math.sin(B)
            t = c * h * g - f * e
            x = int(x_offset + 40 * D * (l * h * m - t * n))  # 3D x coordinate after rotation
            y = int(y_offset + 20 * D * (l * h * n + t * m))  # 3D y coordinate after rotation
            o = int(x + columns * y)  
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))  # luminance index
            if rows > y and y > 0 and x > 0 and columns > x and D > z[o]:
                z[o] = D
                b[o] = chars[N if N > 0 else 0]

    if y_start == rows * y_separator - y_separator:
        y_start = 0

    for i in range(len(b)):
        A += 0.00004  # for faster rotation change to bigger value
        B += 0.00002  # for faster rotation change to bigger value
        if i == 0 or i % columns:
            text_display(b[i], x_start, y_start)
            x_start += x_separator
        else:
            y_start += y_separator
            x_start = 0
            text_display(b[i], x_start, y_start)
            x_start += x_separator


    pygame.display.update()

    hue += 0.005

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    #fin du magnifique donut

    #La longueur de Jobs est égale a 2 quand il est "vide", puisqu'il y a les balises d'ouveture et fermeture de <UL>
    if len(Jobs)==2: #Aucun Emploi qui correspond au filtre
        print ("Pas d'emploi intéressant aujourd'hui")
        exit()
        
    #Contenu HTML est une variable pour construire le message en format HTML
    ContenuHTML = "<html>Emploi(s) correspondant(s) à vos mots-clé: ("+','.join(Filtre)+")<br>\n"
    for Ligne in Jobs:
        ContenuHTML+=Ligne #Ajouter à la variable qui construit le texte en HTML
    ContenuHTML+="</html>" #Fin du code html

    #Afficher le contenu en texte à l'écran aussi

    #Envoyer le message
    msg = MIMEMultipart('alternative')
    message = MIMEText(ContenuHTML, 'html')
    msg.attach(message)
    msg['Subject'] = "Emplois CegepGIM"
    print(msg)

    # Je sais pas trop à quoi cela sert :/
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

#Ceci est un commentaire douteux d'un padawan de la programmation.
#Les tardigrades (Tardigrada), parfois surnommés oursons d'eau, forment un
#embranchement du règne animal, regroupé avec les arthropodes et les 
#onychophores au sein du clade des panarthropodes
#Reset
if __name__ == "__main__":
    main()

#La ligne suivante de williamb est complètement inutile