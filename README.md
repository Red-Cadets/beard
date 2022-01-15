# Beard - Attack/Defense CTF scoreboard parser

<p align="center">
<a href=""><img src="https://img.shields.io/badge/supports-Docker-blue" /></a>
<a href=""><img src="https://img.shields.io/badge/license-MIT-red" /></a>
<a href = "https://t.me/redcadets_chat"><img src="https://img.shields.io/badge/chat-telegram-blue?logo=telegram" /></a>

<p align="center">
    Language: <b>English</b> | <a href="https://link/to/ru/README.md">Русский</a>
</p>

<b>Beard - a comfortable way to track progress of your team during A/D competitions</b>
    <br />
    <a href="https://link/to/wikis/home"><strong>Explore the docs »</strong></a>
    <br />
</p>  


## Important Links

<table>
    <thead>
        <tr>
            <th>Links</th>
            <th></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=1><a href="https://link/to/-/wikis/Installation"><b>📖Installation Guide</b></a></td>
            <td rowspan=6><img src="https://i.ibb.co/FDvzZYJ/image.png"></td>
        </tr>
        <tr>
            <td rowspan=1><a href="https://link/to/-/wikis/home"><b>🌐Wiki</b></a></td>
        </tr>
        <tr>
            <td rowspan=1><a href="https://link/to/-/releases"><b>🚀Releases</b></a></td>
        </tr>
        <tr>
            <td rowspan=1><a href="https://t.me/redcadets_chat"><b>💬Telegram</b></a></td>
        </tr>
    </tbody>
</table>

# ✨ Features

* TODO

## 🛠 Supported scoreboards

| **A/D framework**  | Link | Status | Description
| ------------------ | ---- | ------ | -----------
| ForcAD | https://github.com/pomo-mondreganto/ForcAD | ✅ | 
| HackerDom checksystem | https://github.com/HackerDom/checksystem | ✅ | parsing old-style view at /board
## 🙋 Table of Contents
* 📖 [Fast Installation Guide](link/to/repo)
    * 🐋 [Docker Usage](https://link/to/repo#whale-docker)
* 🦜 [Telegram](https://t.me/redcadets_chat)
* 🖼️ [Gallery](https://link/to/repo#-gallery)
* 🎪 [Community](https://link/to/repo#-community)
* 📝 [TODO](https://link/to/repo#-todo)


# 📖 Fast Installation Guide

## Docker

Clone repository
```bash
git clone https://link/to/repo.git
```
Go to folder:
```bash
cd beard
```
Change .env with your settings:
- `HOST` - IP address or domain on which the application will be deployed. This parameter is required to configure CORS. Example: `http://8.8.8.8 ` or `http://example.com `
- `SCOREBOARD` - Scoreboard location. Example: `http://6.0.0.1/board`
- `TEAM` - Team name or team IP to display information about. Example: `Red Cadets` or `10.10.1.15`
- `TYPE` - Scoreboard type. Example: `forcad` or `hackerdom`
- `BOT_URL` - Telegram bot api address (webhook) for notification. For easy bot integration, use [courier](https://github.com/Red-Cadets/courier). Message format:
```json
{
    "message": "Notification here",
    "type": "markdown",
    "id": "parser",
    "to": "tg chat id here"
}
```

- `ROUND_TIME` - Round time in seconds. For example: `120`
- `EXTEND_ROUND` - The number of rounds to predict future graph. The prediction is based on the points of the last 5 rounds. For example: `10`
- `MONGO_USER` - DB username. Например: `parser`
- `MONGO_PASS` - DB password. Например: `parser`
Run docker-compose:
```bash
docker-compose up -d
```
and go to URL
```bash
http://127.0.0.1:65005/
```


## 🖼️ Gallery


||
|:-------------------------:|
|![Главная страница](https://i.ibb.co/SQrxpVD/Scores.png)|
|Graph of scores of all teams on the scoreboard|
|![Главная страница](https://i.ibb.co/Sc7vBzs/Echarts-lost.png)
|Flag loss graph|
|![Главная страница](https://i.ibb.co/JCQD2g6/Echarts-got.png)|
|Graph of receiving flags|

# 🎪 Community

If you have any feature suggestions or bugs, leave a Github issue.
Open to pull requests and other forms of collaboration!

We communicate over Telegram. [Click here](https://t.me/redcadets_chat) to join our Telegram community!


## 📝 TODO

* TODO

# ❤️ Thanks to

Hackerdom parser is based on https://github.com/Vindori/hackerdom-board-parser