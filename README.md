# Space_Levels_game
A game for fun!

## Content I would like to add:

* save/load menu this should be simple enough, on save write a list of the current attributes of the object as well as the level and any other relevant data, then if load is True
have an if statement when loading the character implementing all of the relevant parameters. 

* add more level-ups: even though this would not show many more skills for personal enjoyment. perhaps I could make a horizontal Laser as a bullet level, this could have damage
proportional to bullet speed? maybe made up of several rectangles that are masked and on hit with the enemy will stop, giving the effect that part of the laser, that isn’t hitting the 
enemy carries on as expected. Maybe some particles where the enemy is hit for more effect?

* more interactive level-up page, I feel giving the user more customizability will encourage more test builds to find the best, this will increase playtime which in turn I guess
is a goal... maybe on clicking a button on the main page, or a key-binded to that button an upgrade menu will pop up, with skill names and next to them plus buttons.

* A story mode would be fun to add, with designed levels and bosses instead of a random wave game.

* A two-player mode

* A high scores list, when a player dies or clicks to close space_levels_game check the current score and maybe a class responsible for a high scores menu, a class method can check
if the score is higher than the ones currently on the high score if it adds the score to the correct place, and delete the lowest score. again these scores can be stored in a txt
or JSON file and loaded in when the score menu is opened?
