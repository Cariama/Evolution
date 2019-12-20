Comment utilser notre code.

Il suffit de lancer le fichier Display.py avec python3.
Il est important que ce fichier simulation.py soit dans le même répertoire que Diplay.py.

Une fois le programme lancé, une fenêtre avec plusieurs paramètre est affiché.

Largeur et Hauteur définissent les dimensions de l'environnement où se déroulera la simulation.
échelle n'est qu'un facteur qui défini la taille de la fenêtre d'affichage. Cela dépend de la taille de l'écran de l'utilisateur.

Le nombre de créatures définit le nombre de créatures initiales au premier jour tout simplement. Nombre de jours à simuler indique après
combien de jour la simulation doit s'arrêter. A noter que si l'affichage dynamique est activé, la simulation peut être continuée.
Durée d'une heure défini un time.sleep entre les mouvements des créatures sur l'affichage dynamique. Durée d'une journée défini le nombre
d'heures par jour.

Affichage dynamique défini simplement quand est-ce qu'une journée est affichée.

Rapport de nourriture défini le nombre de nourriture à faire apparaitre chaque jour. Rapport de prédation défini à) partir de quelle
différence de taille les créatures peuvent se manger. Plus c'est élevé, plus il est difficile pour les créatures de se manger. A définir
entre 0 et 1 compris.

Formule de consomation défini la manière dont les créatures consomment de la nourriture chaque heures.

Mutations autorisées défini quelles variables peuvent évoluer.

Attention, si l'affichage graphique est activé, veiller à cliquer sur la fenêtre pour ensuite appuyer sur s pour commencer la simulation.

Nous avons essayé d'intéger un maximum de personnalisation dans la fonction mais nous encourageons l'utilisateur à modifier les lignes de
codes si d'autres conditions initiales lui semblent intéressante.