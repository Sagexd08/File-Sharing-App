# File-Sharing-App

A simple and efficient file-sharing application built with Python. This app allows users to securely transfer files over a network using a client-server architecture.

Features

Peer-to-peer file transfer

Secure file sharing using encryption

Intuitive user interface (CLI/GUI)

Multi-platform support (Windows, Linux, macOS)

Resume interrupted transfers

File compression for faster transmission

Installation

Clone the repository:

git clone https://github.com/yourusername/file-sharing-app.git
cd file-sharing-app

Install dependencies:

pip install -r requirements.txt

Usage

Running the Server

python server.py

The server will start listening for incoming connections.

Running the Client

python client.py --host <server-ip> --port <server-port>

Follow the prompts to select and send files.

Configuration

Modify config.py to customize the server settings, encryption options, and transfer speed limits.

Dependencies

Python 3.8+

Flask (if using a web interface)

Socket programming

Cryptography module (for encryption)

Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

License

This project is licensed under the MIT License - see the LICENSE file for details.
