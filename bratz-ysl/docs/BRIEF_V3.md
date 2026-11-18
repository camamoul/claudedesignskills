# BRIEF V3 : Bratz × Saint Laurent

Document de référence pour la V3. Il remplace toutes les consignes contradictoires des versions précédentes. Il complète docs/PASSATION.md.

Écrit le 18/11/2026 à partir des retours de Camil sur la V2 (fichier references/00_V2_a_corriger.mp4). Corrigé le 18/11 : smoking de Camil noir (section 5), sections 10 et 11 ajoutées.

---

## 0. RÈGLE N°1 : NE RIEN DEVINER

- Tout ce qui est écrit ici est voulu par Camil. Applique-le à la lettre.
- Si un point n'est pas écrit ici, ou si deux consignes semblent se contredire, **tu t'arrêtes et tu demandes à Camil**. Tu n'inventes pas.
- La liste des questions encore ouvertes est en section 9. Tu ne commences pas un plan concerné par une question ouverte sans la réponse.
- Les vidéos TikTok de references/ servent à montrer un rendu, une lumière, un mouvement. Elles ne sont pas le contenu du film. On ne copie pas leurs décors, leurs logos ni leurs personnes (pas de Kendall Jenner, pas de L'Oréal, pas de tour Eiffel).

---

## 1. CONTEXTE ET CONTRAINTES

- Vidéo 3D de défilé « Bratz × Saint Laurent », projet d'école ISG Luxury (Camil, Aurore, Florine). Projection en classe le **24/11 à 11h**.
- Format 2.39:1 cinémascope, 24 i/s, sortie 1920×1080 avec bandes noires (image utile 1920×800), MP4 H.264.
- Durée cible 45 à 50 s. Pas plus : chaque seconde en plus coûte du rendu.
- Blender **5.3** EEVEE sur MacBook M3. Ne pas passer à 5.4 avant le rendu final.
- **Rien de payant.** Pas de Rodin, pas de service payant. Outils gratuits seulement (section 3).
- Pendant un rendu : Mac branché, capot ouvert, `caffeinate`. Jamais de /restart pendant un rendu.
- Camil a 1 à 3 h par jour. Un rendu complet coûte 2 à 3 h, donc **interdit de rendre le film entier pour tester**.
- Échéances :
  - 20/11 au soir : plan test validé par Camil (section 7, étape B).
  - 22/11 au soir : version de secours complète exportée (même imparfaite, avec musique).
  - **23/11 à 18h au plus tard : lancement du rendu final.**
- Diffusion sur un **écran** en classe (pas un vidéoprojecteur). Les textes doivent se lire de loin.
- **Qualité : Camil veut les meilleurs réglages possibles.** Pour le rendu final, pousse la qualité au maximum (samples, ombres, AgX, résolution, encodage H.264 haute qualité CRF 16 ou mieux, preset lent autorisé) **tant que le temps total mesuré tient dans la fenêtre du 23/11**. Annonce le temps total avant de lancer. Les images test restent rapides (section 2.2).

---

## 2. MÉTHODE DE TRAVAIL ET D'APPRENTISSAGE (obligatoire)

Tu n'as pas de mémoire entre deux sessions. Tu apprends uniquement par les fichiers du projet. Voici comment.

### 2.1 Bible du look (à faire en premier)
1. Pour chaque vidéo de references/, extrais 6 à 12 images clés avec ffmpeg (`fps` adapté à la durée), recadre la vidéo 20 sur le haut de l'écran (ignore l'interface TikTok et le menu « Partager »), et remets la 19 à l'endroit (elle est tournée de 90°).
2. Regarde ces images toi-même.
3. Écris `docs/LOOK.md` : pour chaque aspect (lumière, faisceaux, podium, salle, peau, yeux, bouche, mains, cheveux, démarche, montage, chambre), des règles **concrètes et vérifiables**, chacune liée à une image de référence. Exemple : « les faisceaux sont très lumineux près du projecteur et s'effacent sur les deux tiers de leur longueur, bords doux, voir ref 14 image 3 ».
4. Montre `docs/LOOK.md` à Camil avant de toucher à la scène.

### 2.2 Boucle image test
Pour chaque plan, dans cet ordre :
1. Rends **une seule image** au milieu du plan, 960 px de large, environ 24 samples, denoise. Moins de 30 s.
2. Crée une **planche de comparaison** : ton image à gauche, l'image de référence correspondante à droite.
3. Regarde-la toi-même. Liste les écarts par rapport à LOOK.md et à ce brief.
4. Corrige, recommence. 3 à 5 boucles minimum par plan.
5. Seulement ensuite, montre la planche à Camil.

### 2.3 Contrôle chiffré de l'exposition
Script qui, pour chaque image test, donne le % de pixels brûlés (> 0.98), le % de noirs écrasés (< 0.02) et la luminance moyenne. Refus si plus de 2 % de brûlé ou si le sujet principal est dans les noirs. Exception : flash photo volontaire de 1 à 2 images.

### 2.4 Carnet de leçons
Fichier `docs/LECONS.md`, mis à jour **à chaque fois** qu'un réglage marche ou rate : ce que tu as essayé, le résultat vu, la règle à garder (« FAIRE » ou « NE PLUS FAIRE »). Relis-le au début de chaque session. Quand une leçon est sûre, ajoute-la au skill concerné.

### 2.5 Rendu par plans
- Découpe le film en plans indépendants (`shots/shot01` …). Chaque plan a sa caméra, ses images de début et de fin, ses lumières et son dossier de rendu.
- Quand Camil demande une correction, tu ne re-rends que les plans concernés.
- Avant toute séquence : mesure le temps d'une image, multiplie, annonce le total. Si un plan dépasse 15 min, réduis (samples, objets hors champ, résolution des effets).
- Rendus en images séparées, reprise possible (on ne re-rend jamais une image existante). Assemblage final avec ffmpeg.
- Planche contact PNG de tous les plans pour que Camil juge d'un coup d'œil.

### 2.6 Honnêteté
- Ne dis jamais « c'est corrigé » sans avoir rendu **et regardé** l'image, sur plusieurs plans différents.
- Après chaque plan : 3 lignes, ce que tu as testé, ce que tu as vu, ce qui est encore faux.
- Si c'est moyen, dis-le. Si une chose est trop dure à réussir à temps, propose de la simplifier ou de la couper au lieu de livrer un résultat moche.

---

## 3. OUTILS GRATUITS À UTILISER (le « comment »)

### 3.1 Nettoyer les modèles Rodin (cause des bosses, des jambes de poupée)
Sur une **copie** de chaque modèle :
1. Mesh > Clean Up > Merge by Distance, supprimer la géométrie flottante, boucher les petits trous, recalculer les normales.
2. Voxel Remesh, puis lissage (Smooth / Corrective Smooth), puis Subdivision légère si besoin. But : surface **lisse comme le dessin animé**, sans grumeaux.
3. Le remesh perd les UV et les textures peintes. Fais un bake de la couleur de l'ancien maillage vers le nouveau (Selected to Active), ou repeins en couleurs unies propres.
4. **Supprimer l'aspect « vraie poupée articulée »** : pas de coupures visibles aux épaules, coudes, poignets, hanches, genoux. Bras et jambes continus et lisses.
5. Garder les modèles plus fins (silhouette Bratz : grosse tête, corps fin).

### 3.2 Démarche et gestes (cause de la marche de canard et du bras plié en 4)
- Ne plus coder la marche à la main.
- Auto-rig gratuit avec Mixamo (mixamo.com, compte Adobe gratuit, fichier sous 50 Mo, mesh seul) ou Rigify intégré à Blender.
- Animations de marche de défilé gratuites : Mixamo (chercher « catwalk ») et le pack gratuit de 16 marches Rokoko.
- Retarget sur le personnage, puis **corriger à la main** : pieds posés sur une ligne l'un devant l'autre, pointes vers l'avant (pas vers l'extérieur), hanches qui balancent, épaules en arrière, bras souples, regard caméra en bout de podium, **vrai demi-tour**. Référence : vidéos 01 et 03.
- Vérifie chaque frame clé : aucun membre plié à l'envers ou en accordéon.
- Les doigts des modèles IA sont souvent collés : mains simples en forme de moufle façon dessin animé, mais **propres et lisibles**, jamais de moignons.

### 3.3 Visages (5 personnages principaux seulement)
Kylie, Jade, Camil, Aurore, Florine :
- Yeux : retirer les yeux peints. Globes séparés avec iris, pupille, reflet brillant, **vraies paupières** qui clignent, gros cils en cartes. Référence : vidéos 17, 18, 19.
- Bouche : lèvres pleines satinées mates, arrondies (surtout Jade). Une forme de bouche animable (shape keys) : neutre, sourire, choquée « oh », bisou, parler.
- Sourcils dessinés, nez petit et propre (pas un point), peau lisse.
- Expressions par shape keys simples. Pas besoin de rig facial complexe. Style Bratz, pas Avatar.

### 3.4 Public (environ 130 poupées)
- Visages lisibles mais simples : yeux, nez, lèvres, sourcils, cheveux et **mains** propres. Pas de bouches en bec, pas de lèvres gonflées ratées.
- Pas de clones visibles. Variété de coiffures, teints, tenues.
- Pas tous figés : petits mouvements (tête qui tourne, téléphone levé, applaudissements, chuchotement). Certains peuvent rester immobiles comme dans la série.

### 3.5 Cheveux
- Style Alwayz Bratz : **mèches sculptées en géométrie**, épaisses, lisses et brillantes, avec un reflet en anneau. Pas de cheveux en particules réalistes. Pas de « coupes Starfala » plaquées comme un casque. Références : 16, 17, 18, 19. Le skill cheveux stylisés et les cheveux de Kylie déjà refaits sont la base.
- Priorité aux 5 personnages principaux. Public : coiffures simples mais propres et variées.
- **Mouvement** : seulement là où ça se voit (Kylie et Jade qui marchent, mèches de l'équipe quand elle tourne la tête). Méthode gratuite : quelques os dans les grosses mèches + add-on gratuit **Wiggle 2** (extensions.blender.org, compatible Blender 4.2 et plus, à vérifier sur 5.3). **Bake les mouvements en images clés avant le rendu**, sinon ils n'apparaissent pas au rendu. Mouvement léger qui suit la marche, jamais de cheveux qui traversent le corps.
- Pas de simulation de tissu ou de particules pour les cheveux (trop lent).
- Teste d'abord sur Kylie dans le plan test (étape B).

---

## 4. DIRECTION ARTISTIQUE

### 4.1 Général
- Défilé Saint Laurent **noir et or**, luxueux. Rendu des personnages façon **Alwayz Bratz** (Pixel Zoo) : grosse tête, yeux en amande, lèvres pleines, corps fin, tout **lisse**.
- Ambiance « maquette » : le public est fait de poupées.
- Montage façon clip (référence officielle Bratz « Super Sweet » + vidéos 02, 06, 07) : plans de 0,5 à 2 s, inserts macro, flash blanc entre certaines scènes, fond très flou, halo lumineux autour des sources.
- Pas d'aspect cubique, raide ou latex.

### 4.2 La salle
- **Une pièce fermée**, pas d'extérieur. **Pas de tour Eiffel** (annule l'ancienne consigne « tour Eiffel floue »).
- **Hauteur sous plafond beaucoup plus grande** qu'en V2. Plus de « cube noir vide » : on doit sentir des murs, un plafond haut, de la profondeur.
- Lustres dorés. Reflets dorés. Détails or ici et là.
- Photographes et flashs vivants, mais **pas de perche ni de silhouette floue au premier plan**.
- Pas de logos YSL verticaux.

### 4.3 Le podium
- **Le même podium qu'en V2** (podium noir laqué, rangées de chaises de chaque côté). On ne le change pas, on l'améliore : reflets propres comme ref 04 et 08, poussière d'or légère, bords nets.

### 4.4 Lumière
- **3 projecteurs visibles en haut**, de vrais objets (corps du spot visible).
- Leurs faisceaux : forts près du spot, **qui s'estompent** avec la distance, bords doux, une brume légère qui accroche la lumière. **Jamais un triangle net aux bords durs jusqu'au sol.** Référence principale : vidéo 14 (faisceaux dorés). Complément : 13.
- Pas de lasers, pas de look concert (vidéo 15 interdite).
- Une lumière principale, un **contre-jour doré** sur chaque personnage, un léger remplissage froid. Vue AgX, exposition réglée à la main.
- **Les visages ne doivent jamais faire peur dans l'ombre.** Les yeux et la bouche toujours lisibles.
- Le teint de Kylie qui pâlit sous les flashs (V2 vers 11 s) est **voulu et réussi**. À garder.

### 4.5 Fumée
- **Plus de fumée au sol.** Supprimer la fumée 2D de la V2.
- Un **seul nuage de fumée 3D** dans l'arche, pour l'entrée de Kylie : elle sort de la fumée, la fumée se dissipe derrière elle. Référence : vidéos 10, 11, 12. Tester d'abord sur une image (temps de rendu).

### 4.6 L'arche
- Grande et spectaculaire, comme en V2.
- Derrière : **de la profondeur**. Même si le fond reste blanc lumineux, on doit voir un couloir qui s'enfonce (deuxième arche plus loin, lumière qui baisse). Aujourd'hui on dirait un mur coupé.
- Rien de brûlé.

### 4.7 Textes
- « SAINT LAURENT » en Helvetica Neue Bold, blanc, contour or. « BRATZ » avec le vrai lettrage.
- Dans la salle : **SAINT LAURENT d'un côté de l'arche, le × en haut de l'arche, BRATZ de l'autre côté.** Plus en haut tout seul comme en V2.
- Typographie de la carte de fin à revoir. Le logo BRATZ ne doit **jamais être coupé**.
- Fin : « Two icons. One runway. A new vision of luxury. » (gardé, très bien), puis « Projet créatif conceptuel » et en dessous « Proposition artistique non officielle » (sur deux lignes, sans tiret) **assez grand pour se lire en classe**, puis les noms **Camil, Aurore, Florine**.

---

## 5. PERSONNAGES

| Personnage | Détails |
|---|---|
| Bratz Kylie | Robe noire fendue. Texture de tissu visible, la robe bouge. Cligne des yeux. Clin d'œil et bisou. Catwalk + regard caméra + demi-tour. |
| Bratz Jade | Tenue à sequins noirs, **sequins visibles et qui scintillent**. Lèvres arrondies. Fume : **cigarette tenue dans la main**, bouche qui bouge quand elle fume. Catwalk + regard caméra. |
| Camil | Smoking **noir**, porté **sur torse nu**, pantalon très large (le modèle actuel). Yeux **marron foncé**. |
| Aurore | Yeux **jaune-vert**. **La plus grande des trois.** |
| Florine | Yeux **marron**. |
| Anna Wintour | Easter egg : on la voit **en passant**, à côté de l'équipe. Reconnaissable (carré, lunettes noires). Pas de plan dédié. |
| La vraie Kylie | Easter egg, à côté de l'équipe, pas de plan dédié. **Réutilise la tête de la Bratz Kylie qui défile** (c'est la même personne, et la tête actuelle de la Kylie du public est ratée) avec une **perruque rose** et une tenue différente. Elle doit être reconnaissable. |
| Autres célébrités | Easter eggs discrets dans le public. |
| Public | ~130 poupées, section 3.4. On ne montre pas tout le jury. |

- L'équipe (Camil, Aurore, Florine) est **assise face au podium**, pas tournée de côté. C'était déjà demandé après la V1 et pas fait. À vérifier sur chaque plan.
- Bratz plus fines : souhaité, mais secondaire (à faire si le temps le permet).

---

## 6. RETOURS SUR LA V2, MOMENT PAR MOMENT

Pour chaque point : problème, ce qui est voulu, vérification. Timecodes de references/00_V2_a_corriger.mp4.

**Ticket (0 à 4 s)**
- Problème : posé sur un fond blanc.
- Voulu : le ticket doré en 3D **posé sur une table**. L'ombre actuelle est bien, à garder. Le visuel final du ticket sera fourni par Camil **à la fin du projet** : en attendant, garde un ticket provisoire et ne passe pas de temps dessus.
- Vérif : on reconnaît une table, matière et lumière luxe.

**Arche et salle (4 à 6 s)**
- Problème : arche = tache blanche plate, aucune profondeur, salle cube noir, logo trop haut, fumée 2D moche.
- Voulu : sections 4.2, 4.4, 4.5, 4.6, 4.7.
- Vérif : profondeur visible derrière l'arche, < 2 % de brûlé, faisceaux qui s'estompent.

**Anna Wintour (~6 s)**
- Problème : la poupée à lunettes en haut à gauche est ratée et méconnaissable.
- Voulu : retirée de ce plan. Anna apparaît seulement à côté de l'équipe (section 5).

**Entrée de Kylie (6 à 9 s)**
- Problème : elle apparaît de nulle part, plan large délavé, silhouette illisible, que de l'ombre sur elle.
- Voulu : elle **sort du nuage de fumée** dans l'arche, contre-jour doré, silhouette nette, puis la lumière révèle son visage. Caméra plus proche.
- Vérif : silhouette lisible en 1 s, visage visible.

**Pieds de Kylie (9 à 10 s)**
- **Plan parfait à garder** : cadrage sur les pieds, caméra qui bouge comme en vrai.
- À corriger : jambe de poupée Rodin (section 3.1), robe sans texture, démarche de catwalk (3.2).

**Kylie sur le podium (10 à 13 s)**
- Problème : bras « plié en 4 » à 11 s, robe sans texture ni mouvement, ne cligne pas des yeux, visage qui fait peur sans flash à 12 s.
- Voulu : bras naturel, robe qui bouge, clignements, visage lisse et éclairé, **clin d'œil et bisou** vers la caméra. Teint pâle sous flash = gardé.

**L'équipe choquée (14 à 17 s)**
- Problème : l'équipe est de côté, plan trop rapide qui passe sur Camil, Aurore, Florine puis tout le reste, visages et mains qui font peur, Anna et Kylie méconnaissables et trop mises en avant.
- Voulu : plan **plus lent** sur Camil, Aurore et Florine, **assis face au podium**, qui font **tous les trois la même expression choquée en même temps** (effet BFF drôle). Anna Wintour et la vraie Kylie juste à côté, **en fond**, reconnaissables, sans plan sur elles.

**Réaction de Kylie (~18 s)**
- Voulu : plan sur Kylie, « choquée dans le bon sens », genre « I knew that was coming », sûre d'elle. Mains visibles, expression, clignement.

**Entrée de Jade (20 à 22 s)**
- Problème : floue, noire, pas de lumière, caméra trop haute.
- Voulu : même traitement que l'entrée de Kylie (contre-jour doré, lisible), caméra plus basse.

**Jambe et sequins de Jade (22 à 24 s)**
- Le cadrage sur la jambe est bien. À corriger : robe et sequins moches. Sequins nets et scintillants (ref 06 pour les inserts tissu).

**Cigarette (~23 s)**
- Problème : la cigarette n'est pas dans la main, plan trop haut.
- Voulu : **gros plan centré sur la main qui tient la cigarette**, avec la fumée qui monte.

**Jade fume vers nous (~24 s)**
- Gardé : l'idée est bien.
- À corriger : la bouche doit bouger (aspirer, souffler), visage pas dans le noir, pas de halo parasite.

**Image blanche (25,5 s)**
- Supprimer, sauf si c'est un flash de transition volontaire de 1 à 2 images.

**Équipe (26 à 31 s)**
- Problème : encore de côté au lieu de face au podium, visages qui font peur, plan de 5 s quasi statique.
- Voulu : face au podium, visages lisses et éclairés, plan plus court et vivant.

**Interview (31 à 36 s), à refaire entièrement**
- Problème : Kylie et Jade sont debout devant le canapé et ne font rien.
- Voulu, dans cet ordre :
  1. Camil, Aurore et Florine **interviewés au premier plan**, face caméra, qui disent en gros qu'ils sont trop contents d'être là. **Voix enregistrées** + **sous-titres courts** lisibles en classe, fournis par Camil **à la fin du projet**. En attendant, anime les bouches avec un mouvement de parole générique et laisse la place des sous-titres libre.
  2. Derrière eux, Kylie et Jade **assises sur le canapé**, discrètes mais reconnaissables : Jade fume, Kylie lui parle.
  3. Plan court (1 à 2 s) où l'équipe s'approche d'elles pour la photo, pour qu'on comprenne comment on arrive à la photo.
- Même décor que la V2 (canapé, lampes boules). Pas de nouveau décor.

**Photo de groupe (36 à 38 s)**
- **Meilleur plan de la V2**, à garder.
- Tout le monde **regarde la caméra** du film (pas l'appareil photo).

**Polaroid et miroir (38 à 42 s)**
- Problème : la caméra arrive du noir, la photo est coupée, on ne voit plus les têtes, puis 2 s de mur beige vide.
- Voulu : la photo est coincée dans un miroir (le cadre noir du miroir est OK). La caméra **part de la photo entière**, têtes bien visibles, puis **dézoome** et révèle la chambre (ci-dessous). Plus de mur vide.

**Chambre souvenir (nouveau plan)**
- Référence : vidéo 20. Lumière chaude orange (lampe au sel, bougies), reste de la pièce dans la pénombre, fenêtre avec voilage en dentelle et nuit bleu foncé dehors, lit avec plaid à poils longs et coussins foncés collé sous la fenêtre, coiffeuse blanche avec miroir rond.
- **Florine** à la coiffeuse, se vernit les ongles (gestes lisibles).
- **Aurore** sur le lit, sur un ordinateur portable **sans logo**, les doigts tapent.
- **Camil assis sur le rebord de la fenêtre, les pieds posés sur le lit.** Il a un **ordinateur portable** sans logo sur les genoux et **fume un joint**.
- **Tenues** : par défaut, chacun garde **sa tenue de soirée du défilé**. Option à tester : des **pyjamas** 100 % style Bratz (référence 16 et 17). Tu ne les gardes que s'ils sont faciles à faire **et très beaux** : rends une image test avec tenues de soirée et une avec pyjamas, montre les deux à Camil, il choisit.
- **Pas de reflet** particulier dans la chambre (décision de Camil).
- Simple, peu d'objets, gestes bien faits. On doit comprendre que la photo est un souvenir.

**Carte de fin (42 à 45 s)**
- Section 4.7.

---

## 7. ORDRE DE TRAVAIL

**Étape A. Lecture et bible (1 h max)**
Lis PASSATION.md, ce brief, LECONS.md s'il existe. Fais la bible LOOK.md (2.1). Mets en place les scripts : image test, planche de comparaison, contrôle d'exposition, planche contact. Écris `docs/PLANS.md` : liste des plans (durée, cadre, mouvement, émotion, référence). Montre LOOK.md et PLANS.md à Camil. **Stop, attends sa validation.**

**Étape B. Plan test (2 h max)**
Un seul plan : Kylie qui marche en plan moyen sur le podium. Avec modèle nettoyé (3.1), démarche Mixamo corrigée (3.2), vrais yeux qui clignent (3.3), lumière et faisceaux V3 (4.4), podium amélioré. Rendu de 2 s seulement. Montre-le à Camil avec la planche de comparaison. **Stop.** Si Camil valide, la méthode est généralisée. Sinon on change de méthode avant de continuer. Note tout dans LECONS.md.

**Étape C. Plans cassés** : arche, entrées de Kylie et Jade, image blanche.

**Étape D. Personnages** : les 4 autres visages principaux, mains, public.

**Étape E. Plans à refaire** : équipe choquée, interview, Polaroid, chambre.

**Étape F. Détails** : clin d'œil et bisou, cigarette, sequins, textes.

**Étape G. Montage et son** : coupes calées sur « RUNWAY » (Lady Gaga, Doechii), voix, sous-titres, flashs blancs. Export version de secours le 22/11 au soir.

**Étape H. Rendu final** lancé au plus tard le 23/11 à 18h, par plans, avec caffeinate.

---

## 8. RÉFÉRENCES (dossier references/)

| Fichier | À prendre | À ne PAS prendre |
|---|---|---|
| 00_V2_a_corriger | La version à corriger | |
| 01_catwalk_parking_face | Démarche, pieds sur une ligne, hanches, regard caméra | Le parking |
| 02_montage_defile_noir_blanc | Rythme, plans courts | Le noir et blanc |
| 03_catwalk_parking_de_dos | Démarche de dos, demi-tour | Le parking |
| 04_defile_sombre_podium_laque | Podium noir laqué et reflets, contre-jour | |
| 05_defile_duo_insert_jambes | Insert sur les jambes | Les personnes |
| 06_montage_clip_inserts_macro | Inserts macro tissus et bijoux | |
| 07_montage_mannequins_inserts | Rythme, inserts | Les personnes |
| 08_podium_miroir_reflets | Reflets du sol, profondeur | **Tour Eiffel, logo L'Oréal** |
| 09_fond_flou_bokeh | Flou d'arrière-plan, points lumineux | **Kendall, Paris, extérieur** |
| 10, 11, 12 fumée 3D | Fumée volumique pour le nuage de l'arche | La couleur verte de la 12 |
| 13_faisceaux_dans_la_brume | Faisceaux visibles grâce à la brume | Couleur bleue |
| **14_faisceaux_dores** | **LA référence lumière** : faisceaux dorés qui s'estompent | |
| 15_NE_PAS_UTILISER | Rien | Lasers, look concert |
| 16_bratz_3D_officielles | Poses, proportions | Fond blanc |
| **17_alwayz_bratz_scenes** | **LA référence personnages** : peau lisse, yeux, mains, lumière | Les décors roses |
| 18_alwayz_bratz_episode | Expressions, clignements, gestes, choc, clin d'œil | |
| 19_bratz_clip_gros_plans | Yeux, cils, lèvres en gros plan (vidéo tournée de 90°) | |
| 20_chambre_souvenir | Ambiance chambre (section 6) | Interface TikTok |

---

## 9. QUESTIONS OUVERTES (demander à Camil avant le plan concerné)

1. **Musique** : choisie, « RUNWAY » de Lady Gaga et Doechii (BO du Diable s'habille en Prada 2). **On prend le morceau à partir de 0:03 du morceau** (on saute ses 3 premières secondes) et la vidéo démarre directement avec le son. Il faudra un fondu de sortie propre à la fin. Quand le fichier audio est fourni, détecte les temps forts (librosa ou aubio) et cale les coupes et les flashs dessus. Ne cale pas les coupes avant d'avoir le fichier.
2. **Ticket, voix et sous-titres** : gérés par Camil à la fin. Ne pas bloquer dessus.
3. **Références de démarche** supplémentaires si Camil en envoie.

---

## 10. SI ON MANQUE DE TEMPS (ordre de coupe, décidé par Camil)
Bilan chaque soir. Si l'étape en cours a plus d'une demi-journée de retard, coupe dans cet ordre, **sans redemander** :
1. pyjamas (garder les tenues de soirée) ;
2. mouvement des cheveux (Wiggle 2) ;
3. petits mouvements du public (le garder immobile) ;
4. fumée 3D de l'arche (remplacer par la fausse fumée du skill fake-volumetrics) ;
5. chambre souvenir réduite à un seul plan simple, sans gestes détaillés ;
6. vrais yeux et paupières seulement pour Kylie et Jade (textures de visage échangées pour l'équipe).

**Ne jamais couper** : catwalk propre, demi-tour, équipe face au podium, visages éclairés, arche avec profondeur, carte de fin.

## 11. PRÉCISIONS
- **Remaillage voxel en dernier recours** : d'abord souder, lisser et corriger les jambes et les articulations sur le modèle actuel (on garde les UV et les cheveux de Kylie déjà refaits avec le skill stylized-hair).
- **Mixamo** : ne pas envoyer nos modèles chez Adobe. Télécharger seulement l'animation catwalk sur le mannequin Mixamo, puis la retargeter sur nos rigs existants (`blender/rig.py`).
- **Boucles image test** : 3 à 5 pour les plans principaux (Kylie, Jade, équipe), 1 ou 2 pour les plans secondaires, pour tenir dans la limite d'usage du forfait Pro.
