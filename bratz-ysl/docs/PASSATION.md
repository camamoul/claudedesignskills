# Passation V3 : Bratz × Saint Laurent (18/11/2026)

À lire après `CLAUDE.md` et `docs/DA.md`. Ce document résume l'état du projet après la V1 et la V2, les retours de Camil, ce qui a été préparé dans la session cloud et le plan de la V3.

**Rendu le 24/11/2026 à 11h.** Vidéo de 45 s, 2.39:1, 24 i/s, projetée en classe. La vidéo est pour le fun. Le projet d'école officiel est une « maquette » de défilé, donc un rendu façon **diorama de poupées** est dans le sujet.

## 1. Où en est le projet
| Version | Où | État |
|---|---|---|
| V1 | `renders/v1/bratz_ysl_v1.mp4` | Complète mais jugée « moche » par Camil (voir section 3). |
| V2 | `renders/v2/bratz_ysl_v2.mp4` | Lancée dans la nuit du 17 au 18/11 (environ 1 h de rendu, 127 poupées, arche, faisceaux). **Pas encore revue par Camil.** Défaut signalé : les plans d'entrée de Kylie et de Jade et le plan de la pose sont presque blancs autour de l'arche. |
| V3 | à faire | Voir section 6. |

Scripts de scène sur le Mac : `blender/build_v1.py`, `blender/set_v2.py`, `blender/set_v3.py`, plus `blender/rig.py` et `blender/analyze.py`. Les rigs des 5 personnages sont faits.

## 2. Comment travailler avec Camil
- Il répond en messages courts, souvent par capture d'écran. Il veut que ça avance **sans questions**.
- Il juge sévèrement : **ne jamais montrer de test brut**. Montrer des aperçus soignés, avec des noms sur les personnages quand il faut vérifier qui est qui.
- Une étape à la fois : 3 ou 4 images fixes en basse définition, puis le rendu complet seulement une fois l'étape validée, sauf s'il dit « enchaîne sans me demander ».
- **Ne rien payer.** Pas de Rodin, pas de Fable (facturé hors forfait), pas de service en ligne payant.
- Forfait **Pro** : rester sur **Sonnet** pour les rendus et le montage, Opus seulement pour les étapes difficiles (têtes, lumière).

## 3. Retours de Camil (cumul V1 et aperçus V2)
**Décor et lumière**
- Les faisceaux doivent partir d'un **vrai projecteur visible** et descendre vers le podium. Pas de faisceau sans source, pas de V qui sort de nulle part, pas de blocs gris.
- La salle doit être vivante : fosse de photographes debout avec des flashs, des cadreurs, plusieurs rangs. Mais **pas de perche en diagonale ni de silhouette noire au premier plan**.
- L'entrée des mannequins doit être **spectaculaire** (arche haute, contre-jour, fumée). **Pas de logos « YSL » verticaux** à côté.
- Les reflets du podium laqué doivent être beaux, surtout sous les talons.

**Public et célébrités**
- Pas de clones : chaque poupée est différente et **vraiment Bratz** (grosse tête, yeux en amande, lèvres pleines, corps fin, longues jambes, plateformes, attitude). Environ 130 poupées.
- Ne **pas** montrer tout le jury. Montrer surtout l'équipe (Camil, Aurore, Florine), choquée, et Anna Wintour en passant. Les autres célébrités sont des **easter eggs** dans le décor.
- L'équipe est assise **face au podium**, pas tournée.

**Personnages**
- Pas l'air de poupées raides : **bords fins et arrondis**, rien de cubique, pas de plis.
- **Vrai catwalk** : pas croisés, hanches, bras relâchés, talons fins. Elles arrivent du fond, font un **vrai demi-tour** (pas de marche arrière) et une pose naturelle.
- Matières lisibles : tissu, sequins de Jade visibles de près. Les tenues de l'équipe ne doivent pas avoir l'air de **latex**. **Camil est en gris.**
- Lèvres de Jade arrondies, pas pointues. Yeux en amande.
- La cigarette est tenue dans la main, elle ne flotte pas.
- Des **émotions** : bouche et yeux qui bougent.

**Graphisme**
- Ticket d'ouverture : en 3D, posé sur une table, avec le lettrage Bratz. Pas de fond beige.
- « SAINT LAURENT » en **Helvetica Neue Bold**, blanc, contour or fin, ombre douce. « BRATZ » avec le vrai lettrage : `assets/refs/logo_bratz_blanc_or.png`. Camil trouve ce BRATZ « très bien fait ».
- Carton final : le logo, puis « Two icons. One runway. A new vision of luxury. », puis en minuscule « Projet créatif conceptuel — Proposition artistique non officielle » (textes tirés de son communiqué).

**Narration après le défilé**
- L'équipe réagit, puis courte interview des filles. Derrière, les Bratz discutent avec la vraie Kylie. On s'approche d'elle, on parle, puis la photo.

## 4. Références (`assets/refs/`)
| Fichier | Usage |
|---|---|
| `ref_bratz_ysl_podium.png` | **Cible de composition** des plans de défilé : logo YSL éclairé au fond, trois Bratz en V vers la caméra, public de poupées assis dans la pénombre, sol laqué. |
| `ref_defile_lumiere_photo.jpg` | Lumière d'un vrai défilé Saint Laurent : barre lumineuse en diagonale au plafond, lueur chaude au sol, pas croisés. |
| `logo_bratz_blanc_or.png`, `logo_bratz_noir.png` | Lettrage BRATZ (bas du B et du R coupé à plat : il était caché dans la source). |
| `clip_supersweet_visages.png`, `clip_supersweet_planche_A.png`, `clip_supersweet_planche_B.png` | Clip officiel Bratz « Super Sweet » (style Alwayz Bratz) : gros plans des visages, et une image toutes les 0,5 s. |
| `kylie_cheveux_avant_apres.png` | Cheveux de Kylie refaits avec le skill stylized-hair (validé en cloud). |

Camil a aussi deux enregistrements d'écran du clip (environ 20 s au total) et une page PDF du wiki Alwayz Bratz. À lui demander s'il faut les revoir.

### Ce que montre le clip « Super Sweet » (à copier)
- **Visages** : yeux en géométrie (paupière, gros cils séparés, iris avec reflets). Le **clin d'œil** ferme la paupière, courbe les cils vers le bas et fait un sourire en coin. Les **lèvres** sont énormes, arrondies, en **satin mat** (pas un gloss miroir). La peau est lisse, mate satinée, avec du blush.
- **Cheveux** : vraies mèches, des cheveux qui volent, des reflets doux. La méthode « masque » ne suffit que pour les coiffures serrées (le chignon de Kylie). Les cheveux longs demandent des courbes de cheveux.
- **Image** : lumière douce, ambiance colorée qui reprend le décor (ici, noir et or), halo lumineux (bloom), **arrière-plan toujours très flou**.
- **Montage** : plans de **0,5 à 1 s**, beaucoup d'**inserts macro** (yeux dans un rétro, plaque, main sur un bouton), plongée au fisheye, flous de mouvement, **flash blanc plein écran** pour changer de lieu, écran partagé pour l'appel, titre dessiné à la main qui scintille.

## 5. Skills ajoutés dans la session cloud (`.claude/skills/`)
Tous sont testés sur Blender 5.3 sans interface. Lire leur `SKILL.md` avant usage.
- **fast-eevee** : réglage rapide d'EEVEE et mesure du temps avant le rendu (`fast_eevee.py --apply --bench 6`). Rendre en 1920×804 et ajouter les bandes noires dans ffmpeg (`pad=1920:1080:0:138`). Ombres seulement sur les lumières principales.
- **fake-volumetrics** : faisceaux sous forme de cônes émissifs **parentés à chaque spot**, avec boîtier visible (`--fixtures`), fondu jusqu'au sol, et brume légère sur des plans. Remplace la vraie fumée volumétrique, lente et grise.
- **stylized-hair** : mode `--mask` pour les modèles Rodin d'un seul maillage. Il soude les coutures, peint un masque cheveux d'après la texture, lisse seulement les cheveux et mélange un shader brillant avec un anneau de reflet. Commande validée pour Kylie :
  ```bash
  /Applications/Blender.app/Contents/MacOS/Blender -b scene.blend -P .claude/skills/stylized-hair/scripts/stylized_hair.py -- \
    --mask Kylie --hair-rgb 0.133,0.075,0.059 --tol 0.12 --min-z 0.82 \
    --rgb 0.010,0.0065,0.0055 --smooth-iters 8 --grooves 30 --ring 0.35 --save
  ```
  Pour les autres personnages, mesurer `--hair-rgb` en échantillonnant la texture à l'arrière de la tête. Au-delà de 8 itérations de lissage, les boucles fines se déchiquettent.

## 6. Plan V3 (par ordre d'effet sur le résultat)
1. **Revoir la V2 avec Camil** et corriger les plans brûlés autour de l'arche (exposition du contre-jour).
2. **Montage façon clip** : découper en plans de 0,5 à 1 s calés sur la musique, ajouter des inserts macro (talons dans la laque, sequins, lèvres, cigarette et briquet, ticket, pochette), un flash blanc entre le défilé et l'après. Gros gain pour peu de rendu, et ça masque les défauts des modèles.
3. **Image cinéma** : faible profondeur de champ partout (f/1.4 à f/2.8 sur les gros plans), bloom (groupe Essentials Bloom dans la pile du compositeur 5.3), étalonnage noir et or.
4. **Cheveux** : appliquer stylized-hair à Kylie (commande ci-dessus), puis à Jade, Camil, Aurore et Florine, avec un gros plan de chacun à montrer.
5. **Visages expressifs de Kylie** (clin d'œil, bisou) : de vraies paupières et des shape keys (skill blender-facial-shapekeys), ou des textures de visage échangées sur le flash. Lèvres satinées plutôt que gloss.
6. Démarche (catwalk, demi-tour), matières (sequins, tissus non latex, Camil en gris), cigarette dans la main.
7. Son : musique pendant le défilé seulement, puis voix et ambiance (décisions de la DA). Camil doit fournir la musique et les voix.

Budget : rendu final de 1080 images en moins d'une heure, si possible. Toujours mesurer avec `fast_eevee.py --bench` avant de lancer.

## 7. Pièges connus
- **Mac en veille = rendu arrêté.** Lancer avec `caffeinate`, Mac branché, capot ouvert. Pour reprendre : `use_overwrite = False`, puis relancer les images manquantes.
- **Ne pas passer à Blender 5.4** avant le rendu du 24/11 : le projet est en 5.3.
- **Ne pas taper `/restart`** pendant un rendu.
- **Drive** : le connecteur refuse les fichiers de plus de 10 Mo. Une session cloud ne peut récupérer les zips Rodin que si Camil les rend publics, puis via `drive.usercontent.google.com/download?id=...&export=download&confirm=t`. Les remettre en privé ensuite.
- **MCP Blender** (ahujasid) : son installation a été bloquée par le mode auto (uv). Il n'est pas nécessaire : tout tourne en ligne de commande.
- **Dépôts de skills trouvés sur GitHub** (RobLe3/cc-blender-skill, etc.) : évalués, ils n'apportent rien de plus pour les cheveux, la vitesse de rendu, la fausse fumée ou les visages. Ne rien installer avec `npx -y` sans l'avoir lu.
- EEVEE ignore l'anisotropie : le reflet des cheveux est construit à part dans stylized-hair (anneau éclairé, calculé avec Shader to RGB).
- glTF découpe les sommets aux coutures UV. Il faut **souder avant de lisser**, sinon des fissures s'ouvrent.

## 8. Récupérer ce dossier sur le Mac
Le travail cloud est sur la branche `claude/cool-bardeen-kndshq`. Pour récupérer seulement les fichiers ajoutés, sans toucher au reste :
```bash
cd ~/claudedesignskills/bratz-ysl && git fetch origin claude/cool-bardeen-kndshq && git checkout FETCH_HEAD -- docs/PASSATION.md CLAUDE.md assets/refs .claude/skills/fast-eevee .claude/skills/fake-volumetrics .claude/skills/stylized-hair .claude/skills/SOURCES.txt
```
Attention : cette commande remplace `CLAUDE.md` par la version cloud. Si le Claude du Mac a modifié `CLAUDE.md` entre-temps, retirer `CLAUDE.md` de la commande et ajouter à la main la ligne vers ce document.
