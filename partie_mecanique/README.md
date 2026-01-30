# PARTIE MECANIQUE

### Pièce 3D
Les pièces 3D ont été modélisées via Onshape, et disponible au format STL.

Stator : 
- ``main.stl`` support principal fixé à un trépied. 

Rotor : 
- ``petite_roue.stl`` roue dentée fixée au moteur. 
- ``grande_roue.stl`` roue principale.  
- ``couvercle.stl`` fixé à la grande roue. 
- [courroie](https://www.amazon.fr/sourcing-map-Courroie-distribution-caoutchouc/dp/B0DSR3P59V/ref=sr_1_4?__mk_fr_FR=ÅMÅŽÕÑ&crid=2DVCB6ZJ2Z6N6&dib=eyJ2IjoiMSJ9.INokD1g1XKGq4FjiK4KJ-2DFuZPBLBakq1pM_ikAQQW-i8_wvu6zflLYD9bUancVo1O1l0KUpVF_Tc12299VBfvdVWGJqAfd7dZ5Z0dowRu1OleMIxkBsCXyfrw_BsMGcycEjID_bXYTH-4Jm1so129zpuPP06CmUVDd1TbQXxbmJKklR36qcrfXnCtGEjsZ-37gbQdMV0VhXsDEZqvy0kOxExp_DtmuPP1F3U7picrk7hs-b8qVLdveGdYnYE3JuToG5yF9XXBt19ypSJsxIJoUYEDpVoUJI-cyxjdedZ8.aslACeUXgRTCYPRULSt5mBXesOI6mXxBFWhpa6HJw2Y&dib_tag=se&keywords=courroie+dentée+pas+5+mm+610+mm&qid=1767950807&sprefix=courroie+dentée+pas+5+mm+6010+mm%2Caps%2C284&sr=8-4) pour la transmission. 

### Description du support

``main`` est le support principal qui s'attache au trépied. La pièce est sous-dimensionnée volontairement au niveau du trépied afin d'assurer une meilleur stabilité, il est normal qu'il faille forcer légèrement pour la rentrer dans le trépied. 
Au dos de la pièce il y a un emplacement pour la carte Raspberry Pi qui contrôle le moteur, des emplacements sont prévus pour visser la carte. 
Le moteur se place en bas dans son emplacement prévu, Il se visse par l'arrière, les espacements entre les vis ne sont pas les mêmes horizontalement et verticalement, vérifiez le sens. 
Le capteur à effet Hall est collé sur le côté de la pièce afin de ne pas gêné les câbles et être suffisament près des aimants placés sur la roue. 

#### Support d'axe

Le support d'axe correspond à la partie supérieur de la pièce. Ce tube acceuille des [roulements à billes](https://www.123roulement.com/roulement-palier/roulement-bille/simple-rangee/6005-2rsh-skf) de diamètre intérieur 25 mm et 47 mm de diamètre extérieur. Pour assurer que les roulements à billes ne glisse pas hors du support pendant que le système est en marche il faut ajouter des vis dans les trous creusés sur le dessus de la pièce. Le slip ring se fixe au dos du support d'axe. 

## Transmission mécanique
La ``petite_roue`` est fixée au moteur et entraîne la [courroie](https://www.amazon.fr/sourcing-map-Courroie-distribution-caoutchouc/dp/B0DSR3P59V/ref=sr_1_4?__mk_fr_FR=ÅMÅŽÕÑ&crid=2DVCB6ZJ2Z6N6&dib=eyJ2IjoiMSJ9.INokD1g1XKGq4FjiK4KJ-2DFuZPBLBakq1pM_ikAQQW-i8_wvu6zflLYD9bUancVo1O1l0KUpVF_Tc12299VBfvdVWGJqAfd7dZ5Z0dowRu1OleMIxkBsCXyfrw_BsMGcycEjID_bXYTH-4Jm1so129zpuPP06CmUVDd1TbQXxbmJKklR36qcrfXnCtGEjsZ-37gbQdMV0VhXsDEZqvy0kOxExp_DtmuPP1F3U7picrk7hs-b8qVLdveGdYnYE3JuToG5yF9XXBt19ypSJsxIJoUYEDpVoUJI-cyxjdedZ8.aslACeUXgRTCYPRULSt5mBXesOI6mXxBFWhpa6HJw2Y&dib_tag=se&keywords=courroie+dentée+pas+5+mm+610+mm&qid=1767950807&sprefix=courroie+dentée+pas+5+mm+6010+mm%2Caps%2C284&sr=8-4) qui entraîne la ``grande_roue``. Le ``couvercle`` est vissé sur la grande roue et tient les profilés en aluminium avec [les bandeaux de LEDs](https://fr.aliexpress.com/item/4001201679511.html?spm=a2g0o.tesla.0.0.b102ffNWffNWkx&pdp_npi=6%40dis%21EUR%216%2C82€%216%2C79€%21%21%21%21%21%40211b61bb17643396735751664eb65b%2110000015284474061%21btfpre%21%21%21%211%210%21&afTraceInfo=4001201679511__pc__c_ppc_item_bridge_pc_main__rdjCUwP__1764339673682&gatewayAdapt=glo2fra). Le rapport de réduction entre les roues est d'environ 8.5. 

Courroie :
* Longueur: 610 mm
* Largeur: 15 mm
* Pas: 5 mm

Petite Roue : 
* Diamètre: 19 mm (à l'extérieur des dents)
* Largeur: 30 mm
* Pas: 5 mm

Grande roue : 
* Diamètre: 161 mm (à l'extérieur des dents)
* Largeur: 22 mm
* Pas: 5 mm
* Longueur de l'axe de rotation: 84.4 mm

L'axe de rotation est percé afin d'acceuillir les câbles sortant du slip ring. Ces câbles servent à l'alimentation de la carte Raspberry Pi et des bandeaux de LEDs ainsi que la transmission du signal généré par le capteur à effet Hall. La carte Raspberry Pi est vissé dans le compartiment au centre de la roue.

Le ``couvercle`` recouvre la Raspberry Pi de la grande roue, il est troué pour laisser les câbles qui font la communication entre les bandeaux de LED et la carte Raspberry Pi. [Les profilés en aluminium](https://www.leroymerlin.fr/produits/profile-u-aluminium-anodise-mat-standers-h-10-x-l-15-x-ep-1-mm-l-1-m-87477956.html) y sont vissés en son centre. Sur ces profilés sont attachés [les bandeaux de LEDs](https://fr.aliexpress.com/item/4001201679511.html?spm=a2g0o.tesla.0.0.b102ffNWffNWkx&pdp_npi=6%40dis%21EUR%216%2C82€%216%2C79€%21%21%21%21%21%40211b61bb17643396735751664eb65b%2110000015284474061%21btfpre%21%21%21%211%210%21&afTraceInfo=4001201679511__pc__c_ppc_item_bridge_pc_main__rdjCUwP__1764339673682&gatewayAdapt=glo2fra). Des serre flex permettent de maintenir les LEDs et leurs câbles sur les profilés. 
