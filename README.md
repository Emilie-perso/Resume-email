# Resume-email

L'objectif de ce projet est de résumer les e-mails reçus sur votre boîte mail outlook uniquement. 
Il consiste en une API développée en Python avec le framework FastAPI. 

Si jamais vous voulez le tester voici la marche à suivre : 

#Etape 1 : 

Cloner le projet 

#Etape 2 :

Activer l'environnement virtuel Python avec la commande resume/Scripts/activate 

Si vous êtes sous Windows et n'arrivez pas à activer l'environnement virtuel, il faut activer la lecture de script sous windows.Je vous renvoie vers ce lien 

https://www.informatique-mania.com/windows/comment-activer-lexecution-de-scripts-powershell-dans-windows-10/

#Etape 3 : 

Dans le fichier fonctions.py, dans la fonction read_mail , changer les variables username et password en mettant vos identifiants pour outlook.

#Etapa 4 : 

Lancer l'API avec la commande : uvicorn main:app --reload

# Etape 5 :

Cliquez sur le lien qui s'affiche dans votre terminal.
Vous aurez votre résumé !

Remarque : 
Le projet est toujours en cours de construction et d'amélioration
