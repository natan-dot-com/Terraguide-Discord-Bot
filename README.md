# Discord Terraria Bot

<p align="center">
<img src=https://img.shields.io/badge/Status-In%20Progress-yellow>&nbsp;&nbsp;&nbsp;<img src=https://img.shields.io/badge/Version-v0.1-lightgray>
</p>

### Table of contents
- [1. Resumé](#1-resumé)
- [2. Authors](#2-authors)
- [3. Dependencies](#3-dependencies)
  * [3.1. Linux](#31-linux)
  * [3.2. Windows](#32-windows)
- [4. Quick Setup](#4-quick-setup)
- [5. General Overview](#5-general-overview)
- [6. Changelog](#6-changelog)
- [7. Motivation](#7-motivation)
- [8. Acknowledgements](#8-acknowledgements)
- [9. License](#9-license) 


## 1. Resumé
As the name suggests, it's a bot created using [Discord's Python API](https://discord.com/developers/docs/intro) intented to be a Discord built-in information wiki for every Terraria player. Its content is based on general item/NPC information and its respective crafting recipes, grab bag drops, enemy drops and selling offers from NPCs, as well as having some extra commands about rarity tiers and Angler quests.

## 2. Authors
All the bot's source were made by [me](https://github.com/natan-dot-com) and [Andrei Alisson](https://github.com/AndreiAlisson).

## 3. Dependencies
Discord Terraria Bot uses some specific Python libraries to work. In order to proceed with the setup, you may need to install some of them. 

### 3.1. Linux
From the beggining, you may also need to install a Python package manager in order to proceed with the libraries installation if you don't have one already. Here we'll be using the awesomeness of ```pip```, which can be installed via
```
sudo apt install python3-pip
```
in any Ubuntu-based distribution.

All the libraries can be installed using ```pip``` running the following command from any Linux-based terminal
```
pip install discord.py levenshtein colorthief colormap
```
---

### 3.2. Windows
Similar to Linux, Python needs a package manager in order to install each one of the libraries and we'll be using ```pip``` as well. In Windows, save [get-pip.py](https://bootstrap.pypa.io/get-pip.py) in any directory and run the script using ```python get-pip.py``` (assuming that you already have Python installed) on the Windows Powershell, from the directory that the file has been saved.

The next one will be simple: We can use
```
pip install discord.py levenshtein colorthief colormap
```
into the Windows Powershell to install the remaining dependencies.

## 4. Quick Setup
After installing all dependencies, proceed to create a new API application on [Discord Developer Portal](https://discord.com/developers/applications) and set it up as its needed. The bot token can be inserted at ```package/bot_config.py```.

## 5. General Overview
The entire list of possible commands and flags can be shown with ```t.help```. Some of them can be pointed here, such as:

* ```t.item```: Shows every possible information of an item, such as its gerenal stats, crafting recipes and drop sources.
* ```t.list```: Points every possible item/NPC in data base starting with the command argument.
* ```t.rarity```: Shows a description list about each item rarity tier in Terraria (it can also be specified by passing the rarity tier as argument!).
* ```t.npc```: Shows every information about some specific in-game NPC, such as its conditions to spawn, its inventory and its drops.
* ```t.quest```: Briefly describes about an Angler's quest for an specified quest fish.
* ```t.craft```: Points each crafting recipe for the item given in the command argument.

And so on.

## 6. Changelog
Changes and updates can be tracked from the [Changelog](changelog.md) file!

## 7. Motivation
It was such a great experience working on this project aside with [Andrei](https://github.com/AndreiAlisson), from the data scrap to the bot development. As they say, practice makes perfect and I think we both are going further with our main goal as developers: being able to solve problems and work with creativity.

## 8. Acknowledgements
* [Official Terraria Gamepedia Wiki](https://terraria.fandom.com/wiki/), where all those data files come from.
* [Andrei Alisson](https://github.com/AndreiAlisson), my code mate.
* [Noas](https://www.instagram.com/noas.z/) with his gorgeous drawing skills.

## 9. License
MIT.
