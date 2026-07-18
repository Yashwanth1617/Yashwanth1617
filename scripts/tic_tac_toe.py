import sys
import os
import random

# File paths
BOARD_FILE = "data/board.txt"
README_FILE = "README.md"

def load_board():
    if os.path.exists(BOARD_FILE):
        with open(BOARD_FILE, "r") as f:
            board = f.read().strip()
            if len(board) == 9:
                return list(board)
    return list("---------")

def save_board(board):
    os.makedirs("data", exist_ok=True)
    with open(BOARD_FILE, "w") as f:
        f.write("".join(board))

def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
        [0, 4, 8], [2, 4, 6]             # diagonals
    ]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

def bot_move(board):
    empty = [i for i, v in enumerate(board) if v == "-"]
    if empty:
        # Simple random move
        move = random.choice(empty)
        board[move] = "O"
    return board

def generate_html(board, status_msg):
    cells = []
    for i in range(9):
        if board[i] == "X":
            cells.append("❌")
        elif board[i] == "O":
            cells.append("⭕")
        else:
            if "won" in status_msg.lower() or "draw" in status_msg.lower():
                cells.append("⬜") # game over, no link
            else:
                cells.append(f'<a href="https://github.com/Yashwanth1617/Yashwanth1617/issues/new?title=ttt%7Cmove%7C{i}&body=Just+click+Submit+new+issue!"><kbd>⬜</kbd></a>')
    
    # We use <kbd> or just raw emoji. Let's use raw emoji to make it large.
    # Wait, raw emoji inside <h2> makes it large enough.
    for i in range(9):
        if "<a href" not in cells[i]:
            cells[i] = f"<h2>{cells[i]}</h2>"
        else:
            cells[i] = cells[i].replace("<kbd>⬜</kbd>", "<h2>⬜</h2>")

    html = f"""<!-- TTT_BOARD_START -->
<div align="center">
  <h3>🎮 Interactive Tic-Tac-Toe</h3>
  <p><b>{status_msg}</b></p>
  <table border="1" bordercolor="#444444" cellspacing="0" cellpadding="0">
    <tr>
      <td align="center" width="80" height="80">{cells[0]}</td>
      <td align="center" width="80" height="80">{cells[1]}</td>
      <td align="center" width="80" height="80">{cells[2]}</td>
    </tr>
    <tr>
      <td align="center" width="80" height="80">{cells[3]}</td>
      <td align="center" width="80" height="80">{cells[4]}</td>
      <td align="center" width="80" height="80">{cells[5]}</td>
    </tr>
    <tr>
      <td align="center" width="80" height="80">{cells[6]}</td>
      <td align="center" width="80" height="80">{cells[7]}</td>
      <td align="center" width="80" height="80">{cells[8]}</td>
    </tr>
  </table>
  <br/>
  <p><i>Click a white square to make a move! (You are ❌)</i></p>
  <a href="https://github.com/Yashwanth1617/Yashwanth1617/issues/new?title=ttt%7Creset&body=Just+click+Submit+new+issue!">🔄 Reset Game</a>
</div>
<!-- TTT_BOARD_END -->"""
    return html

def update_readme(html):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    start_marker = "<!-- TTT_BOARD_START -->"
    end_marker = "<!-- TTT_BOARD_END -->"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx] + html + content[end_idx + len(end_marker):]
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)

def main():
    if len(sys.argv) < 2:
        print("No issue title provided.")
        return
        
    issue_title = sys.argv[1]
    
    if not issue_title.startswith("ttt|"):
        print("Not a tic-tac-toe move.")
        return
        
    board = load_board()
    status_msg = "Your turn! (❌)"
    
    if issue_title == "ttt|reset":
        board = list("---------")
        status_msg = "Game reset! Your turn (❌)"
    elif issue_title.startswith("ttt|move|"):
        try:
            pos = int(issue_title.split("|")[2])
            if 0 <= pos <= 8 and board[pos] == "-":
                board[pos] = "X"
                
                if check_win(board, "X"):
                    status_msg = "🎉 You won! Click Reset to play again."
                elif "-" not in board:
                    status_msg = "🤝 It's a draw! Click Reset to play again."
                else:
                    # Bot move
                    board = bot_move(board)
                    if check_win(board, "O"):
                        status_msg = "🤖 Bot won! Click Reset to play again."
                    elif "-" not in board:
                        status_msg = "🤝 It's a draw! Click Reset to play again."
                    else:
                        status_msg = "Bot moved. Your turn! (❌)"
        except ValueError:
            pass

    save_board(board)
    html = generate_html(board, status_msg)
    update_readme(html)

if __name__ == "__main__":
    main()
