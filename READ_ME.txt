Comment utilser notre code.

Il suffit de lancer le fichier Display.py avec python3.
Il est important que ce fichier simulation.py soit dans le m�me r�pertoire que Diplay.py.

Une fois le programme lanc�, une fen�tre avec plusieurs param�tre est affich�.

Largeur et Hauteur d�finissent les dimensions de l'environnement o� se d�roulera la simulation.
�chelle n'est qu'un facteur qui d�fini la taille de la fen�tre d'affichage. Cela d�pend de la taille de l'�cran de l'utilisateur.

Le nombre de cr�atures d�finit le nombre de cr�atures initiales au premier jour tout simplement. Nombre de jours � simuler indique apr�s
combien de jour la simulation doit s'arr�ter. A noter que si l'affichage dynamique est activ�, la simulation peut �tre continu�e.
Dur�e d'une heure d�fini un time.sleep entre les mouvements des cr�atures sur l'affichage dynamique. Dur�e d'une journ�e d�fini le nombre
d'heures par jour.

Affichage dynamique d�fini simplement quand est-ce qu'une journ�e est affich�e.

Rapport de nourriture d�fini le nombre de nourriture � faire apparaitre chaque jour. Rapport de pr�dation d�fini �) partir de quelle
diff�rence de taille les cr�atures peuvent se manger. Plus c'est �lev�, plus il est difficile pour les cr�atures de se manger. A d�finir
entre 0 et 1 compris.

Formule de consomation d�fini la mani�re dont les cr�atures consomment de la nourriture chaque heures.

Mutations autoris�es d�fini quelles variables peuvent �voluer.

Attention, si l'affichage graphique est activ�, veiller � cliquer sur la fen�tre pour ensuite appuyer sur s pour commencer la simulation.

Nous avons essay� d'int�ger un maximum de personnalisation dans la fonction mais nous encourageons l'utilisateur � modifier les lignes de
codes si d'autres conditions initiales lui semblent int�ressante.