# Markdown 2 PDF

Un outil simple et efficace pour convertir des fichiers Markdown en PDF avec une interface graphique conviviale.

![Logo BeerCan](logo.png)

## Fonctionnalités

- Conversion d'un fichier Markdown unique en PDF
- Conversion par lot de tous les fichiers Markdown d'un dossier
- Interface graphique intuitive
- Prise en charge des tableaux Markdown
- Mise en page élégante des PDF générés

## Prérequis

- Python 3.6 ou supérieur
- wkhtmltopdf (doit être installé séparément)

## Installation

1. Clonez ce dépôt :
```bash
git clone https://github.com/votre-nom/markdown-2-pdf.git
cd markdown-2-pdf
```

2. Installez les dépendances Python :
```bash
pip install -r requirements.txt
```

3. Installez wkhtmltopdf :
   - Windows : [Télécharger l'installateur](https://wkhtmltopdf.org/downloads.html)
   - Linux : `sudo apt-get install wkhtmltopdf`
   - macOS : `brew install wkhtmltopdf`

## Utilisation

Lancez l'application :
```bash
python main.py
```

1. Cliquez sur "Sélectionner un fichier" ou "Sélectionner un dossier"
2. Choisissez le fichier Markdown ou le dossier contenant des fichiers Markdown
3. Cliquez sur "Convertir en PDF"
4. Les fichiers PDF seront générés au même emplacement que les fichiers Markdown

## Exemples

### Structure de tableau prise en charge

Le Markdown :
```markdown
| Nom | Âge | Ville |
|-----|-----|-------|
| Jean | 25 | Paris |
| Marie | 30 | Lyon |
```

Sera correctement converti en tableau dans le PDF généré.

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteur

Développé par [BeerCan.fr](https://beercan.fr)
