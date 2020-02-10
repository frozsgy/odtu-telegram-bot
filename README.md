# ODTÜ Telegram Bot

This repository contains a tiny Telegram Bot that was developed to understand the Telegram Bot API, and Python web services. Currently under development.

## Installation

1. Get yourself a Bot account and a token at [Telegram Bots](https://core.telegram.org/bots)
2. Enter your token to `secrets-template.py` and rename it as `secrets.py`
3. Set up your environment and install dependencies
4. Enter your full location of your bot to `locations.py`. You may use `pwd` to find your working directory.

## Usage

1. After installation, run `driver.py`
2. The bot should run smoothly.

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
ExecStart=/usr/bin/python3 /home/pi/telegram-bot/driver.py

[Install]
WantedBy=multi-user.target
```
Don't forget to change the folder and file locations accordingly! The permissions should be 644.
2. Enter the following commands;
```
sudo systemctl daemon-reload
sudo systemctl enable telegram.service
```
3. Reboot your system, and the bot should go live when the network connection is established.

## Dependencies

* Python 3
* Requests

## Bugs, Comments, Ideas?

Don't hesitate contacting me, or sending a pull request. They are always welcome.
