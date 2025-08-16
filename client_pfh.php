<?php
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

if (!socket_connect($socket, "192.168.1.44", 12345)) {
    echo "Unable to connect to server.\n";
    exit;
}

// Read welcome message and rules
while ($message = socket_read($socket, 1024)) {
    echo $message;

    if (strpos($message, "Choose game mode") !== false) {
        break;
    }
}

// Send game mode choice
$game_mode = trim(fgets(STDIN));
socket_write($socket, $game_mode . "\n", strlen($game_mode . "\n"));

if ($game_mode == "2") {
    // Single-player mode
    echo "Single-player mode selected.\n";
    while (true) {
        echo socket_read($socket, 1024);

        $choice = trim(fgets(STDIN));
        socket_write($socket, $choice . "\n", strlen($choice . "\n"));

        echo socket_read($socket, 1024); // Result
        echo socket_read($socket, 1024); // Play again prompt

        $play_again = trim(fgets(STDIN));
        socket_write($socket, $play_again . "\n", strlen($play_again . "\n"));

        if (strtolower($play_again) != "yes") {
            break;
        }
    }
} elseif ($game_mode == "1") {
    // Multiplayer mode
    echo "Multiplayer mode selected. Waiting for another player...\n";
    while (true) {
        echo socket_read($socket, 1024);

        $choice = trim(fgets(STDIN));
        socket_write($socket, $choice . "\n", strlen($choice . "\n"));

        echo socket_read($socket, 1024); // Result
        echo socket_read($socket, 1024); // Play again prompt

        $play_again = trim(fgets(STDIN));
        socket_write($socket, $play_again . "\n", strlen($play_again . "\n"));

        if (strtolower($play_again) != "yes") {
            break;
        }
    }
} else {
    echo "Invalid game mode selected. Disconnecting...\n";
}

socket_close($socket);
?>
