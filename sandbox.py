import json

with open("resources/heroes_2023-05-28_18-58.json", 'r') as f:
    ds = json.load(f)
    
print(ds["anti-mage"]['axe'])