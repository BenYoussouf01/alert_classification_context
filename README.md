# alert_classification_context
Ce depot contient tous les fichier lié au projet de ''VERS UNE CLASSIFICATION CONTEXTUELLE DES ALERTES DANS LES CENTRES D’OPÉRATIONS DE SÉCURITÉ À L’AIDE DE LLMS''
# NVTESTE2 — SOC Alert Triage Experiments

Ce dépôt contient des scripts pour évaluer la stabilité des décisions de triage SOC (interesting / not‑interesting) à partir d’alertes SIEM JSON, avec et sans contexte métier.

## Contenu
- `contexte.json` : contexte métier (groupes, utilisateurs, assets, horaires, policies, etc.).
- `alert-linux.json`, `Alertes-wind.json` : alertes d’entrée (JSON).
- `script-runs-contexte-base.py` : exécute N runs avec contexte.
- `script-runs-no-contexte-base.py` : exécute N runs sans contexte.
- `Script-analyse.py`, `script-analyse2.py` : analyse de stabilité (S_conf, distribution, variations).

## Prérequis
- Python 3.10+
- `together` (SDK API Together)

Installation typique :
```
pip install together
```

## Configuration
Définir la clé :
```
setx TOGETHER_API_KEY "xxx"
```

## Exécution (runs)
### Avec contexte
```
python script-runs-contexte-base.py
```

### Sans contexte
```
python script-runs-no-contexte-base.py
```

## Analyse
```
python Script-analyse.py
python script-analyse2.py
```

## Points à vérifier (noms de fichiers)
Certains scripts écrivent/lisent des noms différents :
- `script-runs-contexte-base.py` écrit `NoContext-results_runs-windows.json` mais affiche `Context-results_runs-linux.json`.
- `script-runs-no-contexte-base.py` écrit `essairuns-windowsvrai windows.json` mais affiche `essairuns-windows.json`.

Il est conseillé d’unifier ces noms dans les scripts pour éviter la confusion.

## Licence
À compléter.
