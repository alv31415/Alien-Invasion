# Alien-Invasion :space_invader:

This project was developed following Eric Mathees' Python Crash Course, Second Edition. Its a the classic game, Alien Invasion, developed in Python using Pygame.

## Table of Contents

* [Additional Features](#additional-features)
* [To Do List](#to-do-list)
* [Pictures](#pictures)

## Additional Features

I introduced some of my own features that I believe improved the game experience:

* included a high scores button
  * displays the top 10 scores achieved by a player
  * after each game, the score of the game is saved
  * we extract a list from a json file
  * we introduce the new score into the list, and sort the list
  * we then take the first 10 elements
  * we store this new list into the json
* included instructions button
  * explains the basic functioning of the game
* added a title screen in the menu
* added a "level up screen" 
* additional functionality for quickly testing new features
  * "god-mode" increases the speed of the ship and bullets
  * "x-mode" increases the fall speed of the ship
  
## To Do List

- [ ] improve documentation
- [ ] add an options button to handle difficulty of the game, speed of ship, etc ...
- [ ] introduce power ups

## Pictures

The main menu:

<p align = "center">
  <img src = "https://github.com/alv31415/Alien-Invasion/blob/master/Alien%20Invasion%20Pictures/Screenshot%202020-08-20%20at%2011.07.22.png">
</p>

The instructions pane:

<p align = "center">
  <img src = "https://github.com/alv31415/Alien-Invasion/blob/master/Alien%20Invasion%20Pictures/Screenshot%202020-08-20%20at%2011.07.36.png">
</p>

The high-score pane:

<p align = "center">
  <img src = "https://github.com/alv31415/Alien-Invasion/blob/master/Alien%20Invasion%20Pictures/Screenshot%202020-08-20%20at%2011.07.52.png">
</p>

The level up screen:

<p align = "center">
  <img src = "https://github.com/alv31415/Alien-Invasion/blob/master/Alien%20Invasion%20Pictures/Screenshot%202020-08-20%20at%2011.08.09.png">
</p>

Game play:

<p align = "center">
  <img src = "https://github.com/alv31415/Alien-Invasion/blob/master/Alien%20Invasion%20Pictures/Screenshot%202020-08-20%20at%2011.08.29.png">
</p>
