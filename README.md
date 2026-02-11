# NVTESTE2 — SOC Alert Triage Experiments

Ce dépôt contient des scripts pour évaluer la stabilité des décisions de triage SOC (interesting / not‑interesting) à partir d’alertes SIEM JSON, avec et sans contexte métier.

## Reproduction minimale (fichiers indispensables)
- `contexte.json` : contexte métier (primordial).
- `alertes-linux.json`, `alertes-windows.json` : alertes d’entrée (JSON).
- `script-runs-contexte-base.py` : exécute N runs avec contexte.
- `script-runs-no-contexte-base.py` : exécute N runs sans contexte.
- `script-analyse2.py` : analyse des résultats (S_conf, distribution, variations).

## Fichiers de résultats (générés)
- `Context-results_runs-linux.json` : résultats des runs **avec** contexte (Linux).
- `contextresults_runs-windows.json` : résultats des runs **avec** contexte (Windows).
- `NoContext-results_runs-linux.json` : résultats des runs **sans** contexte (Linux).
- `NoContext-results_runs-windows.json` : résultats des runs **sans** contexte (Windows).

## Fichiers d’analyse (générés)
- `Context-analysis_runs-linux1.json` : analyse des runs **avec** contexte (Linux) produite par `script-analyse2.py`.
- `analysis-linux-sansContexte.json` : analyse des runs **sans** contexte (Linux).
- `analysis-windows-sansContexte.json` : analyse des runs **sans** contexte (Windows).

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

## Étapes minimales
1. Installer les dépendances.
```
pip install together
```
2. Définir la clé API.
```
setx TOGETHER_API_KEY "xxx"
```
3. Lancer les runs avec contexte.
```
python script-runs-contexte-base.py
```
4. Lancer les runs sans contexte.
```
python script-runs-no-contexte-base.py
```
5. Générer l’analyse.
```
python script-analyse2.py
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
python script-analyse2.py
```

## Partage (fichiers à ignorer)
Pour partager le projet sans alourdir le dépôt, éviter d’inclure les fichiers de résultats volumineux et leurs analyses générées :
- `Context-results_runs-linux.json`
- `contextresults_runs-windows.json`
- `NoContext-results_runs-linux.json`
- `NoContext-results_runs-windows.json`
- `Context-analysis_runs-linux1.json`
- `analysis-linux-sansContexte.json`
- `analysis-windows-sansContexte.json`

## Licence
À compléter.
