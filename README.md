# Terraria-Fishing-Bot

This program automates the task of fishing in the video game Terraria by clicking on the screen and reeling in the fishing pole as soon as movement is detected.
It can also accomplish several other tasks related to fishing, such as quickstacking items, opening crates and taking potions.
I have only tested it on Windows 10 so far, but it could work on other systems.

## Setup
* Download the executable from the releases tab on github.
* Start it.
* Make sure your antivirus does not block the program. Any message saying that it is a virus is false, but - in the case that you do not trust a random internet stranger such as myself - you can also run the bot in a completely safe way, as described below.
* Give it admin permissions.
  * Unfortunately, Terraria blocks all virtual keyboard and mouse inputs that do not have admin permissions. 

If you do not trust the executable, the source code is also available. You will have to install python and a few libraries if you want to use it instead. (Using the script would still require admin permissions, but you would be able to look at the code.)

## Usage
* Click 'Start'.
* Follow the Instructions that appear.
  * Position yourself on a platform above a fishing lake.
  * Select your fishing rod in your hotbar.
  * Turn off waves in Settings>Video>Waves Quality

![instructions1](https://user-images.githubusercontent.com/62914261/124031030-1a84ea80-d9f7-11eb-9dd2-57f9c7d59cde.PNG)
  * Press ok, then position your mouse cursor like this:

![instructions2](https://user-images.githubusercontent.com/62914261/124031294-6cc60b80-d9f7-11eb-84af-08d586c473e2.PNG)

  * Press ALT to confirm the liquid level and let the bot fish for you as long as you have bait! (Do not move your mouse from here on out. To stop the bot, hold ALT again.)

## Settings
![bot](https://user-images.githubusercontent.com/62914261/124027267-f4f5e200-d9f2-11eb-8a1e-76b578071538.PNG)

- [x] **Stop fishing on blood moon**
  - Only applicable to fishing in water
  - Generally recommended, as you will be killed while AFK otherwise
- [ ] **Take buffs every** 3 **minutes**
  - The bot presses 'b' in the given interval
  - Already active potions are not consumed
  - Recommended, if you have a lot of fishing/crate potions
- [ ] **Quickstack**
  - Automatically quickstack all loot to nearby chests
  - Inventory has to be open (Autopause disabled)
  - Hotbar should be filled
  - Generally recommended, if possible
- [ ] **Open crates**
  - Automatically opens all fished crates (except for quickstacked ones)
  - Last slot in your inventory should be free
  - Activates Quickstack -> Same things apply
  - Only really useful to replenish potions and bait
  - (Can sometimes accidentally switch fished equipment with equipped equipment)

  **Contrast** 400
  - Only change if bot is unreliable
  - Lower if not every fish is caught
  - Higher if pole is reeled in without a fish


### Liquid
Select in which liquid you are trying to fish
* Water
  * Beware of bloodmoon
* Lava
  * Lava bubbles can sometimes trigger the bot
  * Special equipment or fishing rod required
* Honey
  * Only catch Honeyfins


### Screen settings
Advanced settings, only change if the bot clicks on the wrong spots.


## Basic Troubleshooting
### It does not do *anything*
It is possible that you have not run the program with admin permissions.

### Fishing is unreliable
If the bot is not functioning properly, look at the debug image:

![debug](https://user-images.githubusercontent.com/62914261/124031992-48b6fa00-d9f8-11eb-9641-4cb04fb1893f.PNG)

The white line is the "sight" of the bot. Ensure the bobber is touching the line.
If there are still problems, try messing with the contrast setting.
