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

All the libraries can be installed using ```pip``` running the following command from any Linux-based terminal
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

## Quick Setup
After installing all dependencies, proceed to create a new API application on [Discord Developer Portal](https://discord.com/developers/applications) and set it up as its needed. The bot token can be inserted at ```package/bot_config.py```.

## General Overview
The entire list of possible commands and flags can be shown with ```t.help```. Some of them can be pointed here, such as:

* ```t.item```: Shows every possible information of an item, such as its gerenal stats, crafting recipes and drop sources.
* ```t.list```: Points every possible item/NPC in data base starting with the command argument.
* ```t.rarity```: Shows a description list about each item rarity tier in Terraria (it can also be specified by passing the rarity tier as argument!).
* ```t.npc```: Shows every information about some specific in-game NPC, such as its conditions to spawn, its inventory and its drops.
* ```t.quest```: Briefly describes about an Angler's quest for an specified quest fish.
* ```t.craft```: Points each crafting recipe for the item given in the command argument.

And so on.

## Motivation
It was such a great experience working on this project aside with [Andrei](https://github.com/AndreiAlisson), from the data scrap to the bot development. As they say, practice makes perfect and I think we both are going further with our main goal as developers: being able to solve problems and work with creativity.

## Shoutouts
* [Official Terraria Gamepedia Wiki](https://terraria.fandom.com/wiki/), where all those data files come from.
* [Andrei Alisson](https://github.com/AndreiAlisson), my code mate.
* [Noas](https://www.instagram.com/noas.z/) with his gorgeous drawing skills.

## License
MIT.
