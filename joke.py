import os
import requests
import json

"""
Retrieve a random joke from public "dad joke" API.

User-agent header is set to contact email in order for API provider
to monitor use.

Return joke as a string

"""
def get_joke():
    headers = {'user-agent': 'contact@colinpeterson.ca', 'Accept': 'application/json'}
    r = requests.get('https://icanhazdadjoke.com/', headers=headers)
    return(r.json()['joke'])
    


