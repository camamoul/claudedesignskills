# Bratz × Saint Laurent : passation pour Claude Code (Mac)

Projet d'école de Camil (ISG Luxury), en groupe avec Aurore et Florine. Rendu le 24/11/2026 à 11h.
Il s'agit d'une vidéo 3D de défilé de **45 s**, en **cinémascope 2.39:1**, à **24 images/s**, projetée en classe.
Réponds à Camil en français, de façon concise. Il veut **un rendu lisse, façon série Alwayz Bratz**, dans un défilé Saint Laurent **noir et or, luxueux** : pas de rose ni de paillettes dans le décor. Il juge sévèrement les brouillons moches : montre des aperçus soignés, pas des tests bruts.

## À lire en premier
- `docs/DA.md` : toute la direction artistique, les 24 décisions, le casting et le **storyboard v2** (section 10). C'est la référence.
- `docs/PASSATION.md` : **état au 18/11 et plan de la V3** (retours de Camil sur la V1 et la V2, références dans `assets/refs/`, skills fast-eevee, fake-volumetrics et stylized-hair, pièges connus).
- `.claude/skills/` : 28 skills vérifiés (Blender, rigging, animation, cheveux, tissus, lumière, rendu, caméras, motion design, montage). La provenance est dans `SOURCES.txt`.

## Les modèles 3D (`assets/`, hors git : ils sont sur le Drive « Bratz x YSL » de Camil)
| Fichier | Personnage | État |
|---|---|---|
| `kylie.glb` / `kylie_rig.glb` | Bratz Kylie, robe noire fendue | Squelette et démarche faits. La robe d'un seul bloc se déforme : à corriger avec la simulation de tissu. |
| `jade.glb` / `jade_rig.glb` | Bratz Jade, sequins noirs, fume | Squelette et démarche faits. **Les lèvres sont trop pointues : à lisser.** |
| `team_camil.glb` | Camil (garçon), smoking noir sur torse nu, pantalon très large | Pas encore de squelette. |
| `team_florine.glb` | **Florine** : brune ondulée, mini-robe en velours à épaules dénudées, collants | Pas encore de squelette. |
| `team_aurore.glb` | **Aurore** : balayage caramel, bustier corset | Pas encore de squelette. Le liseré du corset paraît rougeâtre : le passer en noir. |

Les modèles viennent de Rodin (Hyper3D, en Gen-2.5). Les yeux et la bouche sont **peints dans la texture** : il n'y a pas de géométrie de paupières.

## Le pipeline existant
- `blender/analyze.py` : profil de hauteur d'un GLB, pour placer les articulations.
- `blender/rig.py` : squelette, skinning (EL4CTEO `bind_mesh`), cycle de démarche de défilé, export en GLB.
- `index.html` et `snap.mjs` : une scène three.js de **prévisualisation seulement** (rendu logiciel, moche). Le rendu final se fait dans **Blender**, avec Cycles ou EEVEE, sur le GPU du M3.

## Les chantiers ouverts (par priorité)
1. Installer Blender 5.3 et mcp-for-blender (ahujasid). **Désactiver la télémétrie avec `DISABLE_TELEMETRY=true`.**
2. **Les visages expressifs**, sans payer : le clin d'œil, le bisou, la réaction « oh » de la vraie Kylie, le regard en coin. Pistes : des textures de visage interchangeables, des shape keys après avoir ajouté des paupières, ou un mélange avec Veo uniquement sur les gros plans. Camil laisse Claude choisir.
3. Lisser les maillages Rodin, qui sont grumeleux, pour un rendu Alwayz Bratz. Les cheveux restent des **volumes sculptés lisses**, pas des mèches.
4. Construire le décor d'après `docs/DA.md` : podium noir laqué qui scintille comme sous la pluie, lustres dorés, tour Eiffel floue, fumée et faisceaux, flashs. Plus le salon privé et le miroir de chambre.
5. Réaliser les 9 célébrités du front row, reconnaissables à leurs signes distinctifs, et la vraie Kylie, différente de la Bratz Kylie.
6. Animer, mettre en caméra (telle que décrite dans le DA), rendre et monter. Ajouter le sound design et les voix enregistrées par l'équipe.

## Décisions complémentaires (17/11)
- **La vraie Kylie** au front row porte une **perruque rose** (époque « King Kylie »), pour la distinguer de sa Bratz en noir.
- **Sia** : carré à frange longue sur les yeux, moitié noir, moitié blond platine. **Énorme nœud en satin noir** sur la tête, blazer noir croisé, lèvres rouges.
- **Kim Kardashian** : très longs cheveux noirs ondulés, raie au milieu, haut col montant brun-noir semi-transparent, maquillage nude.
- **La vraie Kylie** : longue perruque rose pastel ondulée, robe bustier en latex rose, grosse bague en diamants.
- **Le sac de l'équipe** : sac hobo Saint Laurent type « Le 5 à 7 » en cuir noir lisse, fermoir YSL doré, anse courte d'épaule. Le même pour les trois.
- **Lady Gaga et Doja Cat** : des looks **gothiques noirs** (chapeau, voilette, cristaux noirs), pour rester en noir et or.
- **Le salon privé** : velours noir et or, laiton, champagne, lumière tamisée.
- **Le miroir de la fin** : une chambre neutre, sans personne dans le reflet.
- **Les polices** :
  - **Saint Laurent** : **Helvetica Neue Bold**, en capitales, avec un interlettrage large. Elle est **préinstallée sur macOS**.
  - **Bratz** : la référence est la capture de Camil (un lettrage cartoon gras, penché, avec un contour crème et une ombre portée noire). **À utiliser en blanc** : remplissage blanc, contour or fin, ombre portée noire douce. Il n'y a pas de fichier .otf : télécharger **House of Fun** (Leigh Taylor / Flava Fonts, gratuite sur FontSpace, l'équivalent le plus proche), ou vectoriser le mot « BRATZ ».
- **Le ticket doré** n'est pas commencé : Claude propose un design, qu'Aurore reprendra pour le vrai.

Ce qui manque encore : le modèle 3D du sac, les références de Hailey Bieber et Vaccarello (facultatif), et la musique.

## Priorités de production (décision du 17/11, plus de crédits Rodin)
- **En vrai 3D** (squelette, animation, visages expressifs) : la Bratz Kylie, la Bratz Jade, Camil, Aurore et Florine. C'est la priorité absolue.
- **La vraie Kylie** a un gros plan de réaction. Essayer un générateur 3D gratuit (Hunyuan3D ou TRELLIS sur Hugging Face). Sinon, la traiter en « carte » (voir ci-dessous) avec un cadrage serré.
- **Les 8 autres célébrités** : des **cartes 2D**, c'est-à-dire des images Gemini détourées et posées sur des plans dans le front row. Elles sont en pénombre, avec une faible profondeur de champ et un travelling. Images à générer « assises, de trois quarts, tournées vers le podium ».
- **Le sac « Le 5 à 7 »** : à modéliser directement dans Blender (forme simple, cuir noir, fermoir YSL doré), sans Rodin.
- Les modèles secondaires n'ont pas besoin d'être parfaits.

## Refaire les squelettes sur le Mac
Les fichiers `kylie_rig.glb` et `jade_rig.glb` n'existaient que dans la session cloud. Pour les régénérer :
`/Applications/Blender.app/Contents/MacOS/Blender -b -P blender/rig.py -- kylie assets/kylie.glb assets/kylie_rig.glb .claude/skills`
(Même commande pour `jade`.) Les articulations de Camil, d'Aurore et de Florine sont à mesurer avec `blender/analyze.py`, puis à ajouter dans le dictionnaire `JOINTS` de `rig.py`.
