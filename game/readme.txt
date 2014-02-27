game.py : main
après l'initialisation on entre dans la boucle qui affiche les frames du jeu
cette boucles se dicises en trois étapes :
    - entrées utilisateur
    - évolution du monde (entre autre en fonction des précédentes entrées)
    - rendue (on dessine l'écran)
    
l'évolution du monde et normalement exclusivement géré dans l'update des différents objets qui constituent le monde


pour le moment les collision sont gérer par les objet eux-mêmes dans la méthode collide
(qui doit donc être implémenter pour chaque sprite) ce mécanisme est à mettre en concurence avec l'utilisation de groupcollide
dans ce deusième mécanisme les objets serait sans doute moins complexe et les group de sprite plus utilisé (voir des exemples)


TODO :

 - hierarchy de class pour les item

 - pour les mobs
 
 