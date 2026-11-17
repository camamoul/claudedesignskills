# Bratz × Saint Laurent : passation pour Claude Code (Mac)

Projet d'école de Camil (ISG Luxury), en groupe avec Aurore et Florine. Rendu le 24/11/2026 à 11h.
Il s'agit d'une vidéo 3D de défilé de **45 s**, en **cinémascope 2.39:1**, à **24 images/s**, projetée en classe.
Réponds à Camil en français, de façon concise. Il veut **un rendu lisse, façon série Alwayz Bratz**, dans un défilé Saint Laurent **noir et or, luxueux** : pas de rose ni de paillettes dans le décor. Il juge sévèrement les brouillons moches : montre des aperçus soignés, pas des tests bruts.

## À lire en premier
- `docs/DA.md` : toute la direction artistique, les 24 décisions, le casting et le **storyboard v2** (section 10). C'est la référence.
- `.claude/skills/` : 28 skills vérifiés (Blender, rigging, animation, cheveux, tissus, lumière, rendu, caméras, motion design, montage). La provenance est dans `SOURCES.txt`.

## Les modèles 3D (`assets/`, hors git : ils sont sur le Drive « Bratz x YSL » de Camil)
| Fichier | Personnage | État |
|---|---|---|
| `kylie.glb` / `kylie_rig.glb` | Bratz Kylie, robe noire fendue | Squelette et démarche faits. La robe d'un seul bloc se déforme : à corriger avec la simulation de tissu. |
| `jade.glb` / `jade_rig.glb` | Bratz Jade, sequins noirs, fume | Squelette et démarche faits. **Les lèvres sont trop pointues : à lisser.** |
| `team_camil.glb` | Camil (garçon), smoking noir sur torse nu, pantalon très large | Pas encore de squelette. |
| `team_fille1.glb` | Brune ondulée, mini-robe en velours à épaules dénudées, collants | Pas encore de squelette. Prénom à confirmer (Aurore ou Florine). |
| `team_fille2.glb` | Balayage caramel, bustier corset | Pas encore de squelette. Le liseré du corset paraît rougeâtre : le passer en noir. Prénom à confirmer. |

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

Ce qui manque encore : les polices, le sac YSL (à générer à part), le design du ticket doré (Aurore) et la musique.
