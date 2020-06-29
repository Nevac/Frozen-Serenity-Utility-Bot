# Frozen-Serenity-Utility-Bot
For all the guild needs

## Setup
The user Python version is 3.7.3

### First install
```
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

### pip wrong version
```
python3 -m pip install --upgrade --force pip
```
### update all dependencies (dangerous)
```
sudo python3 -m pip install -U $(python3 -m pip freeze | cut -d '=' -f 1)
```