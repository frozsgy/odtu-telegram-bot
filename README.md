# ODTÜ Telegram Bot

This repository contains a tiny Telegram Bot that was developed to understand the Telegram Bot API, and Python web services. Currently under development.

## Installation

1. Get yourself a Bot account and a token at [Telegram Bots](https://core.telegram.org/bots).
2. Set up your environment and install dependencies.
3. Replace `YOUR-TELEGRAM-BOT-TOKEN` in the `init-tables.sql` file with your Telegram Bot Token.
4. Import `init-tables.sql` into your Postgres database.

## Usage

1. After installation, run `driver.py`
2. The bot should run smoothly.

## Command Line Arguments
* `--verbose` will make the bot verbose, and it will print many things on the terminal window.
* `--log` will activate the logging mode, which will log all messages to the database.

## Running as a Service
The following guide explains how to run the bot as a service on Raspberry Pi (Raspbian), but it is applicable to any other Linux system as well.
1. Create a file at `/lib/systemd/system/telegram.service` with the following content:
```
[Unit]
Description=Telegram Bot
Wants=network-online.target
After=network-online.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python3 /home/pi/telegram-bot/driver.py

[Install]
WantedBy=multi-user.target
```
Don't forget to change the line starting with `ExecStart` accordingly! The permissions of this file should be 644.

2. On a terminal window, enter the following commands;
```
sudo systemctl daemon-reload
sudo systemctl enable telegram.service
```
3. Reboot your system, and the bot should go live when the network connection is established.

## Dependencies

* Python 3
* Requests
* PostgreSQL

## Running via Docker

Simply use `docker-compose up`. 

## Bugs, Comments, Ideas?

Don't hesitate contacting me, or sending a pull request. They are always welcome.

Made in Ankara with 💙
