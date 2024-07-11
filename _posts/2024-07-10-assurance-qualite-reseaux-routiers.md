---
layout: post
title: "Améliorer la continuité des réseaux routiers dans un SIG : quelques méthodes"
date: 2024-07-10 19:00:00 +0300
categories: gis
---

Les données sur les réseaux routiers sont essentielles pour planifier des trajets entre différents lieux. Cependant, la présence de nombreuses discontinuités dans le réseau peut entraîner des résultats d’analyse inattendus. Il existe des méthodes d’analyse permettant d’évaluer la qualité des données routières et de détecter les erreurs potentielles dans la continuité du réseau. Dans cet article, nous détaillerons trois méthodes pour assurer la qualité des réseaux routiers : la recherche des îles flottantes, l'identification des groupes presque connectés, et la détection des anomalies avec les isolignes de distances.

## Recherche des îles flottantes

Les îles flottantes (ou composantes isolées) dans un réseau routier sont des segments de voies qui ne sont pas connectés au réseau principal. Ces discontinuités peuvent entraîner des problèmes de navigation et d’analyse des trajets. Il est donc crucial de les identifier et de les résoudre pour assurer la continuité et la fiabilité du réseau. Voici un exemple de procédure :

- **Créer une topologie et assigner un ID unique à chaque groupe de chemins connectés :** L’objectif est d’analyser le réseau routier pour identifier les segments connectés entre eux. Des outils comme le transformateur **[TopologyBuilder](http://docs.safe.com/fme/html/FME-Form-Documentation/FME-Transformers/Transformers/topologybuilder.htm)** dans FME ou l'outil GRASS **[v.net.components](https://grass.osgeo.org/grass83/manuals/v.net.components.html)** dans QGIS permettent de réaliser cette tâche. Utilisez une couche linéaire représentant le réseau routier pour produire une autre couche linéaire des segments de route, avec un attribut identifiant chaque groupe de segments connectés. Notez que pour utiliser l'outil GRASS **v.net.components**, les lignes doivent être découpées aux intersections. Sinon, utilisez l'outil QGIS **[Couper avec des lignes](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#qgissplitwithlines)** en utilisant la même couche, pour les découper.
- **Dissoudre toutes les lignes connectées ayant le même ID :** Cette étape consiste à regrouper toutes les lignes ayant le même ID de groupe en une seule entité. Utilisez l’outil **[Regrouper](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#qgisdissolve)** dans QGIS, en spécifiant comme champ de regroupement celui qui contient l'ID du groupe. Cela facilite la sélection et l’analyse des groupes de segments connectés.
- **Identifier les réseaux principaux :** Identifiez visuellement sur la carte le ou les groupes constituant le réseau principal. Les autres groupes sont considérés comme non connectés. Par exemple, créez un attribut booléen (oui/non) pour différencier ces groupes.
- **Extraire les groupes qui ne sont pas connectés aux réseaux principaux :** Utilisez l’attribut booléen précédemment créé pour différencier le réseau principal du reste. Vérifiez chaque groupe non connecté individuellement afin de déterminer s’il peut être connecté au réseau principal.

<figure>
<img src="/img/road-network-comps.png" style="zoom:33%;" />
<figcaption>Segments de voies coloriés par l'identifiant du groupe. Les composantes "8" constituent le réseau principal et les autres sont des composantes isolées.</figcaption>
</figure>

## Identification des groupes presque connectés

Cette analyse vise à identifier les composantes isolées de voies qui se trouvent à une distance seuil définie par rapport au groupe voisin. Voici les étapes de procédure :

- **Créer une topologie et assigner un ID unique à chaque groupe de chemins connectés**, comme dans l'exemple de procédure précédent.
- **Extraire les nœuds de départ et de fin** de chaque segment de voie. L'outil **[Extraire des sommets spécifiques](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#qgisextractspecificvertices)** permet de le faire, en spécifiant comme index de sommets "0, -1".
- **Extraire les nœuds isolés**, c’est-à-dire les nœuds sans superposition avec d’autres nœuds, correspondant aux extrémités des chemins sans issue. Utilisez l’outil **[Joindre les attributs par localisation (résumé)](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#qgisjoinbylocationsummary)** de QGIS pour compter le nombre de nœuds distincts superposés sur la même couche de points. Comme "Champs à résumer", choisissez n'importe quel attribut et comme "Résumés à calculer", choisissez "compte". Retenez les nœuds qui n’ont pas de superposition (compte = 1) pour l’étape suivante.
- **Créer des tampons autour de ces nœuds isolés**, en utilisant la distance désirée, par exemple 100 mètres. Utilisez l’outil **[Tampon](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#buffer)** dans QGIS et cochez les options "Regrouper le résultat" et "Garder les entités disjointes séparées" pour fusionner les tampons superposés en une entité.
- **Compter les valeurs distinctes d’ID de réseau dans chaque polygone obtenu :** Les polygones (tampons fusionnés) contenant deux valeurs d’ID de réseau différentes ou plus indiquent des groupes de chemins qui sont proches mais non connectés. Utilisez l'outil **[Joindre les attributs par localisation (résumé)](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#qgisjoinbylocationsummary)** pour compter les valeurs distinctes d'ID à partir des nœuds qui intersectent chaque polygone. Les polygones ayant deux valeurs uniques ou plus doivent être vérifiés et, si possible, connectés pour améliorer la continuité du réseau.

<figure>
<img src="/img/almost-connected-ways.png" style="zoom:33%;" />
<figcaption>Composantes presque connectées : les endroits en rouge, où il y a plusieurs IDs de groupe distincts, sont probablement à connecter.</figcaption>
</figure>

## Détection des anomalies avec les isolignes de distances

Cette analyse vise à détecter les anomalies potentielles dans la continuité du réseau routier en examinant les distances 2D le long des chemins à partir de points choisis. Chaque segment du réseau se voit attribuer une valeur de distance. Les nœuds finaux sont ensuite analysés pour identifier ceux qui, bien que proches, présentent des écarts de distance significatifs, ce qui pourrait indiquer une anomalie. Voici la procédure :

- **Créer une topologie et assigner un ID unique à chaque groupe de chemins connectés**, comme dans les exemples de procédure précédents.
- **Découper les lignes selon des isolignes de distance.** Choisissez des points de départ et créez des isolignes de distance depuis ces points de départ. L’outil GRASS **[v.net.iso](https://grass.osgeo.org/grass83/manuals/v.net.iso.html)** permet de réaliser cette tâche. Paramètres recommandés :
   - "Couche de ligne en entrée (arcs)" : la couche du réseau routier avec topologie et IDs de groupe.
   - "Couche de points de centres (nœuds)" : la couche des points de départ.
   - "Seuil pour connecter les centres au réseau" : définissez un seuil de distance pour ancrer les points de départ au réseau.
   - "Coûts des isolignes" : spécifiez les distances consécutives (par exemple, "1000, 2000, 3000, 4000, 5000").
- **Extraire les nœuds de départ et de fin**, comme dans la procédure précédente.
- **Extraire les nœuds isolés**, correspondant aux extrémités des chemins sans issue, comme dans la procédure précédente.
- **Créer des tampons autour des nœuds isolés** dans une distance choisie (par exemple 100 m), comme dans la procédure précédente.
- **Analyser les écarts de distance :** Les écarts de distance dans le réseau entre les nœuds voisins peuvent être détectés en analysant le contraste entre les catégories de distance dans chaque polygone (max – min ou écart type). Pour ce faire :
   - Convertissez la couche de lignes issue de l’étape 2 en nœuds, par exemple avec l’outil QGIS **[Extraire les sommets](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#qgisextractvertices)**;
   - Utilisez l’outil **Joindre les attributs par localisation (résumé)** pour joindre aux polygones des tampons les écarts des distances. Les polygones ayant des écarts importants entre "max" et "min" sont à vérifier, car ils peuvent indiquer des tronçons mal connectés rendant la déviation énorme.

<figure>
<img src="/img/road-network-isodistance-anomaly.png" style="zoom:66%;" />
<figcaption>Possible endroit à connecter. Il y a un écart de 10 km de parcours entre les nœuds encadrés en rouge (La différence entre 6 et 1 est 5, et les catégories ici sont à intervalle de 2 km à partir de Soavina, donc une distance de 5 x 2 km).</figcaption>
</figure>

## Conclusion

En suivant ces méthodes d’analyse, vous pouvez améliorer la qualité des réseaux routiers en identifiant et en résolvant les discontinuités. Cela assure une meilleure navigation et des analyses de trajet plus précises, augmentant ainsi la fiabilité des données routières. Utilisez des outils SIG libres comme QGIS pour faciliter ces processus et garantir un réseau routier continu et efficace.
