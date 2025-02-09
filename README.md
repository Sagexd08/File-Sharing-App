# File-Sharing-App

The File Sharing App is a robust and efficient application built using Python, designed to facilitate secure and seamless file transfers over a network. Utilizing a client-server architecture, this app ensures that files can be shared efficiently while maintaining data integrity and security. Whether you need to share files with peers or transfer data across devices, this application provides a reliable solution.

## Features

This application offers peer-to-peer file transfer, eliminating the need for intermediary servers and ensuring direct and fast data transmission. Security is a key focus, with encryption mechanisms integrated to safeguard file transfers and protect sensitive information. 

The application provides an intuitive user interface, which can be accessed via both a command-line interface (CLI) and a graphical user interface (GUI). It is designed to be compatible with multiple platforms, including Windows, Linux, and macOS, ensuring flexibility for various users. Additionally, the app supports resuming interrupted transfers, allowing users to continue downloads or uploads from where they left off without data loss. File compression capabilities are also integrated, significantly improving transmission speeds and reducing bandwidth consumption.

## Installation

To set up and use the File Sharing App, first, clone the repository from GitHub by running the following command:
   
```sh
   git clone https://github.com/yourusername/file-sharing-app.git
   cd file-sharing-app
```

Once inside the project directory, install the necessary dependencies using:
   
```sh
   pip install -r requirements.txt
```

These dependencies include libraries required for encryption, network communication, and interface functionality.

## Usage

### Running the Server
To start the server, execute the following command:
   
```sh
   python server.py
```

This will initiate the server, which will listen for incoming connections from clients. The server must be running before clients can connect and begin file transfers.

### Running the Client
To connect to a running server and initiate file transfers, use the command:
   
```sh
   python client.py --host <server-ip> --port <server-port>
```

Replace `<server-ip>` and `<server-port>` with the actual IP address and port number of the running server. The client interface will guide you through selecting files for transfer and managing the connection.

## Configuration

Users can customize server settings, encryption preferences, and transfer speed limits by modifying the `config.py` file. This allows for tailored optimization based on network conditions and security requirements. 

## Dependencies

The application requires Python 3.8 or higher. It also utilizes the Flask framework for web-based interfaces, socket programming for establishing connections, and cryptography modules to implement encryption. These components ensure smooth operation and secure file transfers.

## Contributing

Contributions to this project are highly encouraged. If you wish to improve the application, fix bugs, or add new features, feel free to submit issues or pull requests on the GitHub repository. All contributions will be reviewed and merged accordingly to enhance the overall functionality and usability of the application.

## License

This project is licensed under the MIT License. For more details, refer to the [LICENSE](LICENSE) file included in the repository.

