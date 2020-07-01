# Frozen-Serenity-Utility-Bot
For all the guild needs

## Setup
The user Python version is 3.7.3

### Install MongoDB
```
sudo apt install mongodb
sudo systemctl enable mongodb
sudo systemctl start mongodb
```

### Setup project
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip freeze
```

### pip wrong version
```
python3 -m pip install --upgrade --force pip
```

### Update all dependencies (dangerous)
```
sudo python3 -m pip install -U $(python3 -m pip freeze | cut -d '=' -f 1)
```

## Run bot
```
python3 app.py
```
