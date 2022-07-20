#Tests E2E du logiciel Scodoc

Ces jeux de tests ont été conçus pour tester automatiquement Scodoc d'un point de vue E2E (End to End). Ils sont en théorie indépendants les uns des autres. Ils ont étés développés en python 3.
## I Configuration
Dans cette partie je vais détailler les prérequis pour l'environnement de développement
### Prérequis Module
Ces prérequis peuvent être trouvés dans requirements.txt qui se trouvent à la base du projet.
Vous devez avoir pip d'installé, normalement il est fourni avec les versions de python3, sinon vous trouverez les étapes d'installation [ici](https://pip.pypa.io/en/stable/installing/)
Les modules suivant sont nécessaire :
>selenium==3.141.0
>python-dotenv==0.17.1
>HtmlTestRunner==0.8.0

Vous pouvez les installer manuellement avec pip avec la commande suivante :
>pip install selenium

ou alternativement avec 
>pip install -r requirements.txt
### Environnement de test
Un modèle de .env est fourni dans ce projet, pour que les tests soient fonctionnel vous devez le remplir et le renommer en .env. Ce dernier servira à remplir différentes informations spécifiques concernant votre environnement Scodoc. Nous allons le voir ici en détail
#### .env

>BASE_URL = "https://scodoc-dev-iutinfo.univ-lille.fr/ScoDoc/"

Ici sera le lien vers la page d'accueil de votre Scodoc

>NOM_DPT = "test01"

Le nom du département surlequel vous allez effectuer vos tests, il est **FORTEMENT** conseillés de mettre ici un nom de département qui n'existe pas, sous risque de perte de données.

>SCODOC_ADMIN_ID = "admin_id"

Le nom d'utilisateur d'un Admin Scodoc.

>SCODOC_ADMIN_PASS = "admin_password"

Le mot de passe d'un Admin Scodoc.

>SCODOC_ENS_ID = "enseignant_id"

Le nom d'utilisateur d'un enseignant lambda qui servira pour rentrer des notes, soit qui existe, soit qui sera créé.

>SCODOC_ENS_PASS = "enseignant_password@10"

Le mot de passe de l'utilisateur précédent, si l'utilisateur précédent n'existe pas, veillez à avoir un mot de passe suffisamenent compliqué pour la création de ce dernier.

>SCODOC_CHEF_ID = "chef_id"

Le nom d'utilisateur d'un enseignant lambda qui se verra attribué le rôle de résponsable d'un module afin de créer des interrogations , soit qui existe, soit qui sera créé.

>SCODOC_CHEF_PASS = "p@ssword42@"

Le mot de passe de l'utilisateur précédent, si l'utilisateur précédent n'existe pas, veillez à avoir un mot de passe suffisamenent compliqué pour la 

>LINK_SCODOC_SERVER = "root@ssh_server_scodoc"

Le lien vers votre serveur Scodoc, ce dernier servira à lancer des scripts de mise en place sur le serveur. Veillez donc à avoir une connexion avec les droits root sur votre serveur, de préférences avec échange de clef ssh.

>BASE_NOT_SECURED_URL = "scodoc-dev-iutinfo.univ-lille.fr/"

Le lien vers la page de choix de département, avec le format précisé.

>NAVIGATEUR = "firefox"

Ici vous pouvez choisir entre firefox et chrome,choisissez le navigateur dans lequel vous voulez que vos tests se déroulent. Cette ligne permettra au programme de choisir le webdriver correspondant.

#### Explications du fonctionnement des tests

Les tests sont prévus pour fonctionner avec firefox ou chrome les webdrivers sont intégrés dans le projet pour éviter de devoir les installer manuellement. Ces webdrivers servent à faire la connexion entre python et le navigateur. 

##Lancement des tests

Pour lancer les tests, assurez vous d'avoir une connexion possible avec votre serveur. Positionnez vous à la racine de ce projet et il suffit donc de lancer la commande par exemple pour le premier jeux de tests

>python3 01_creation_departement_test.py

Alternativement vous pouvez lancer l'ensemble des tests avec la commande

>./lancement_de_tout_les_tests.sh

L'option --c ou --cleanup est disponible si vous souhaitez effacer tout les rapports précédents

###Resultats des tests

Les tests sont présentés sur une page HTML qui se trouve dans le dossier ResultatTest, il y a une page HTML par jeux de tests créée. Un récapitulatif est également créé par le biais du script

>./scriptGenerateReportPage.sh

Celui ci est lancé automatiquement à la fin du script

>./lancement_de_tout_les_tests.sh

Vous y retrouverez les liens menant au détails de chaque rapport ainsi qu'un résumé du nombre de test passés/échoués