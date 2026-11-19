# Retours de Camil sur la V3 (19/11/2026) et nouvelle méthode

À lire après `CLAUDE.md`, `docs/PASSATION.md` et `docs/BRIEF_V3.md`. Ce document s'applique à toutes les prochaines versions. En cas de conflit avec un message de nuit précédent (« enchaîne sans validation », « baisse la qualité pour finir »), **c'est ce document qui compte** : on n'est plus en mode nuit.

Vidéo jugée : `bratz_ysl_v3.mp4` (45 s, rendue dans la nuit du 18 au 19/11).

---

## 1. Changer de méthode (à faire avant de toucher à la scène)

Pourquoi : les mêmes erreurs reviennent depuis la V1 (smoking gris, équipe de côté, robe en bloc, cigarette hors de la main, chambre pas faite, rendu trop brillant). La règle « vérifie ton travail » ne suffit pas, il faut vérifier **les critères de Camil**.

1. **LECONS.md** : ajoute chacun des retours de la section 3 comme règle « NE PLUS FAIRE » / « FAIRE », avec le numéro du plan concerné.
2. **CHECKLIST.md** (nouveau fichier) : une liste de vérification courte **par plan**, tirée de LECONS.md, de ce document et du brief. Exemple pour le plan 08 : « équipe face au podium, regarde devant ; cadre serré sur les trois ; smoking noir ; noms dans la bande noire ; peu de public visible ».
3. **Au début de chaque session**, relis LECONS.md et CHECKLIST.md avant toute autre chose.

## 2. Boucle d'auto-amélioration (obligatoire pour chaque plan)

Utilise les skills `quality-refinement-autoloop` et `reference-look-calibration`.

1. Rends **une image test** (960 px, moins de 30 s).
2. Fais une **planche** : ton image à gauche, l'image de référence à droite.
3. **Regarde-la toi-même.** Liste les écarts avec la référence, LOOK.md et CHECKLIST.md, et ajoute les mesures (couleur, luminosité, taille du sujet dans le cadre).
4. Corrige **un seul point à la fois**, puis recommence. Note chaque essai dans LECONS.md : ce que tu as essayé, ce que tu as vu, la règle à garder.
5. Arrête-toi quand **tous les points de la checklist passent**, ou après **6 boucles au maximum**. Montre alors à Camil la planche finale, avec les points encore faux.
6. Quand une leçon marche sur 2 plans, ajoute-la au skill concerné, pour qu'elle serve la prochaine fois.
7. **Jamais** de rendu d'une séquence entière tant que l'image test ne passe pas. Ne re-rends que les plans corrigés.

## 3. Retours sur la V3, par ordre de priorité

### Textes
1. **Noms** (CAMIL, AURORE, FLORINE, « LOOK 01 — KYLIE », « LOOK 02 — JADE ») et **futurs sous-titres** : **centrés dans la bande noire du bas**, sous l'image 2.39:1, plus dans l'image. Assez grands pour se lire en classe.
2. **Logos SAINT LAURENT × BRATZ trop petits** : plus grands dans la salle et sur la carte de fin. BRATZ jamais coupé.

### Lumière
3. **Trop lumineux quand tout est allumé** : le podium et le public brillent trop, ce n'est pas assez Bratz. Matières moins brillantes (rugosité plus forte, moins de reflets sur le public), podium laqué mais pas éblouissant.
4. **Kylie et Jade trop sombres quand elles arrivent** : contre-jour doré **et** visage bien éclairé dès l'arche.
5. **Image orange vide vers 2,5 s** : à supprimer. **Salle à 4,5 s** presque noire : on doit voir les murs, le plafond et le public.
6. **Arche** (6 s et 18 s) : un rectangle beige plat. Il faut de la profondeur derrière (couloir, deuxième arche, lumière qui baisse) et un nuage de fumée dont Kylie sort.

### Visages : moins de détails, mais plus nets (règle de style)
7. Le rendu actuel en fait trop (cils en 3D, yeux en relief). Dans la série (ref 17, 18, 19 et `assets/refs/clip_supersweet_visages.png`), le visage est un **volume 3D simple et très lisse**, et les détails sont **graphiques**, presque dessinés :
   - **cils** : une seule forme noire épaisse et nette par œil, comme un trait de feutre qui s'évase vers l'extérieur, pas des cils 3D séparés ;
   - **eye-liner, sourcils, contour des lèvres** : aplats nets, peints dans la texture ou en géométrie très plate collée à la peau ;
   - **yeux** : surface lisse avec un iris net et un gros reflet blanc, rien qui dépasse du visage ;
   - **peau** en aplat doux, avec des ombres simples et douces, sans petits détails.
   Refais **d'abord le visage de Kylie**, avec une planche à côté de la ref 19, puis applique la méthode aux autres.
8. **Yeux de Kylie noirs sur la photo de groupe** : on doit voir l'iris, le reflet et le blanc de l'œil.

### Personnages et animation
9. **Smoking de Camil NOIR** (il est gris partout), porté sur torse nu, pantalon très large. À vérifier sur **tous** les plans.
10. **Plan vers 13-14 s** : nous sommes mal faits, pas lisses, et on regarde sur le côté. On doit regarder **devant nous, vers le podium**, en cadre **serré sur nous trois**, avec presque pas de public visible. Les noms ne doivent **jamais** s'afficher sur des poupées du public. Même correction **vers 24 s** (de côté, visages coupés).
11. **Démarche** : les articulations cassent un peu (genoux, coudes). Corrige image par image.
12. **Plan des pieds qui marchent** : texture bizarre, mal fait. Jambes lisses, talons fins, reflet propre.
13. **Robe de Kylie** : toujours un seul bloc, sans fluidité. Fais une vraie simulation de tissu bakée sur la jupe, ou des os de jupe beaucoup plus souples. La fente doit s'ouvrir.
14. **Sequins de Jade** : toujours mal faits. Il faut de vrais petits disques qui scintillent par points (ref 06 et 21 à 42).
15. **Public en gros plan** (14 s, 16 s) : pas assez Bratz. Améliore-le, ou cadre plus large et plus flou pour cacher les défauts.

### Jade
16. **La cigarette doit être DANS sa main**, entre l'index et le majeur, et visible. **Fumée plus belle** : fine, en volutes, qui monte, blanc-gris transparent (ref 10, 11). Fais le gros plan main et fumée (plan 12) et le plan où elle souffle vers nous (plan 13).

### Fin
17. **La chambre n'est pas faite.** Refais entièrement selon le brief, section 6 :
    - le Polaroid coincé dans le cadre du miroir, têtes visibles, puis un dézoom ;
    - la chambre (ref 20) : lampe au sel orange, bougies, fenêtre avec voilage en dentelle et nuit bleue, lit avec plaid, coiffeuse blanche à miroir rond ;
    - Florine se vernit les ongles, Aurore tape sur son ordinateur sur le lit, Camil est sur le rebord de la fenêtre, pieds sur le lit, avec un ordinateur et un joint ;
    - plus de mur blanc vide, plus d'image noire.

## 4. À garder tel quel
Le salon et l'interview (26 à 30 s), la photo de groupe (sauf les yeux), la carte de fin (sauf la taille des logos), Kylie sur le podium (10 à 12 s), l'insert sur les sequins (cadrage gardé).

## 5. Ordre de travail
1. Méthode (sections 1 et 2) : LECONS.md et CHECKLIST.md.
2. Les plus visibles et les plus longs d'abord : **visage de Kylie** (7), **chambre** (17), **robe** (13), **équipe face au podium** (10).
3. Puis les plans courts : cigarette (16), sequins (14), arche (6), lumière (3 à 5), smoking (9), textes (1 et 2), pieds (12), démarche (11), yeux sur la photo (8), public (15).
4. Re-rends seulement les plans corrigés, remonte le MP4 et fais un bilan plan par plan : ce qui est corrigé, ce qui reste faux.

Rendu final lancé au plus tard le **23/11 à 18 h** (brief). Si le temps manque, coupe dans l'ordre de la section 10 du brief.
