# A word guessing game in Python using pygame library.
This game is based on the popular 2-player paper pencil game Hangman. 

The player has to guess a random word chosen by the game from selected topics. The game hints the player by showing an image related to the word and also reveals the number of letters in it. As the player enters a valid letter, the instances of that letter in the word get revealed and the word gets closer to completion. Whereas if the player enters a wrong letter, a hangman stick figure is developed. The player has to guess all letters in the word without making six wrong guesses.

As the player guesses more and more words, the game loads new levels raising the difficulty either by reducing the limit of wrong guesses or by not revealing the number of letters.


An exciting feature of this game is the ability to create your own quizzes by adding your own set of questions or downloading new set of questions based on preffered topic.

--------------------------
# Installation
- Clone/Download the repository.
- Make sure Python is installed. (Version 3.4 or above)
- Install pygame library for Python
```
pip install pygame
```
- Run the program "Hangman.py" in Python
```
python Hangman.py
```
- Enjoy the game!
---------------------------
# Gameplay
- Select preferred topics

![op1](https://user-images.githubusercontent.com/55421311/190084602-dbe55808-cf31-4201-9f44-b638094ba953.png)

- Start guessing. Try to avoid wrong guesses. As the word gets formed, guessing becomes easier.

![op2](https://user-images.githubusercontent.com/55421311/190085546-e8829c71-7261-4763-865e-e2471b2833c3.png)

- Finish words and advance to higher levels.

![op3](https://user-images.githubusercontent.com/55421311/190086015-209b0538-b7ab-45f5-8544-e7aacf6ff656.png)

![op4](https://user-images.githubusercontent.com/55421311/190086041-45dc1706-aa0e-405f-9867-25532198eb55.png)

- Break highscores and climb up the leaderboard!

![op5](https://user-images.githubusercontent.com/55421311/190086220-685e5289-00aa-46db-8263-13048f117efb.png)

------------------------------

This project makes use of technologies such as Python, Pygame library in Python for GUI, Digital Assets by freepik to enhance the look, cryptography for securing the game data. 

