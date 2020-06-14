---
layout: post
title: "Consignes de cartographie OpenStreetMap"
date: 2020-06-06 16:30:00 +0300
categories: gis
---

Cet article cerne des consignes et des exemples spécifiques pour aider ceux qui cartographient à distance dans le cadre de l'activité de cartographie d'Operation Fistula à Madagascar. Il couvre les éléments cartographiques suivants: les bâtiments, les voies de communication et l'hydrographie. Il est assumé que l'éditeur OpenStreetMap utilisé est JOSM.

Les illustrations, s'ils ne sont pas de mon propre travail, sont de Wikimedia Commons.

## À propos de l’imagerie

Plusieurs imageries sont disponibles pour fond, mais les plus utilisées pour Madagascar sont Bing Aerial Imagery et Maxar (Standard ou Premium) Imagery. Bing est fréquemment utilisée pour sa clarté et le fait qu'elle est l'imagerie par défaut dans l'éditeur OpenStreetMap iD; Maxar est moins claire mais est l'imagerie la plus récente disponible gratuitement.

<img src="/img/bing_v_maxar.png" style="zoom:67%;" />

La plus grande difficulté dans l'utilisation des imageries est la gestion de leur géoréférencement. Les règles générales d'OpenStreetMap s'appliquent: utiliser des tracés GPS pour bien aligner l'imagerie, aligner avec les données existantes [^1]. Il est également fréquent de devoir réaligner certaines imageries quand on change de lieu car celles-ci ne se superposent pas à l'imagerie de référence ou aux données existantes.

Au cours de la cartographie, il est pratique de basculer fréquemment entre diverses imageries pour mieux identifier les éléments à cartographier. Par exemple, si les contours d'un bâtiment ne sont pas du tout clairs dans l'imagerie Maxar, essayer de basculer vers Bing ou d'autres imageries. Dans JOSM, le raccourci par défaut pour rapidement basculer entre les imageries est la touche "~". Ce raccourci peut être modifié dans les paramètres.

## Cartographier les bâtiments

L'ajout des bâtiments prend la majeure partie du temps dans une tache de cartographie. En dehors des agglomérations, ça prend beaucoup de temps d'identifier chaque petit bâtiment éparpillé. Dans les agglomérations où le bâti est dense, il faut beaucoup d'effort pour identifier et dessiner chacun des bâtiments collés entre eux.

Diverses techniques pour dessiner correctement les bâtiments sont développées [ici](https://wiki.openstreetmap.org/wiki/Roof_modelling).

Dans les régions Sava et Vatovavy Fitovinany, la plupart des bâtiments ont des formes rectangulaires ou en "L". Ces formes de bâtiments peuvent être rapidement ajoutées à l'aide des outils *building tools* et extrusion de JOSM. 

### Building tools

Dans JOSM *building tools* vient avec l'extension du même nom et s'active avec le raccourci "B". Il permet de dessiner rapidement un bâtiment rectangulaire avec un attribut par défaut `building=yes`. 

Consignes:

- Suivre la longueur du bâtiment puis extruder suivant la largeur
- Commencer par le côté qui est collé à un autre bâtiment pour éviter une superposition des bâtiments
- Maintenir la touche ctrl en dessinant pour désactiver l'accrochage automatique (utile pour des bâtiments très rapprochés mais qui ne se collent pas)

<img src="/img/glued_buildings.gif" style="zoom: 50%;" />

### Extrusion

L'outil extrusion permet d'extruder (avancer/reculer) des facettes de polygones, permettant d'obtenir rapidement des bâtiments de formes orthogonales plus complexes. C'est un outil intégré à JOSM, accessible via le raccourci "X".

<img src="/img/extrusion.gif" style="zoom: 67%;" />

## Cartographier les voies de communication

La donnée des voies de communication est fondamentale dans toute analyse sur l'accessibilité de chaque localité: peut-on y aller, par quel moyen s'y rendre, combien de temps pour y arriver. Cette donnée joue un rôle important dans l'organisation des déplacements sur le terrain.  Ainsi il faut cartographier les voies de communication avec soin et vigilance.

### Dessiner correctement les chemins et les routes

Étant des entités OpenStreetMap linéaires, les routes et les chemins devraient être dessinés suivant leur axe central. Les règles de bonne pratique d’OpenStreetMap s’appliquent: dessiner une route rectiligne avec une ligne droite (sans nœuds intermédiaires), lisser les virages en utilisant un nombre approprié de nœuds pour ne pas avoir des angles prononcés [^2].

<img src="/img/road_nodes.png" style="zoom: 67%;" />

Éviter de:

- accrocher une route aux bordures des bâtiments
- accrocher une route à une zone d'occupation du sol (champs de culture, plan d'eau, forêt, zone résidentielle...)

<img src="/img/road_ricefield.png" style="zoom: 67%;" />

Essayer de:

-  connecter toute section de route et de chemin au réseau routier général, c’est-à-dire que ce chemin ou cette route devrait à un certain moment aboutir à la route principale desservant la commune/la région/le pays
- connecter les routes de part et d'autre d'un village/hameau
- déduire si une section de chemin ou de route passe à travers une forêt mais cette section n’est pas visible avec l’imagerie. Si oui, tracer grossièrement la partie traversant la forêt

### Hiérarchiser correctement le réseau routier

Les voies de communications sont à hiérarchiser suivant leur dimension économique et social [^3].

| Catégorie                     | Attribut                 | Dimension économique et sociale                              |
| ----------------------------- | ------------------------ | ------------------------------------------------------------ |
| Route primaire                | `highway=primary`      | Routes desservant les plus grandes villes du pays, les chefs-lieux de province |
| Route secondaire              | `highway=secondary`    | Routes desservant les capitales régionales                   |
| Route tertiaire               | `highway=tertiary`     | Routes principales desservant les communes. Généralement, ce sont les routes empruntées par les taxi-brousses. |
| Route mineure                 | `highway=unclassified` | Routes ne servant pas au transit (pas de taxi-brousse), desservant des petits villages |
| Rues des zones résidentielles | `highway=residential`  | Rues desservant plusieurs maisons dans une ville ou dans un grand village |
| Voies d'accès                 | `highway=service`      | Voies menant à une propriété, à un parking ou à une zone industrielle |
| Pistes                        | `highway=track`        | Pistes carrossables servant d'accès à une forêt ou à une zone agricole. Généralement ces pistes ne sont utilisées que par des camions, des tracteurs ou des charrettes. |
| Chemins                       | `highway=path`         | Voies non accessibles aux véhicules à 4 roues, empruntées par les piétons et les véhicules à deux roues (motos et bicyclettes) |

Logiquement, une route quelconque devrait sortir quelque part vers une route de plus grande dimension dans le réseau routier, et non l'inverse.

À partir d’une imagerie, il est souvent difficile de déduire l’importance d’une route, si c’est une route mineure ou une route tertiaire. Il est également difficile de voir si la voie est carrossable ou non, la largeur à elle seule ne permet pas de le déduire (un chemin peut être aussi large pour contenir une voiture mais n’est pas empruntable à voiture dans la vérité). Les rues des zones résidentielles et les pistes quant à elles sont relativement plus faciles à déduire.

## Cartographier les éléments de l'hydrographie

### Les cours d'eau

Les mêmes bonnes pratiques que les routes et chemins s'appliquent quand on dessine des cours d'eau: pas trop de nœuds non nécessaires mais aussi pas d'angles prononcés. La ligne devrait relier les parties les plus profondes de la rivière. 

Le sens de la ligne doit **suivre le sens de l'écoulement de l'eau**: si on a dessiné le cours d'eau d'aval en amont il faudra inverser le sens de la ligne (raccourci "R" pour JOSM). Quand il est difficile de voir avec l'imagerie dans quel sens l'eau coule, l'ajout d'un calque contenant des courbes de niveau comme *OpenCycleMap* ou *OpenTopoMap* peut aider. Dans JOSM, la symbologie des lignes contient des flèches qui permettent de voir le sens suivant lequel ces lignes ont été dessinées.

Dans la plupart des cas, on aura: des ruisseaux, des fossés, des rivières et parfois des canaux.

#### Les ruisseaux  

Attribut: `waterway=stream`. Les ruisseaux sont de petits cours d'eau peu profonds et assez étroits, partant d'une source d'eau naturelle. On peut probablement sauter par-dessus. Quand il passe par une zone de rizières, un ruisseau peut être artificiellement canalisé et sera ainsi cartographié comme un **fossé**.

<img src="/img/stream.png" style="zoom: 67%;" />

#### Les fossés

Attribut: `waterway=ditch`. Un fossé est une petite dépression creusée (naturellement ou artificiellement) qui canalise l'eau, utilisée pour drainer les terres environnantes ou pour évacuer les eaux pluviales. Ces fossés se rencontrent souvent sur les bordures des parcelles de rizières.

<img src="/img/ditch.png" style="zoom:67%;" />

#### Les rivières 

Attribut: `waterway=river`. Les rivières sont des cours d'eau plus développés que forment les ruisseaux qui se rejoignent. Une rivière se déverse dans une autre rivière, dans la mer ou dans un plan d'eau endoréique (et jamais dans un ruisseau ou un fossé).

Quand une rivière est assez étroite (moins de 12 mètres de largeur), on la cartographie avec une ligne passant par ses parties les plus profondes. Quand la rivière est assez large (plus de 12 mètres de largeur), on met en plus de la ligne un polygone (ou un multipolygone s'il y a des îlots) délimitant l'**étendue de l'eau** et portant les attributs `natural=water` et `water=river` [^4].

<img src="/img/river_mapping.png" style="zoom:67%;" />

#### Les canaux 

Attribut: `waterway=canal`. On parle ici de cours d'eau artificiels assez larges servant de voie de transport (par exemple, le canal des Pangalanes). 

### Les plans d'eau et les zones humides

Les plans d'eau et les zones humides se cartographient évidemment avec un polygone. Certains mappers peuvent trouver l'extension [FastDraw](https://wiki.openstreetmap.org/wiki/JOSM/Plugins/FastDraw) de JOSM efficace pour dessiner ces éléments.

#### Les plans d'eau

Les surfaces d'eau naturelle peuvent être une rivière, un étang, un lac, un lac artificiel... L'étendue d'eau est dessinée avec un polygone avec l'attribut `natural=water`. Le type du plan d'eau, si connu, peut être précisé avec la clé `water=*` dont la valeur est  `river` pour une rivière, `pond` pour un étang, `lake` pour un lac, `reservoir` pour un lac artificiel. Voir [la page wiki de la clé `water=*`](https://wiki.openstreetmap.org/wiki/FR:Key:water)  pour d'autres valeurs.

<img src="/img/water_bodies.png" style="zoom:67%;" />

#### Les zones humides

Les zones humides sont des zones naturellement inondées ou avec un sol gorgé d'eau, entre autres, les marécages, les mangroves et les marais.

| Type     | Attributs                              | Description                                                  |
| -------- | -------------------------------------- | ------------------------------------------------------------ |
| Marécage | `natural=wetland` + `wetland=swamp`    | Une zone humide à arbres ou arbustes                         |
| Mangrove | `natural=wetland` + `wetland=mangrove` | Une zone humide à forêt de palétuviers sur la zone intertidale de la côte |
| Marais   | `natural=wetland` + `wetland=marsh`    | Une zone humide à végétation aquatique ou herbacée           |

<img src="/img/wetlands.png" style="zoom:67%;" />

Presque partout à Madagascar, des zones humides sont converties en rizières. Les rizières se démarquent sur l'imagerie par des traits de parcelles. Les zones de rizières sont cartographiées avec un polygone (ou multipolygone) ayant comme attributs `landuse=farmland` et `crop=rice`.

## Cartographier l’intersection route — cours d’eau

Quand le réseau routier doit traverser un cours d'eau, les situations les plus courantes sont: une traversée à gué, une traversée à pont, une traversée à bac ou à bateau.

### Un gué

Un gué est une traversée de cours d'eau où le véhicule (ou le piéton) doit toucher le fond de l’eau. Parfois des pierres y sont posées pour faciliter le passage des piétons. 

Si le cours d'eau est assez étroit, on met sur **un nœud commun** entre la ligne du cours d'eau et la ligne de la route l'attribut `ford=yes`.

Si le cours d'eau est assez développé et on a dessiné l'étendue de l'eau avec un polygone, l'attribut `ford=yes` sera mis sur la section de route qui traverse le polygone de la rivière et ayant toujours un nœud en commun avec la ligne de cours d'eau au milieu du polygone (la section de ligne `highway=*` + `ford=yes` doit ainsi avoir au moins 3 nœuds) [^5].

<img src="/img/ford_mapping.png" style="zoom:67%;" />

### Un pont

Un pont est une structure de traversée permettant au véhicule ou au piéton de traverser au-dessus du niveau de l’eau. La section de route qui passe par le pont est cartographiée avec les attributs supplémentaires `bridge=yes` et `layer=1` pour indiquer un passage via un pont au-dessus du niveau du sol (le fond de la rivière). Optionnellement, le pont en tant que structure peut être cartographié avec un polygone portant l'attribut `man_made=bridge`.

Un pont **ne partage pas de nœud** avec la rivière au-dessus de laquelle il passe.

<img src="/img/bridge_mapping.png" style="zoom:67%;" />

### Une traversée par bac ou par bateau

Un bac est un type de bateau à fond plat utilisé pour traverser l’eau. Généralement il transporte les véhicules et leurs passagers d’une rive vers l’autre d’une grande rivière (ou d’un lac). Parfois des bateaux ou des pirogues assurent aussi la même fonction. Les bacs et bateaux étant toujours présents sur les lieux, ils sont souvent repérables sur l'imagerie.

<img src="/img/boats.png" style="zoom:67%;" />

Le trajet du bac ou du bateau à travers la rivière est cartographié avec une ligne portant l'attribut `route=ferry`. Cette ligne du trajet ne devrait pas partager de nœud avec la ligne de la rivière. Le premier nœud et le dernier nœud du trajet devraient être cartographiés comme des terminaux de ferry (`amenity=ferry_terminal`) [^6].

<img src="/img/ferry_mapping.png" style="zoom:67%;" />

## À propos de MapWithAI

L'extension MapWithAI pour JOSM permet d'ajouter des routes et des chemins détectés par intelligence artificielle. Les étapes de manipulation à suivre sont:

- Télécharger les données MapWithAI de la zone où les données OSM ont été téléchargées au préalable (ctrl + "R")
- Avec MapWithAI comme calque active, sélectionner les segments de routes à ajouter, puis ctrl + "A" va les ajouter au calque de données OSM
- Réctifier et/ou compléter les attributs
- Ajuster le tracé des chemins au besoin (utiliser l'outil "W" ou déplacer manuellement les nœuds)
- Vérifier que tous les segments sont connectés: MapWithAI laisse souvent ces très petits écarts entre les segments. Il faut y zoomer très près pour voir. On peut aussi le tester avec la sélection des chemins adjacents (sélectionner un chemin puis Shift + "E": si le chemin à côté ne se sélectionne pas, ça n'est pas connecté).

<img src="/img/mapwithai_gap.gif" />

Il faut surtout vérifier l'intersection avec les cours d'eau car MapWithAI ne détecte pas les ponts. Il mettra probablement un nœud à l'intersection où il pourrait y avoir un pont.

## À propos des multipolygones

Utilisations:

- pour cartographier des surfaces ayant un ou plusieurs creux, comme les étendues de rivières ayant des ilots à l'intérieur.
- pour des éléménts surfaciques (sans creux) très vastes, comme un grand lac ou un corridor forestier: la limite dans OSM est de 2000 nœuds par chemin, au-delà il va falloir utiliser un multipolygone à plusieurs chemins comme contours extérieurs. Exemple dans OpenStreetMap: [cette forêt](https://www.openstreetmap.org/relation/7065900).
- pour cartographier des éléments à contours extérieurs disjoints. Exemple dans OpenStreetMap: [cet hôpital](https://www.openstreetmap.org/relation/11176282).

On a parfois besoin de fusionner un multipolygone avec un polygone ou avec un autre multipolygone. Ce sera par exemple le cas quand un vaste élément surfacique s'étend sur plusieurs taches (carreaux) cartographiques.

<img src="/img/to_merge.png" style="zoom:67%;" />

Quand on fusionne les deux chemins adjacents (dont l'un est une limite extérieure de multipolygone), il y a des conflits à régler [^7]. Il va falloir:

- choisir les tags à conserver depuis les deux chemins → Comme le nouveau chemin va être la limite extérieure d'un multipolygone, on ne garde aucun attribut, sinon on finira avec à la fois le chemin extérieur et la relation elle même gardant les mêmes attributs `landuse=farmland` + `crop=rice`, ce qui serait une erreur de cartographie.
- choisir si le multipolygone auquel appartient un des chemins est à conserver ou non → On conserve le multipolygone pour garder les limites intérieures.

Dans le cas de deux limites extérieures de multipolygones adjacents (qui n'ont ainsi pas d'attributs), il va tout simplement falloir conserver les deux multipolygones pour avoir tous leurs limites intérieures.

<img src="/img/mp_merge.gif" style="zoom:67%;" />

Voir aussi la [page wiki](https://wiki.openstreetmap.org/wiki/FR:Relation:multipolygon) des multipolygones.

## Notes

[^1]: [FR:Using Imagery](https://wiki.openstreetmap.org/wiki/FR:Using_Imagery)
[^2]: [FR:Bonnes pratiques/Laissez droites les routes droites](https://wiki.openstreetmap.org/wiki/FR:Bonnes_pratiques#Laissez_droites_les_routes_droites)
[^3]: [FR:Highway Tag Africa](https://wiki.openstreetmap.org/wiki/FR:Highway_Tag_Africa)
[^4]: [Rivers/How to map](https://wiki.openstreetmap.org/wiki/Rivers#How_to_map)
[^5]: [Tag:ford=yes/How to Map](https://wiki.openstreetmap.org/wiki/Tag:ford%3Dyes#How_to_Map)
[^6]: [FR:Tag:route=ferry#Comment cartographier avec un simple chemin](https://wiki.openstreetmap.org/wiki/FR:Tag:route%3Dferry#Comment_cartographier_avec_un_simple_chemin)
[^7]: [JOSM Tags Memberships Conflict Dialog](https://josm.openstreetmap.de/wiki/Help/Action/CombineWay#TagsMembershipsConflictDialog)