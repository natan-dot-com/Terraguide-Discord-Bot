# Discord Terraria Bot

## Resumé
As the name suggests, it's a bot created using [Discord's Python API](https://discord.com/developers/docs/intro) intented to be a Discord built-in information wiki for every Terraria player. Its content is based on general item/NPC information and its respective crafting recipes, grab bag drops, enemy drops and selling offers from NPCs, as well as having some extra commands about rarity tiers and Angler quests.

## Authors
All the bot's source were made by [me](https://github.com/natan-dot-com) and [Andrei Alisson](https://github.com/AndreiAlisson).

## Dependencies
Discord Terraria Bot uses some specific Python libraries to work. In order to proceed with the setup, you may need to install some of them. 

### Linux
From the beggining, you may also need to install a Python package manager in order to proceed with the libraries installation if you don't have one already. Here we'll be using the awesomeness of ```pip```, which can be installed via
```
sudo apt install python3-pip
```
in any Ubuntu-based distribution.

All of the libraries can be installed using ```pip``` running the following command from any Linux-based terminal
```
pip install discord.py levenshtein colorthief colormap
```
---

### Windows
Similar to Linux, Python needs a package manager in order to install each one of the libraries and we'll be using ```pip``` as well. In Windows, save [get-pip.py](https://bootstrap.pypa.io/get-pip.py) in any directory and run the script using ```python get-pip.py``` (assuming that you already have Python installed) on the Windows Powershell, from the directory that the file has been saved.

The next one will be simple: We can use
```
pip install discord.py levenshtein colorthief colormap
```
into the Windows Powershell to install the remaining dependencies.

## Introduction

## License
MIT.
