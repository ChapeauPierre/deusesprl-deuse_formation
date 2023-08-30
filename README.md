# django-forum

Un mini-projet pour apprendre les bases en Django.

Plugins:

- [Django](https://www.djangoproject.com/)

- [django-webpack-loader](https://github.com/django-webpack/django-webpack-loader)

- [Django REST](https://www.django-rest-framework.org/)

- [React JS](https://reactjs.org/)

- [Flutter](https://docs.flutter.dev/)


## Développement Docker


### Installation Docker

Pour installer docker, il vous suffit de suivre la [documentation](https://docs.docker.com/engine/install/ubuntu/).

Pour installer docker-compose, il vous suffit de suivre la [documentation](https://docs.docker.com/compose/install/).


### Première utilisation

Pour lancer le projet localement sur votre machine de développement:

```sh
$ sudo nano /etc/hosts
# Ajouter la ligne "127.0.0.1       deuse-formation.local" dans le fichier
$ ./install_docker.sh docker-compose.yml
```

Vérifier que le projet se lance bien sur [http://deuse-formation.local/](http://deuse-formation.local/)


## Mail

Pour le developpement, nous redirigons tous nos emails sur une boïte mail [mailinator](https://www.mailinator.com).

Pour ce faire, vous pouvez suivre l'article Medium [Django et E-mail](https://medium.com/@duboisr/django-et-e-mail-eb9d9ac4503e).



## Projet

Ce mini-projet a été mis en place pour vous permettre de découvrir/apprendre/perfectionner les bases en Django.

Le design des pages se basera sur le thème d'Axel [github](https://github.com/AxelCardinaels/formation-html).

Pour aller plus vite, l'ensemble des templates sera déjà disponible dans l'app Django `main`.

Pour ce projet, je vais vous demander de créer un forum qui sera composé:

- D'une partie "compte utilisateur"

    - L'app Django `user`, le modèle et l'admin sont déja fournis.
    
    - Une page de login. Vous retrouverez le design de la page [ici](http://deuse-formation.local/login/) en vous inspirant de cet [article](https://learndjango.com/tutorials/django-login-and-logout-tutorial)
    
    - Une page de création de compte. Vous retrouverez le design de la page [ici](http://deuse-formation.local/register/) en vous inspirant de cet [article](https://learndjango.com/tutorials/django-signup-tutorial)
    
    - Des pages destinées au reset de mdp (avec envoi d'un mail). Vous retrouverez le design des pages en vous inspirant de cet [article](https://learndjango.com/tutorials/django-password-reset-tutorial):
    
    - D'une page profile pour mettre à jour les données du compte utilisateur. Vous retrouverez le design de la page [ici](http://deuse-formation.local/profile/user_pk/)

- D'une partie "forum"
    
    - Une page listant tous les sujets (Topics) créés. Ces derniers pourront être filtrés sur leur titre, leur statut et s'ils ont déjà eu des réponses. Vous retrouverez le design de la page [ici](http://deuse-formation.local/topics/)
    
    - Une page pour permettre la création d'un nouveau sujet. Attention, seuls les utilisateurs ayant un compte peuvent créer un nouveau sujet. Vous retrouverez le design de la page [ici](http://deuse-formation.local/topics/new/)
    
    - Une page pour répondre au sujet sélectionné. Attention, seuls les utilisateurs ayant un compte peuvent répondre, les autres ont un accès en lecture seul. De plus, si l'utilisateur connecté est le créateur du sujet, il doit y avoir un bouton permettre de clôturer le sujet. Vous retrouverez le design de la page [ici](http://deuse-formation.local/topics/topic_pk/)

Toutes ces pages sont disponibles à partir de la [homepage](http://deuse-formation.local/) du projet.

Pour la partie login/registration, n'hésitez pas à jeter un oeil au [Django's Built-in Login System](https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html).

Ce projet est commun à tous les sujets ci-dessous.


### Sujet 1: Créer un forum en Django (sans utiliser les classBasedViews)
Pour ce sujet, il suffit simplement de créer le forum sans utiliser les [classBasedViews](https://docs.djangoproject.com/fr/3.1/topics/class-based-views/).


### Sujet 2: Créer un forum en Django (avec les classBasedViews)
Pour ce sujet, il suffit simplement de recréer le forum en utilisant les [classBasedViews](https://docs.djangoproject.com/fr/3.1/topics/class-based-views/).

Vous pouvez consulter l'article suivant pour vous aider:

- [Django Doc](https://ccbv.co.uk/)


### Sujet 3: Créer un forum en Django Rest API + ReactJs
Pour ce sujet, il faut créer une simple page app en ReactJs ainsi que de mettre en place un API REST pour communiquer avec la BDD. Pour cela, il faut utiliser le [Django REST framework](https://www.django-rest-framework.org/).

Concernant la réalisation de l'application ReactJs, cette dernière se fera dans le dossier `app/assets/src/forum/`. L'ensemble des outils permettant l'intégration de l'app ReactJS dans un projet Django aura déjà été configuré.

Vous retrouverez un exemple d'integration d'un composant ReactJs dans une view Django [ici](http://deuse-formation.local/main/react/).

Vous pouvez consulter les articles suivants pour vous aider:

- [ReactJs](https://reactjs.org/docs/getting-started.html)

- [ReactJs 2](https://openclassrooms.com/fr/courses/7008001-debutez-avec-react)

- [ReactJs 3](https://openclassrooms.com/fr/courses/7150606-creez-une-application-react-complete)

- [Django REST](https://www.django-rest-framework.org/tutorial/quickstart/)

- [Django REST 2](https://openclassrooms.com/fr/courses/7192416-mettez-en-place-une-api-avec-django-rest-framework)

- [Django REST Doc](https://www.cdrf.co/3.12/rest_framework.generics/RetrieveAPIView.html#get_object)


### Sujet 4: Créer un forum en Django Rest API + Flutter
Pour ce sujet, il faut créer une application mobile en Flutter ainsi que de mettre en place un API REST pour communiquer avec la BDD. Pour cela, il faut utiliser le [Django REST framework](https://www.django-rest-framework.org/). Concernant la réalisation de l'application Flutter, cette dernière se fera dans le dossier `mobile/`.

Pour lancer l'application mobile, il vous suffit de faire la commande `./install_base_flutter_mvvm.sh` après avoir lancé un émulateur Android/Ios.

Vous pouvez consulter les articles listés dans notre StackOverflow Teams pour vous aider:

- [StackOverflow Teams](https://stackoverflowteams.com/c/deuse/questions/431)

- [Django REST](https://www.django-rest-framework.org/tutorial/quickstart/)

- [Django REST 2](https://openclassrooms.com/fr/courses/7192416-mettez-en-place-une-api-avec-django-rest-framework)

- [Django REST Doc](https://www.cdrf.co/3.12/rest_framework.generics/RetrieveAPIView.html#get_object)
