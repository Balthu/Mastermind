"""
__author__: Balthurion
__mail__: lgoffaux@gmail.com
__version__: 1.0

Mastermind Game Rules (Solo Mode)

Objective: The objective of Mastermind is to guess the secret color code created by the computer within a limited
number of attempts.

Setup: - The computer randomly generates a sequence of 4 colors. This sequence is the "mystery line" that the player
needs to guess. - The possible colors are represented by different colored buttons: Yellow, Blue, Red, Green, White,
Black, Purple, and Pink.

Gameplay:
    1. Starting the Game:
        - The player begins with 10 attempts to guess the mystery line.
        - Only the buttons on the last row are enabled initially.

    2. Making a Guess:
        - The player clicks on the buttons to change their colors and create a guess.
        - Each button cycles through the available colors with each click.

    3. Validating a Guess: - Once the player has selected colors for all four positions in the current row,
    they click the "Validate" button. - The computer then provides feedback on the guess.

    4. Feedback:
        - Feedback is given using color-coded pegs:
            - Green Peg: Indicates a correct color in the correct position.
            - Orange Peg: Indicates a correct color in the wrong position.
        - The feedback pegs are displayed next to the guess row.

    5. Disabling Rows:
        - After validation, the current row is disabled.
        - If there are remaining attempts, the next row becomes active for the player to make a new guess.

    6. Winning the Game: - The player wins if they guess the correct sequence (all four colors in the correct
    positions) within the allowed attempts. - A message box will appear stating "You win!!!"

    7. Losing the Game:
        - If the player exhausts all 10 attempts without guessing the correct sequence, they lose.
        - The mystery line is revealed.
        - A message box will ask if the player wants to play again.

Restarting the Game:
    - The player can start a new game at any time by selecting "New Game" from the "Options" menu.
    - To quit the game, the player can select "Quit" from the "Options" menu.

Example Scenario:
    1. The computer generates a mystery line: [Red, Blue, Green, Yellow].
    2. The player starts with 10 attempts.
    3. The player makes a guess by clicking the buttons to select the colors, then clicks "Validate."
    4. Suppose the guess is [Red, Yellow, Blue, White]:
        - Feedback: [Green, Orange] (Green for the correct Red, Orange for the correct Blue in the wrong position).
    5. The player continues making guesses based on the feedback, aiming to match the mystery line within 10 attempts.

Good luck and enjoy the game!
"""

import tkinter as tk
from copy import deepcopy
from tkinter import messagebox
from random import choice

# Initialize the main window
root = tk.Tk()
root.title("Mastermind")

# Create frames for different parts of the game
mystery_frame = tk.Frame(root, bg="#B98D67", borderwidth=3)
game_frame = tk.Frame(root, bg="#B98D67", borderwidth=3)
validate_frame = tk.Frame(root, bg="#B98D67")

# Pack the frames into the main window
mystery_frame.pack()
game_frame.pack()
validate_frame.pack(fill=tk.BOTH)

# List of possible colors
color_cel = [
    "#FDDC36",  # Yellow
    "#6084E6",  # Blue
    "#FD3536",  # Red
    "#56D558",  # Green
    "#FDFDFF",  # White
    "#343636",  # Black
    "#8660AF",  # Purple
    "#FD89C4",  # Pink
]

# Configure grid layout for frames
mystery_frame.grid_rowconfigure(0, minsize=50)
for i in range(10):
    game_frame.grid_rowconfigure(i, minsize=50)
for i in range(9):
    game_frame.grid_columnconfigure(i, minsize=50)
    mystery_frame.grid_columnconfigure(i, minsize=50)

# Initialize lists to hold widgets
btn = []
lbl_check = []
mystery_label = []
following_turn = []


def colorchange(i, j):
    """
    Change the color of the button at position (i, j) in the grid.

    Cycles through the list of colors defined in color_cel.
    """
    actual_color = color_cel.index(btn[i][j].cget("bg"))
    if actual_color != 7:
        btn[i][j].config(bg=color_cel[actual_color + 1])
    else:
        btn[i][j].config(bg=color_cel[0])


def mystery_line() -> list:
    """
    Generate a random sequence of 4 colors for the mystery line.

    Returns:
        list: A list containing 4 randomly selected colors.
    """
    return [choice(color_cel) for _ in range(4)]


def attempt():
    """
    Validate the player's current guess.

    Checks the guess against the mystery line and provides feedback.
    """
    global mystery, turn
    print(turn)
    tempory_attempt = [btn[turn][i].cget("bg") for i in range(4)]
    orange_attempt = deepcopy(mystery)
    colorset = []

    # Check for correct colors in the correct positions
    for j in range(4):
        if tempory_attempt[j] == mystery[j]:
            colorset.append("green")
            orange_attempt.remove(tempory_attempt[j])
            print(orange_attempt)

    # Check for correct colors in the wrong positions
    for j in range(4):
        if tempory_attempt[j] in orange_attempt:
            colorset.append("orange")
            orange_attempt.remove(tempory_attempt[j])
        print(orange_attempt)

    # Disable current row and enable the next one
    for j in range(4):
        btn[turn][j].config(state=tk.DISABLED)
        following_turn[turn].config(text="")
        if turn != 0:
            btn[turn - 1][j].config(state=tk.NORMAL)
            following_turn[turn - 1].config(text="●", font=("Arial", 20), fg="red")

    # Sort and display feedback
    colorset.sort()
    for j in range(len(colorset)):
        lbl_check[turn][j].config(fg=colorset[j])

    # Check if the game has ended
    endgame()
    turn -= 1


def endgame():
    """
    Check if the game has ended, either by winning or exhausting all attempts.

    Displays the mystery line and a message box indicating the result.
    """
    checking_endgame = [btn[turn][i].cget("bg") for i in range(4)]
    if checking_endgame == mystery:
        show_mystery()
        messagebox.showinfo("Mastermind", "You win !!!")
        newgame()
    elif turn == 0:
        show_mystery()
        newgame()


def newgame():
    """
    Start a new game.

    Resets the game state and asks the player if they want to play again.
    """
    global mystery, turn, btn, lbl_check, mystery_label, following_turn
    answer = messagebox.askyesno("Game over", "Wanna play again ?")
    if answer:
        mystery = mystery_line()
        turn = 10
        btn = []
        lbl_check = []
        mystery_label = []
        following_turn = []
        initialisation_gui()


def show_mystery():
    """
    Display the mystery line at the top of the game window.
    """
    for i in range(4):
        mystery_label[i].config(bg=mystery[i], text="", relief=tk.SOLID)


def initialisation_gui():
    """
    Initialize the game interface.

    Creates the grid of buttons and labels for the game.
    """
    for i in range(10):
        row = []
        check_row = []
        label = tk.Label(game_frame, bg="#B98D67")
        label.grid(row=i, column=4, sticky=tk.NSEW)
        following_turn.append(label)
        for j in range(4):
            button = tk.Button(
                game_frame,
                bg="#FDFDFF",
                state=tk.DISABLED,
                command=lambda i=i, j=j: colorchange(i, j),
            )
            if i == 9:
                button.config(state=tk.NORMAL)
            button.grid(row=i, column=j, padx=2, pady=2, sticky=tk.NSEW)
            row.append(button)
            check_label = tk.Label(
                game_frame, font=("Arial", 20), text="●", fg="#624632", bg="#F5C590"
            )
            check_label.grid(row=i, column=5 + j, pady=2, sticky=tk.NSEW)
            check_row.append(check_label)
        btn.append(row)
        lbl_check.append(check_row)
    for i in range(4):
        m_label = tk.Label(
            mystery_frame,
            bg="#624632",
            fg="white",
            font=("Arial", 20),
            text="?",
            borderwidth=2,
            relief=tk.SOLID,
        )
        m_label.grid(row=0, column=i, sticky=tk.NSEW, padx=2, pady=2)
        mystery_label.append(m_label)
    following_turn[9].config(text="●", font=("Arial", 20), fg="red")


def rules():
    """
    Display the rules of the game in a new window.

    Creates a new window displaying the rules of the game.

    Returns:
        None
    """
    rules_window = tk.Toplevel(root, bg="#B98D67")
    rules_window.geometry("800x300")
    rules_window.title("Mastermind - Rules")
    rules_window.resizable(False, False)
    text_rules = tk.Text(
        rules_window, font=("Arial", 10, "bold"), bg="#624632", fg="white"
    )
    text_rules.insert(
        tk.INSERT,
        "The objective of Mastermind is to guess the secret color code created"
        "by the computer within a limited number of attempts.The computer randomly generates a sequence of 4 colors."
        "\n\n\nThe possible colors are represented by different colored buttons:"
        "Yellow, Blue, Red, Green, White, Black, Purple, and Pink. \n\n\n"
        "The player clicks on the buttons to change their colors and create a guess. \n"
        "Once the player has selected colors for all four positions in the current row, they click the Validate button."
        "\n\nThe computer then provides feedback on the guess \n"
        "\nThe player wins if they guess the correct sequence (all four colors in the correct positions)"
        "within the allowed attempts.",
    )
    text_rules.config(state=tk.DISABLED)
    text_rules.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


# Create and configure the validate button
valide_button = tk.Button(
    validate_frame,
    font=("Arial", 20),
    bg="#624632",
    fg="white",
    text="Validate",
    command=attempt,
)
valide_button.pack(padx=10, pady=15)

# Create and configure the menu bar
menubar = tk.Menu(root)  # Menu bar
root.config(menu=menubar)  # Configuring the root window with the menu
menu_option = tk.Menu(menubar, tearoff=False)  # Options dropdown menu
menubar.add_cascade(
    label="Options", menu=menu_option
)  # Adding the options dropdown to the menu bar

# Adding options to the dropdown menu
menu_option.add_command(label="New Game", command=newgame)
menu_option.add_separator()
menu_option.add_command(label="Rules", command=rules)
menu_option.add_separator()
menu_option.add_command(label="Quit", command=lambda: root.quit())

# Initialize the mystery line and starting turn
mystery = mystery_line()
turn = 9
initialisation_gui()

# Start the main loop
root.mainloop()
