# Démarrage V4 : Bratz × Saint Laurent (nouvelle session, 20/11/2026)

Ce document lance une **nouvelle session** de Claude Code. La session précédente (V3) a été coupée par un crash du Mac. Tu n'as aucune mémoire d'elle : tout ce qu'il faut savoir est dans les fichiers ci-dessous. Lis-les **dans cet ordre** avant de toucher à quoi que ce soit.

## 0. Lecture obligatoire (dans l'ordre)
1. `CLAUDE.md` : le projet, les personnages, les modèles.
2. `docs/BRIEF_V3.md` : **la référence**, y compris les sections 8 (références), 10 (ordre de coupe) et 11 (précisions).
3. `docs/RETOURS_V3.md` : les 17 retours de Camil sur la V3, et la **méthode obligatoire** (boucle image test → comparaison → correction).
4. `docs/LECONS.md` : tout ce qui a marché ou raté. **Relis-le en entier.** Il contient les règles « FAIRE / NE PLUS FAIRE ».
5. `docs/CHECKLIST.md` : les vérifications par plan.
6. `docs/LOOK.md` et `docs/PLANS.md` : la bible visuelle et le découpage en 20 plans.
7. `docs/PASSATION.md` : l'historique V1 et V2, les skills et les pièges.
8. Les skills de `.claude/skills/` qui servent ici : `fast-eevee`, `fake-volumetrics`, `stylized-hair`, `quality-refinement-autoloop`, `reference-look-calibration`, `blender-clothing`, `blender-simulation`, `blender-facial-shapekeys`.

Puis fais un **état des lieux** (section 2) et montre-le à Camil.

## 1. Contexte en bref
- Vidéo 3D de défilé « Bratz × Saint Laurent », 45 à 50 s, 2.39:1 (image utile 1920×800, bandes noires jusqu'à 1920×1080), 24 i/s, MP4 H.264. Projection en classe le **24/11 à 11 h**, sur un écran.
- Blender **5.3** EEVEE, MacBook M3. **Ne pas passer à 5.4.**
- **Rien de payant.**
- Musique : `references/runway.mp3` (« RUNWAY », Lady Gaga et Doechii). La vidéo commence à 0:03 du fichier. Environ 118 BPM, gros son à 6,0 s du fichier (3,0 s de vidéo), l'énergie retombe vers 26 s du fichier (environ 23 s de vidéo : flash blanc, la musique coupe). **Ne jamais mettre ce fichier dans git** (dépôt public).
- Animations Mixamo (40 fichiers FBX, retargetées) : bibliothèque dans `assets/anim/`. Démarche de Kylie **validée** : Catwalk_Walk, un pas tous les 2 temps.
- Version de secours qui existe déjà : `bratz_ysl_v3.mp4` (45 s, complète, avec musique).
- Échéance : **rendu final lancé au plus tard le 23/11 à 18 h**, par plans.

## 2. État au moment du crash (à vérifier sur le disque)
Ce que la session précédente avait fait ou était en train de faire, d'après ses derniers messages :
- **Méthode** : 17 retours ajoutés dans LECONS.md, CHECKLIST.md créé, `tools/look_metrics.py` écrit (OpenCV n'est pas sur le Mac).
- **Visage de Kylie** (`shots/shot05/planche_visage_kylie_v4.png`) : cils en une seule forme graphique, reflet blanc dans l'iris, sourcils nets, lèvres prune satinées, clignement complet. **Reste** : un pli de peau à la tempe et au coin intérieur de l'œil (visible seulement en gros plan de trois-quarts), et un liseré rouge au bord des lèvres.
- **Chambre** (`shots/shot19/`, script `blender/bedroom.py`) : décor construit (lampe au sel, fenêtre bleu nuit avec voilage, lit, coiffeuse, Polaroid). Le crash a eu lieu **pendant la boucle 4**. Restait faux après la boucle 1 : Aurore coupée au bord droit, Camil de profil sans ses pieds visibles sur le lit, ordinateurs et joint invisibles, geste du vernis peu lisible, plaid sans poils.
- **Bug de bake trouvé** : les rigs tournent en mode quaternion, et la fonction `bake` lisait `rotation_euler` (ignoré par Blender). C'est corrigé avec `matrix_basis.to_euler()`, **mais les placements du salon et de l'équipe au front row ont été faits avec ce bug**. Il faudra reconstruire ces plans avec le bake corrigé.
- **Smoking de Camil** : il était encore **gris**. Il doit être **NOIR**, porté sur torse nu, pantalon très large. C'est la 4e fois que ça revient : à corriger partout, en premier.
- Robe (13), équipe face au podium (10) et tout le reste de RETOURS_V3.md : pas encore faits.

**À faire en premier** : vérifie ce qui existe vraiment (fichiers, dates, `renders/v3/film_v3.blend`, `shots/`), ce qui est perdu, et si un processus Blender tourne encore (`pgrep -fl Blender`). Écris l'état dans LECONS.md, puis montre à Camil un résumé en 10 lignes maximum.

## 3. Éviter un nouveau crash (cause probable : manque de mémoire)
- **Un seul processus Blender à la fois.** Jamais deux rendus, ni un rendu et une simulation en parallèle. Pas d'agents en parallèle qui lancent Blender.
- Simulation de tissu : commencer **en basse résolution** (peu de sommets sur la jupe) et **sur peu d'images**, puis monter.
- Avant un rendu long : vérifier la mémoire libre (`vm_stat`, `memory_pressure`). Cacher les collections hors champ, poupées lointaines en version légère.
- Rendus en images séparées, sans écraser les images existantes (`use_overwrite = False`, `use_placeholder = True`), pour pouvoir reprendre après un crash.
- Lancer les rendus longs avec `caffeinate -dimsu`, et en arrière-plan avec un log.
- Sauvegarder le `.blend` après chaque étape réussie.

## 4. Ordre de travail V4
1. **État des lieux** (section 2) et résumé à Camil.
2. **Smoking de Camil en NOIR** partout (rapide, et ça revient sans cesse).
3. **Chambre** : reprendre la boucle 4 (Aurore entière dans le cadre, Camil de trois-quarts avec les pieds sur le lit, ordinateurs et joint visibles, geste du vernis lisible).
4. **Robe de Kylie** (retour 13) : séparer la jupe du corps (objet `Dress`, le haut reste sur le corps), appliquer les transformations, recalculer les normales. Collision sur les jambes et les hanches (marge 0,005 à 0,02 selon l'échelle). Tissu sur la jupe, épinglé à la taille, pré-roll de 20 à 30 images. Pas d'auto-collision sauf si nécessaire. Bake avant rendu. **Garder la marche Mixamo validée.** Si ça ne tient pas en 2 boucles, revenir à des os de jupe plus souples.
5. **Équipe face au podium** (retour 10) : nous trois, choqués en même temps, regardant devant vers le podium, cadre serré, presque pas de public. Reconstruire le salon et le front row avec le **bake corrigé**.
6. Le reste de RETOURS_V3.md, section 5 : cigarette dans la main de Jade et fumée, sequins, arche avec profondeur et fumée, lumière moins brillante, Kylie et Jade éclairées à l'entrée, textes dans la bande noire du bas, logos plus grands, pieds, articulations, yeux de Kylie sur la photo, public.
7. Re-rendre **seulement les plans corrigés**, remonter le MP4 (`renders/v4/bratz_ysl_v4.mp4`) avec la musique, et faire un bilan plan par plan.

Pour chaque plan : la boucle de RETOURS_V3.md, section 2 (image test → planche avec la référence → regarder → corriger un point → noter dans LECONS.md), **6 boucles au maximum**, puis montrer à Camil.

## 5. Style à ne pas oublier
- Visages : **moins de détails, mais plus nets**. Volume 3D lisse, cils en une forme noire graphique, eye-liner et sourcils en aplats, yeux lisses avec un gros reflet blanc (ref 17, 18, 19 et `assets/refs/clip_supersweet_visages.png`).
- Lumière : noir, or et crème ; contre-jour doré ; visages toujours lisibles ; **pas trop brillant** (podium et public ne doivent pas éblouir).
- Noms et sous-titres : **centrés dans la bande noire du bas**.

## 6. Comment parler à Camil
- Français, court, concret. Il a peu de tokens et peu de temps.
- Ne montre jamais un test brut. Montre des planches soignées, avec les noms des personnages si besoin.
- Après chaque plan, 3 lignes : ce que tu as testé, ce que tu as vu, ce qui est encore faux.
- Ne dis jamais « c'est corrigé » sans avoir rendu **et regardé** l'image.
