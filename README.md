# Astrophysics-For-Gamers-in-a-Hurry

APFGIH is game designed to be a fun and interactive learning experience for people of all ages. 

## Installation

#### Windows

To start this game, first install python >3.6 from [python.org](https://www.python.org/). After starting the installer please check
"Add Python to PATH".

When the installer is finished, reboot your computer.

Launch CMD or Command Prompt by entering CMD in the search box or hitting Ctrl-R and entering cmd.

Enter the following commands
```
pip install pygame
pip install pytmx
pip install firebase_admin
pip install numpy
pip install googlecloudfirestore
```

Now double click main.py and the game should start.

#### Linux/MacOS

Start terminal and enter 
```
sudo pip3 install pygame
sudo pip3 install pytmx
sudo pip3 install firebase_admin
sudo pip3 install numpy
sudo pip3 install googlecloudfirestore
```

Now double click main.py and the game should start.

## File Structure

#### main.py
Contains the main menu and the authentication for the game. All database access happens here.

#### game.py
Contains the main game created in pygame. All player movements are processed here.

#### Map/Map.py
Contains the code for the Map object. A rendering method is called every iteration to draw the map and various items on the screen.
We use specific layer names to help organize. All layers MUST remain the same name during modifications.

#### Minigames/
This folder contains all the minigames in the game. All minigames must be in a function that takes in the screen object. The minigame
must include its own game loop and input processing as the main game is paused. If a game is completed successfully, return true, otherwise return false.

## Sources
*	“Alpha Centauri: A Triple Star System about 4 Light Years from Earth.” NASA, NASA, nasa.gov/mission_pages/chandra/images/alpha-centauri-a-triple-star-system-about-4-light-years-from-earth.html.
*	“Escape Velocity.” Wikipedia, Wikimedia Foundation, en.wikipedia.org/wiki/Escape_velocity.
*	“What is an Orbit?” NASA, NASA, nasa.gov/audience/forstudents/5-8/features/nasa-knows/what-is-orbit-58.html.
*	“Jupiter.” NASA, NASA, solarsystem.nasa.gov/planets/jupiter/overview/.
*	“Basics of Space Flight - Solar System Exploration: NASA Science.” NASA, NASA, solarsystem.nasa.gov/basics/primer/.
*	“Sun.” NASA, NASA, solarsystem.nasa.gov/solar-system/sun/overview/.
*	“What is a Black Hole?” NASA, NASA, nasa.gov/audience/forstudents/5-8/features/nasa-knows/what-is-a-black-hole-58.html.
*	“Messier 42 (The Orion Nebula).” NASA, NASA, nasa.gov/feature/goddard/2017/messier-42-the-orion-nebula.
*	“Neutron Stars.” NASA, NASA, imagine.gsfc.nasa.gov/science/objects/neutron_stars1.html.
*	“What is a Supernova.” NASA, NASA, nasa.gov/audience/forstudents/5-8/features/nasa-knows/what-is-a-supernova.html.
*	Manley, Scott. How Gravity Assists Work. YouTube, YouTube, 25 Sept. 2017, www.youtube.com/watch?v=16jr7WWGSxo.
*	Hiyu. Hiyu Explains Rocket Science! YouTube, YouTube, 13 Oct. 2017, www.youtube.com/watch?v=p-GqfY2qdHQ.
*	“Speedrunning Marathons for Charity.” Games Done Quick, gamesdonequick.com/.
*	Seaheroquest.com, www.seaheroquest.com/site/en/.
## References (basically stuff that is added in for fun)
*	Star Trek
*	Starbound
*	Darkest Dungeon
*	Astrophysics for people in a hurry
*	Stellaris
*	Warframe
*	Emoticon
*	H.P. Lovecraft
*	Minecraft
*	Fortnite
*	Bongo Cat
*	Kerbal Space Program
*	Undertale
*	Rahcraft

_Created by: Jason Qaun, Adam Medhi, Henry Tu, Ryan Zhang for ENG4U_

Code is forked off of [RahCraft](https://github.com/RahCraft/RahCraft) and [HUBG](https://github.com/RASTERA).
