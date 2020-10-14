# superghost-computer
A superghost bot called Zyka that YOU can play with! She will *always* return the best moves, so don't expect to win without serious strategy!
^-^

Superghost is a traditional pen-and-paper game, and more information about the rules can be found here: https://www.wikiwand.com/en/Ghost_(game)

## How to use
Simply download all the files, then run game.py. This is a command-line game, and will prompt you on how to play. 

All you really have to do is to follow the instructions - when it's your turn, add a letter. For example, if the string "denti" is already on the board, you can type "dentis" to go for the word "dentist".

At any point during your turn, you can type /ch to challenge, and follow the prompts to challenge Zyka. This ends the round, and depending on whether or not the challenge was successful, you or Zyka will score a point.

## How it's made
This simple python app sits on the foundation of https://github.com/danielq987/superghost-tree. Essentially that program generates a tree of all the possible moves which can be achieved in a game of two-person superghost, and labels each as a goal for player 1 or player 2. 

This app simply traverses that tree to find the guaranteed winning move and subsequent moves, as well as choosing the move with the highest probability of winning if there is no guaranteed win. More info about this project can be found on my not-yet-existing blog (hopefully up soon)!

