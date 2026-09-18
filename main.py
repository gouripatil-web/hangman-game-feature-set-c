import tkinter as tk
from tkinter import messagebox
import random

WORD_BANK = {
    "Animals": {
        "Easy": [("CAT", "A common pet that says meow."), ("DOG", "A common pet that barks."),
                 ("LION", "A large wild cat known as the king of the jungle.")],
        "Medium": [("ELEPHANT", "The largest land animal."), ("GIRAFFE", "An animal with a very long neck."),
                   ("PENGUIN", "A flightless bird that lives in cold regions.")],
        "Hard": [("CHIMPANZEE", "A highly intelligent great ape."), ("CROCODILE", "A large reptile with powerful jaws."),
                 ("KANGAROO", "An Australian animal that moves by jumping.")]
    },
    "Technology": {
        "Easy": [("CODE", "Instructions written for a computer."), ("JAVA", "A popular programming language."),
                 ("MOUSE", "A computer pointing device.")],
        "Medium": [("PYTHON", "A popular programming language named after a snake."),
                   ("DATABASE", "An organized collection of data."),
                   ("ALGORITHM", "A step-by-step method for solving a problem.")],
        "Hard": [("CRYPTOGRAPHY", "The practice of securing information using codes."),
                 ("MULTITHREADING", "Executing multiple threads within a process."),
                 ("NEURALNETWORK", "A computing model inspired by the brain.")]
    },
    "Sports": {
        "Easy": [("CRICKET", "A bat-and-ball sport popular in India."),
                 ("TENNIS", "A racket sport played over a net."),
                 ("GOAL", "A score in many sports.")],
        "Medium": [("FOOTBALL", "A sport played by two teams trying to score goals."),
                   ("BADMINTON", "A racket sport played with a shuttlecock."),
                   ("BASKETBALL", "A sport where players try to score in a hoop.")],
        "Hard": [("VOLLEYBALL", "A team sport in which the ball is hit over a net."),
                 ("GYMNASTICS", "A sport involving strength, balance and flexibility."),
                 ("TABLETENNIS", "A racket sport played on a table with a small ball.")]
    }
}

DIFFICULTY = {
    "Easy": {"attempts": 8, "time": 90, "hint_penalty": 5},
    "Medium": {"attempts": 6, "time": 60, "hint_penalty": 10},
    "Hard": {"attempts": 5, "time": 45, "hint_penalty": 15},
}

class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game - Feature Set C")
        self.root.geometry("720x620")
        self.root.resizable(False, False)

        self.category = tk.StringVar(value="Animals")
        self.difficulty = tk.StringVar(value="Easy")
        self.guess_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Choose category and difficulty, then start the game.")
        self.timer_var = tk.StringVar(value="Time: --")
        self.score_var = tk.StringVar(value="Score: 0")
        self.high_score = 0

        self.word = ""
        self.hint = ""
        self.guessed = set()
        self.remaining_attempts = 0
        self.score = 0
        self.time_left = 0
        self.timer_running = False

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="HANGMAN", font=("Arial", 28, "bold")).pack(pady=12)
        tk.Label(self.root, text="Feature Set C: Category • Difficulty • Timer • Hints • Score/High Score",
                 font=("Arial", 10)).pack()

        controls = tk.Frame(self.root)
        controls.pack(pady=15)

        tk.Label(controls, text="Category:").grid(row=0, column=0, padx=5)
        tk.OptionMenu(controls, self.category, *WORD_BANK.keys()).grid(row=0, column=1, padx=5)

        tk.Label(controls, text="Difficulty:").grid(row=0, column=2, padx=5)
        tk.OptionMenu(controls, self.difficulty, *DIFFICULTY.keys()).grid(row=0, column=3, padx=5)

        tk.Button(controls, text="Start / Replay", command=self.start_game, width=14).grid(row=0, column=4, padx=10)

        info = tk.Frame(self.root)
        info.pack()
        tk.Label(info, textvariable=self.timer_var, font=("Arial", 13, "bold")).grid(row=0, column=0, padx=25)
        tk.Label(info, textvariable=self.score_var, font=("Arial", 13, "bold")).grid(row=0, column=1, padx=25)
        self.attempts_label = tk.Label(info, text="Attempts: --", font=("Arial", 13, "bold"))
        self.attempts_label.grid(row=0, column=2, padx=25)

        self.word_label = tk.Label(self.root, text="Start a game", font=("Courier", 26, "bold"))
        self.word_label.pack(pady=28)

        self.guessed_label = tk.Label(self.root, text="Guessed letters: None", font=("Arial", 11))
        self.guessed_label.pack(pady=5)

        guess_frame = tk.Frame(self.root)
        guess_frame.pack(pady=12)
        tk.Label(guess_frame, text="Enter letter:").pack(side="left", padx=5)
        self.guess_entry = tk.Entry(guess_frame, textvariable=self.guess_var, width=8,
                                    font=("Arial", 16), justify="center")
        self.guess_entry.pack(side="left", padx=5)
        self.guess_entry.bind("<Return>", lambda event: self.make_guess())
        tk.Button(guess_frame, text="Guess", command=self.make_guess, width=10).pack(side="left", padx=5)

        tk.Button(self.root, text="Use Hint", command=self.use_hint, width=14).pack(pady=8)

        self.hint_label = tk.Label(self.root, text="Hint: ---", font=("Arial", 11), wraplength=600)
        self.hint_label.pack(pady=5)

        tk.Label(self.root, textvariable=self.status_var, font=("Arial", 11), wraplength=650).pack(pady=18)
        tk.Label(self.root, text="Score rules: correct letters +10, wrong letter -2, hint -penalty, win +20.",
                 font=("Arial", 9)).pack(side="bottom", pady=12)

    def start_game(self):
        self.timer_running = False
        cfg = DIFFICULTY[self.difficulty.get()]
        self.word, self.hint = random.choice(WORD_BANK[self.category.get()][self.difficulty.get()])
        self.guessed.clear()
        self.remaining_attempts = cfg["attempts"]
        self.time_left = cfg["time"]
        self.score = 0
        self.guess_var.set("")
        self.timer_running = True
        self.hint_label.config(text="Hint: ---")
        self.status_var.set("Game started! Guess one letter at a time.")
        self.update_display()
        self.tick()
        self.guess_entry.focus_set()

    def update_display(self):
        display = " ".join(letter if letter in self.guessed else "_" for letter in self.word)
        self.word_label.config(text=display)
        guessed_text = ", ".join(sorted(self.guessed)) if self.guessed else "None"
        self.guessed_label.config(text=f"Guessed letters: {guessed_text}")
        self.score_var.set(f"Score: {self.score}")
        self.attempts_label.config(text=f"Attempts: {self.remaining_attempts}")

    def make_guess(self):
        if not self.timer_running:
            messagebox.showinfo("Game", "Please start a new game first.")
            return

        letter = self.guess_var.get().strip().upper()
        self.guess_var.set("")

        if len(letter) != 1 or not letter.isalpha():
            self.status_var.set("Please enter exactly one alphabet letter.")
            return

        if letter in self.guessed:
            self.status_var.set("You already guessed that letter.")
            return

        self.guessed.add(letter)

        if letter in self.word:
            self.score += 10
            self.status_var.set(f"Good guess! '{letter}' is in the word.")
        else:
            self.remaining_attempts -= 1
            self.score = max(0, self.score - 2)
            self.status_var.set(f"'{letter}' is not in the word.")

        self.update_display()
        self.check_end()

    def use_hint(self):
        if not self.timer_running:
            messagebox.showinfo("Game", "Please start a new game first.")
            return

        hidden = [letter for letter in self.word if letter not in self.guessed]
        if not hidden:
            self.status_var.set("All letters are already revealed.")
            return

        letter = random.choice(hidden)
        self.guessed.add(letter)
        penalty = DIFFICULTY[self.difficulty.get()]["hint_penalty"]
        self.score = max(0, self.score - penalty)
        self.hint_label.config(text=f"Hint: {self.hint}  (Penalty: {penalty} points)")
        self.status_var.set(f"Hint used. The letter '{letter}' has been revealed.")
        self.update_display()
        self.check_end()

    def check_end(self):
        if all(letter in self.guessed for letter in self.word):
            self.timer_running = False
            self.score += 20
            self.high_score = max(self.high_score, self.score)
            self.score_var.set(f"Score: {self.score} | High Score: {self.high_score}")
            self.status_var.set(f"🎉 You won! The word was {self.word}.")
            messagebox.showinfo("You Won!", f"Congratulations!\nWord: {self.word}\nScore: {self.score}\nHigh Score: {self.high_score}")
        elif self.remaining_attempts <= 0:
            self.end_game("No attempts left.")
        elif self.time_left <= 0:
            self.end_game("Time's up!")

    def end_game(self, reason):
        self.timer_running = False
        self.word_label.config(text=" ".join(self.word))
        self.high_score = max(self.high_score, self.score)
        self.score_var.set(f"Score: {self.score} | High Score: {self.high_score}")
        self.status_var.set(f"Game over: {reason} The word was {self.word}.")
        messagebox.showinfo("Game Over", f"{reason}\nThe word was: {self.word}\nScore: {self.score}\nHigh Score: {self.high_score}")

    def tick(self):
        if not self.timer_running:
            return

        self.timer_var.set(f"Time: {self.time_left}s")
        if self.time_left <= 0:
            self.check_end()
            return

        self.time_left -= 1
        self.root.after(1000, self.tick)

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanApp(root)
    root.mainloop()
