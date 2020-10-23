<!-- @format -->

# PyBot

Python application for serving a discord bot.

## Development

Clone and change into repo directory.

```bash
git clone https://github.com/collinkleest/PyBot.git
cd PyBot/
```

Setup virtual environment for isolated development.

```bash
pip install virutalenv
# or
pip3 install virualenv
```

Create a virual environmnmet

```bash
python -m venv venv
# or
python3 -m venv venv
```

Activate the virual environment on unix (linux / macos)

```bash
./venv/bin/activate
# or
soruce venv/bin/activate
```

Activate the virtual environmnet on windows.

Inside CMD

```bash
.\venv\bin\activate
```

Inside Powershell

```bash
.\venv\bin\activate.ps1
```

Install all dependencies in `requirements.txt` file.

```bash
pip install -r requirements.txt
#or
pip3 install -r requirements.txt
```

## Environment

These environement variables need to passed into the application in order for it to run properly.

```
DISCORD_TOKEN=<discord bot token>
DISCORD_GUILD=<discord server/guild name>
FFMPEG_PATH=<path to ffmpeg binary>
```
