# Algorithm – Hangman Game Feature Set C

1. Start the program.
2. Display the Hangman game interface.
3. Let the player select a category.
4. Let the player select a difficulty level.
5. According to the selected difficulty, set the number of attempts and timer.
6. Randomly select a word and its hint from the selected category and difficulty.
7. Display blank spaces for the letters of the selected word.
8. Start the countdown timer.
9. Ask the player to enter one letter.
10. Check whether the letter is already guessed.
11. If the letter is in the word:
    - Reveal the letter.
    - Increase the score.
12. Otherwise:
    - Reduce the remaining attempts.
    - Reduce the score slightly.
13. If the player requests a hint:
    - Display the word hint.
    - Reveal one hidden letter.
    - Apply the difficulty-based score penalty.
14. Check whether all letters have been revealed.
15. If all letters are revealed:
    - Declare the player the winner.
    - Add the winning bonus.
    - Update the high score.
16. If attempts become zero or the timer reaches zero:
    - Declare game over.
    - Reveal the word.
    - Update the high score if required.
17. Allow the player to start/replay another game.
18. Stop.
