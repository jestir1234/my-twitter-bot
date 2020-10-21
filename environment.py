import os

oauth_keys = []

with open('keys.env') as f:
    for line in f:
        if line.startswith('#'):
            continue
        oauth_keys.append(line.split())

