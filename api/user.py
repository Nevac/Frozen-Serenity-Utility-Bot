import requests

API = 'https://discord.com/api'


def getUser(id):
    response = requests.get(API + '/users/' + id)
    user = response.json()