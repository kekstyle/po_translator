# 🎯 Po Translator v1.0

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB.svg?style=flat)](https://www.python.org/)
[![Windows App](https://img.shields.io/badge/Platform-Windows-blue)](https://github.com/)
[![License](https://img.shields.io/badge/License-Personnelle-lightgrey)](#license)
[![Version](https://img.shields.io/badge/Version-1.0-orange)](#)
[![Linux Compatible](https://img.shields.io/badge/Platform-Linux-green)](#installation-sur-linux)

Po Translator est une application Windows pour traduire et éditer facilement des fichiers `.po` et `.mo`. Elle combine automatisation via `deep-translator` et contrôle manuel avec une interface graphique intuitive. Une solution rapide et élégante pour localiser vos projets sans effort.

---

## 🚀 Fonctionnalités clés

- 🔄 Traduction automatique des fichiers `.po` (balises et variables conservées)
- 🧾 Édition interactive des fichiers `.mo`
- 💡 Suggestion alternative intelligente pour chaque ligne
- ⚡ Conversion `.po` → `.mo` en un clic
- 🎨 Interface utilisateur moderne en Tkinter
- 📦 Exécutable Windows prêt à l’emploi (`.exe` autonome avec icône personnalisée)
- 🧠 Nettoyage automatique des entités et ponctuation

---

## 🧰 Technologies

- [`polib`](https://github.com/izimobil/polib) – Manipulation des fichiers `.po`/`.mo`
- [`deep-translator`](https://github.com/nidhaloff/deep-translator) – Traduction automatique
- `tkinter` – Interface graphique intégrée à Python

---

## 📦 Installation

### Windows 

Aucune installation nécessaire.  
Télécharge simplement le fichier `po_translator.exe` et double-clique !

> ✅ Python n’est **pas requis** sur le PC cible — tout est embarqué via PyInstaller.

## 🐧 Installation sur Linux

> ⚠️ Requiert Python 3.10+ installé sur le système

### Étapes d’installation :

1. Télécharge l’archive `po_translator_linux.tar.gz` depuis la [section Releases]([https://github.com/...](https://github.com/kekstyle/po_translator/tree/main/Linux)) du dépôt
2. Ouvre un terminal et rends-toi dans ton dossier de téléchargement :
	```bash
	cd ~/Téléchargements
3.Décompresse l’archive :

	```bash
	tar -xzvf po_translator_linux.tar.gz
4.Rends le script exécutable :

	```bash
	chmod +x install.sh
5.Lance l’installation :

	```bash
	./install.sh


📁 Les fichiers seront installés dans un répertoire local. 🖼️ Un raccourci .desktop sera créé si tu utilises GNOME ou KDE — tu pourras lancer l’appli depuis ton menu d'applications.


## 💻 Utilisation

1. Lance l’application `po_translator.exe`
2. Sélectionne ton fichier `.po` ou `.mo`
3. Utilise les boutons “Traduire”, “Éditer”, ou “Compiler”
4. Les modifications sont enregistrées automatiquement à la fin du traitement

---

## ✨ Suggestions de traduction

- Reformulation proposée automatiquement pour chaque ligne
- Amélioration du style, ponctuation, et fluidité
- Respect des balises HTML, variables, dates, etc.
- Nettoyage des entités HTML incorrectes (`&#123;`, etc.)

---

## 🗓️ À venir

- 🔍 Barre de recherche dans les entrées `.mo`
- 🌍 Choix de langues personnalisable
- 🧠 Suggestions multiples cliquables
- 📜 Historique des traductions
- 🖼 Mode clair / sombre

---

## 👤 Auteur

Développé par [MakerLab.fr](https://makerlab.fr)  
Modifications et interface graphique par **Kekstyle** 🤝

---


## 📄 Licence

Ce projet est sous licence **Creative Commons Attribution - Pas d’Utilisation Commerciale - Partage dans les Mêmes Conditions 4.0 International (CC BY-NC-SA 4.0)**.  
Vous êtes libre de le modifier et de le redistribuer, tant que vous :
- créditez l’auteur original,
- n’en faites pas un usage commercial,
- conservez la même licence pour toute version modifiée.

🔗 [Voir les termes complets de la licence](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr)

© 2025 MakerLab.fr
