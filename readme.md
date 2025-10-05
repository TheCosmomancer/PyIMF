# Secure File & Messaging System

A client-server application for managing encrypted files and internal messaging with role-based access control.

## Features

- **User Authentication**: SHA-256 password hashing with role-based access (Agent/Secretary levels)
- **Encrypted File Storage**: Files encrypted using Fernet symmetric encryption
- **Messaging System**: Send direct messages or broadcast to all users
- **Access Control**: Files restricted by clearance level (1-3)
- **Spell-Check**: Levenshtein distance-based autocorrect for messages

## Architecture

- **Server** (`server.py`): Multi-threaded socket server handling client connections
- **Client** (`client.py`): Tkinter GUI for agents and secretaries
- **Database** (`classes.py`): Peewee ORM models for users, messages, and files
- **Setup** (`add‫‪Secretary‬‬.py`): Initial secretary account creation

## Requirements

- Python 3.x
- peewee
- cryptography
- Levenshtein
- nltk

## Usage

1. Run `add‫‪Secretary‬‬.py` to create the initial secretary account
2. Start `server.py` to launch the server
3. Run `client.py` to connect and log in

**Note:** Server is hardcoded to `127.0.0.2:5000`. Modify `SERVER` variable in both files if needed.

## User Roles

- **Secretary (Level 4)**: Full access - create/delete agents, manage all files, view all messages
- **Agent (Level 1-3)**: View files at or below clearance level, send/receive messages

---

*readme was written with AI.*