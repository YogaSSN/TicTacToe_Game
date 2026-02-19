import tkinter as tk
import math

HUMAN = "X"
AI = "O"
EMPTY = ""

board = [EMPTY] * 9




def check_winner(player):

    # Rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == player:
            return True

    # Columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] == player:
            return True

    # Diagonals
    if board[0] == board[4] == board[8] == player:
        return True

    if board[2] == board[4] == board[6] == player:
        return True

    return False


def is_full():
    return EMPTY not in board



def minimax(depth, alpha, beta, maximizing):

    if check_winner(AI):
        return 10 - depth
    if check_winner(HUMAN):
        return depth - 10
    if is_full():
        return 0

    if maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                eval = minimax(depth + 1, alpha, beta, False)
                board[i] = EMPTY
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                eval = minimax(depth + 1, alpha, beta, True)
                board[i] = EMPTY
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval


def best_move():
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(0, -math.inf, math.inf, False)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                move = i

    return move




def button_click(index):
    if board[index] == EMPTY and not game_over:
        board[index] = HUMAN
        buttons[index].config(text=HUMAN, fg="#00f5ff")

        if check_winner(HUMAN):
            end_game("You Win! 🎉")
            return

        if is_full():
            end_game("Draw!")
            return

        ai_turn()


def ai_turn():
    move = best_move()
    if move is not None:
        board[move] = AI
        buttons[move].config(text=AI, fg="#ff4c4c")

        if check_winner(AI):
            end_game("AI Wins! 🤖")
            return

        if is_full():
            end_game("Draw!")
            return


def end_game(message):
    global game_over
    game_over = True
    status_label.config(text=message)


def reset_game():
    global board, game_over
    board = [EMPTY] * 9
    game_over = False
    status_label.config(text="Your Turn")

    for btn in buttons:
        btn.config(text="")




root = tk.Tk()
root.title("Tic Tac Toe AI")
root.geometry("400x500")
root.config(bg="#1e1e2f")

game_over = False

frame = tk.Frame(root, bg="#1e1e2f")
frame.pack(pady=30)

buttons = []

for i in range(9):
    btn = tk.Button(
        frame,
        text="",
        font=("Arial", 28, "bold"),
        width=5,
        height=2,
        bg="#2e2e3f",
        fg="white",
        activebackground="#444",
        command=lambda i=i: button_click(i)
    )
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

status_label = tk.Label(
    root,
    text="Your Turn",
    font=("Arial", 16),
    bg="#1e1e2f",
    fg="white"
)
status_label.pack(pady=20)

reset_btn = tk.Button(
    root,
    text="Restart Game",
    font=("Arial", 14),
    command=reset_game,
    bg="#00bfff",
    fg="black"
)
reset_btn.pack()

root.mainloop()
