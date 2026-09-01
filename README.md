# Rock-Paper-Scissors (Sockets)

A lightweight client-server Rock-Paper-Scissors game built for a networking assignment. Features a multi-threaded Python server and a PHP terminal client communicating over TCP sockets.

Supports both single-player (against the computer) and 2-player matchmaking via a queue.

### Requirements

* Python 3.x
* PHP CLI with the `sockets` extension enabled

### How to Run?

1. **Start the server:**
```bash
python server.py

```


2. **Configure the IP:**
Update the IP in `client.php` to your server's IP (use `127.0.0.1` if testing locally).
3. **Start the client:**
```bash
php client.php

```


*(Run a second client in another terminal to test multiplayer mode).*

# !!! ENJOY THE GAME !!!
