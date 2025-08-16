import socket
import threading
import random
from queue import Queue

# Game options
OPTIONS = ["rock", "paper", "scissors"]

# Thread-safe queue for player matchmaking
player_queue = Queue()


def get_result(choice1, choice2):
    """Determines the result of the game."""
    if choice1 == choice2:
        return "It's a tie!"
    elif (choice1 == "rock" and choice2 == "scissors") or \
         (choice1 == "scissors" and choice2 == "paper") or \
         (choice1 == "paper" and choice2 == "rock"):
        return "Player 1 wins!"
    else:
        return "Player 2 wins!"


def handle_single_player(client_socket):
    """Handles single-player mode."""
    client_socket.sendall(b"You chose to play against the computer.\n")
    while True:
        # Ask for the player's choice
        client_socket.sendall(b"Choose Rock, Paper, or Scissors: ")
        player_choice = client_socket.recv(1024).decode().strip().lower()

        if not player_choice:
            client_socket.sendall(b"No input received. Disconnecting.\n")
            break

        if player_choice not in OPTIONS:
            client_socket.sendall(b"Invalid choice. Please try again.\n")
            continue

        # Generate computer's choice
        computer_choice = random.choice(OPTIONS)

        # Determine the result
        result = get_result(player_choice, computer_choice)
        result_message = f"You chose {player_choice}, the computer chose {computer_choice}. {result}\n"
        client_socket.sendall(result_message.encode())

        # Ask if the player wants to play again
        client_socket.sendall(b"Do you want to play again? (yes/no): ")
        play_again = client_socket.recv(1024).decode().strip().lower()

        if play_again != "yes":
            client_socket.sendall(b"Thank you for playing!\n")
            break

        # Loop back for another round


def handle_multiplayer():
    """Handles multiplayer mode."""
    while True:
        # Wait until two players are available
        player1 = player_queue.get()
        player2 = player_queue.get()

        try:
            player1.sendall(b"Another player has joined! Let the game begin.\n")
            player2.sendall(b"Another player has joined! Let the game begin.\n")

            while True:
                # Ask both players for their choices
                player1.sendall(b"Player 1: Choose Rock, Paper, or Scissors: ")
                choice1 = player1.recv(1024).decode().strip().lower()

                player2.sendall(b"Player 2: Choose Rock, Paper, or Scissors: ")
                choice2 = player2.recv(1024).decode().strip().lower()

                if choice1 not in OPTIONS or choice2 not in OPTIONS:
                    player1.sendall(b"Invalid choice. Please try again.\n")
                    player2.sendall(b"Invalid choice. Please try again.\n")
                    continue

                # Determine the result
                result = get_result(choice1, choice2)
                result_message = f"Player 1 chose {choice1}, Player 2 chose {choice2}. {result}\n"

                # Send results to both players
                player1.sendall(result_message.encode())
                player2.sendall(result_message.encode())

                # Ask both players if they want to play again
                player1.sendall(b"Do you want to play again? (yes/no): ")
                play_again1 = player1.recv(1024).decode().strip().lower()

                player2.sendall(b"Do you want to play again? (yes/no): ")
                play_again2 = player2.recv(1024).decode().strip().lower()

                if play_again1 != "yes" or play_again2 != "yes":
                    player1.sendall(b"Thank you for playing!\n")
                    player2.sendall(b"Thank you for playing!\n")
                    break

                # Loop back for another round
        finally:
            player1.close()
            player2.close()


def handle_client(client_socket, client_address):
    """Handles a single client connection."""
    print(f"New connection from {client_address}")

    # Send the welcome message and rules
    rules = (
        "Welcome to Rock, Paper, Scissors!\n\n"
        "Rules of the Game:\n"
        "1. The game can be played against another player or the computer.\n"
        "2. You will choose one of the following options:\n"
        "   - Rock\n"
        "   - Paper\n"
        "   - Scissors\n"
        "3. If both players make the same choice, it's a tie.\n\n"
        "Winning Conditions:\n"
        "- Rock beats Scissors (Rock crushes Scissors)\n"
        "- Scissors beats Paper (Scissors cut Paper)\n"
        "- Paper beats Rock (Paper wraps Rock)\n\n"
    )
    client_socket.sendall(rules.encode())

    # Ask for the game mode
    client_socket.sendall(b"Choose game mode:\n1. Play against another player\n2. Play against the computer\nEnter your choice (1 or 2): ")
    game_mode = client_socket.recv(1024).decode().strip()

    if game_mode == "1":
        # Add the player to the queue for multiplayer
        player_queue.put(client_socket)
    elif game_mode == "2":
        handle_single_player(client_socket)
    else:
        client_socket.sendall(b"Invalid game mode. Disconnecting.\n")
        client_socket.close()


def start_server():
    """Starts the server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)

    print("Server is running on 0.0.0.0:12345")

    # Start multiplayer handler thread
    threading.Thread(target=handle_multiplayer, daemon=True).start()

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    start_server()
