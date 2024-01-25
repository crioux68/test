#Script pour extraire les emplois correspondants à nos préférences 
#du site du Cégep et qui nous envoie le résultat par email
#
#Importer les modules nécessaires pour faire du Web Scraping
#

#conflit?


import requests
from bs4 import BeautifulSoup
#pour le email
import smtplib, ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#définir le site qu'on va examiner
URL = "https://cegepgim.ca/offres-emploi/"
#définir les mots clés qu'on recherche, défini comme une liste
Filtre = ["éolienne","foresterie","infirmier","test"]
#Borel borel borel borel borel borel borel borel borel bonjour
x = 2 + 2
print(x)
def main(): 
    ###### Main ######
    #extraire le contenu de la page
    Page = requests.get(URL)
    Resultats = BeautifulSoup(Page.content, "html.parser")
 

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
                EmploiDetail+=Campus.text.strip()+"<br>\n"
                EmploiDetail+="Plus de détails: <a href='"+Lien_url+"'>"+Lien_url+"</a></li>\n\n"
                Jobs.append(EmploiDetail) #Ajouter à la liste
            
    Jobs.append("\n</ul>")  #Fermer la balise UserList

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

    # Je sais pas trop à quoi cela sert :/
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

#Ceci est un commentaire douteux d'un padawan de la programmation.
#Reset
if __name__ == "__main__":
    main()

#La ligne suivante de williamb est complètement inutile