import requests
from bs4 import BeautifulSoup as BS
from time import perf_counter_ns
import random
from datetime import datetime

dt = datetime.now()
d_t = dt.strftime('%Y-%m-%d_%H-%M')
heroes_file = f"./resources/heroes_{d_t}.json"
builds_file = f"./resources/builds_{d_t}.json"

def tostr(s, encoding="ascii", errors="strict"):
    if not isinstance(s, str):
        return s.decode(encoding, errors)
    else:
        return s

def strjoin(iterable, joiner=""):
    return tostr(joiner).join(iterable)

def _reverseString(s):
	s = list(s)
	s.reverse()
	return strjoin(s)

def handle_dagon(titles):
    alphabet1 = _reverseString('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    alphabet2 = _reverseString('abcdefghijklmnopqrstuvwxyz')
    letters1 = list(alphabet1)
    letters2 = list(alphabet2)
    new_titles = []
    for title in titles:
        if title == "Dagon":
            new_titles.append(f"Dagon_{letters1[random.randint(0, (len(letters1)-1))]}{letters2[random.randint(0, (len(letters2)-1))]}_")
        else:
            new_titles.append(title)
    return new_titles

def refreshDatasets():
    hero_names_url = 'https://www.dotabuff.com/heroes'
    hero_names_response = requests.get(hero_names_url, headers={'User-agent': 'your bot 0.1'})
    hero_names_html_content = hero_names_response.text
    hero_names_soup = BS(hero_names_html_content, 'html.parser')
    table_rows = hero_names_soup.find_all("a", {"href": True})
    hero_names = [row["href"].replace("/heroes/", "") for i, row in enumerate(table_rows) if 49 < i < 174]

    heroes_data = {}
    with open(heroes_file, "w", encoding="utf-8") as f:
        f.write('{')
    with open(builds_file, 'w', encoding="utf-8") as f:
        f.write('{')

    time_spent = []

    for h, hero_nam in enumerate(hero_names):
        
        start_time = perf_counter_ns()
        
        counter_url = f'https://www.dotabuff.com/heroes/{hero_nam}/counters'
        counter_responce = requests.get(counter_url, headers = {'User-agent': 'your bot 0.1'})
        counter_html_content = counter_responce.text

        counter_soup = BS(counter_html_content, 'html.parser')
        hero_data = {}

        table_rows = counter_soup.find_all("tr", {"data-link-to": True})

        for row in table_rows:
            hero_name = row["data-link-to"].replace("/heroes/", "")
            required_number = row.find_all("td", {"data-value": True})[1]["data-value"]
            hero_data[hero_name] = required_number
        
        if (h+1) != len(hero_names):
            hero_data = '"' + str(hero_nam) + '"' + ": " + str(hero_data).replace("'", '"') + "," + "\n"
        else:
            hero_data = '"' + str(hero_nam) + '"' + ": " + str(hero_data).replace("'", '"') + "\n"
        
        with open(heroes_file, "a") as outfile:
            outfile.write(hero_data)
            
        different_names = {"anti-mage": "Anti-Mage", "keeper-of-the-light": "Keeper%20of%20the%20Light", "natures-prophet": "Nature's%20Prophet"}
        
        if hero_nam not in different_names.keys():
            parts = hero_nam.split("-")
            capitalized_parts = [part[0].upper() + part[1:] for part in parts]
            hero_nam_req = "%20".join(capitalized_parts)
        else:
            hero_nam_req = different_names.get(hero_nam)
        
        build_url = f'https://www.dota2protracker.com/hero/{hero_nam_req}#'
        build_responce = requests.get(build_url, headers = {'User-agent': 'your bot 0.1'})
        build_html_content = build_responce.text

        build_soup = BS(build_html_content, 'html.parser')
        
        div = build_soup.find('div', class_='content-box-body items-body')

        # Find the second "inner-box" div
        try:
            inner_box1 = div.find_all('div', {"class": False})[0].find_all("div", class_="inner-box")[0]
            inner_box2 = div.find_all('div', class_='inner-box')[1]
        except:
            continue

        # Extract the "item-group" divs
        item_groups1 = inner_box1.find_all('div', class_='inner-item-small')
        item_groups2 = inner_box2.find_all('div', class_='item-group')

        hero_bld_data_st = "{"
        hero_bld_data_mn = "{"
        
        for i, item_group in enumerate(item_groups1):
            # Find the "item-row-bottom" divs
            item_row_bottoms = item_group.find_all('div', class_='item-row-bottom')

            # Extract the values from the "item-row-bottom" divs
            values = item_group.text.replace(" ", '').replace("\n", '')
            
            # Find the "item-row-top" divs
            item_row_tops = item_group.find_all('div', class_='item-row-top')
            
            # Extract the "title" attributes from the "item-row-top" divs
            titles = [row['title'] for row in item_row_tops]

            if "x" in values:
                pt1, pt2 = values.split('x')
                amount = int(pt1)
                chance = int(pt2.replace('%', ''))
            else:
                amount = 1
                chance = int(values.replace('%', ''))
            
            if (i+1) < len(item_groups1):
                hero_bld_data_st = hero_bld_data_st + f'"{amount}x {titles[0].replace("item_", "")}": '+ "{" + f'"chance": {chance}' + '}, '
            else:
                hero_bld_data_st = hero_bld_data_st + f'"{amount}x {titles[0].replace("item_", "")}": '+ "{" + f'"chance": {chance}' + '}'
        hero_bld_data_st = hero_bld_data_st + '}'
        
        for i, item_group in enumerate(item_groups2):
            # Find the "item-row-bottom" divs
            item_row_bottoms = item_group.find_all('div', class_='item-row-bottom')

            # Extract the values from the "item-row-bottom" divs
            values = item_group.text.replace(" ", '').replace("\n", '')
            
            # Find the "item-row-top" divs
            item_row_tops = item_group.find_all('div', class_='item-row-top')
            
            # Extract the "title" attributes from the "item-row-top" divs
            titles = [row['title'] for row in item_row_tops]
            titles = handle_dagon(titles)
            
            if "or" in values:
                for y, value in enumerate(values.split("or")):
                    pt1, pt2 = value.split("m")
                    if "x" in value:
                        pt1, pt2 = value.split('x')
                        amount = int(pt1)
                        chance = int(pt2.replace('%', ''))
                    else:
                        amount = 1
                        chance = int(pt2.replace('%', ''))
                    if pt1[0] == "-":
                        if pt1[3] != "-":
                            pt1, pt2 = pt1[1:].split('-')
                        else:
                            pt1, pt2 = pt1[1], pt1[4]
                    else: 
                        pt1, pt2 = pt1.split('-')
                    timing = pt2
                    
                    if (y+1) < len(item_groups2):
                        hero_bld_data_mn = hero_bld_data_mn + f'"{titles[y].replace("item_", "")}{y+1}": ' + '{' + f'"chance": {chance}, "timing": {timing}'+ '}, '
                    else:
                        hero_bld_data_mn = hero_bld_data_mn + f'"{titles[y].replace("item_", "")}{y+1}": ' + '{' + f'"chance": {chance}, "timing": {timing}'+ '}'
            else:
                if "x" in values:
                    pt1, pt2 = values.split('x')
                    amount = int(pt1)
                    chance = int(pt2.replace('%', ''))
                else:
                    if "m" in values:
                        pt1, pt2 = values.split("m")
                        amount = 1
                        chance = int(pt2.replace('%', ''))
                        if pt1[0] == "-":
                            if pt1[3] != "-":
                                pt1, pt2 = pt1[1:].split('-')
                            else:
                                pt1, pt2 = pt1[1], pt1[4]
                        else: 
                            pt1, pt2 = pt1.split('-')
                        timing = pt2
                    else:
                        amount = 1
                        chance = int(values.replace('%', ''))
                
                if (i+1) < len(item_groups2):
                    hero_bld_data_mn = hero_bld_data_mn + f'"{titles[0]}": ' + '{' + f'"chance": {chance}, "timing": {timing}' + "}, "
                else:
                    hero_bld_data_mn = hero_bld_data_mn + f'"{titles[0]}": ' + '{' + f'"chance": {chance}, "timing": {timing}' + "}"
        
        checker = hero_bld_data_mn[len(hero_bld_data_mn)-2:]
        if checker == ", ":
            hero_bld_data_mn = hero_bld_data_mn[:-2]
        hero_bld_data_mn = hero_bld_data_mn + '}'
        
        if (h+1) < len(hero_names):
            hero_data = '"' + str(hero_nam) + '"' + ": {" + '"' + "start" + '"' + f': {hero_bld_data_st}, "main": {hero_bld_data_mn}' + "},\n"
        else:
            hero_data = '"' + str(hero_nam) + '"' + ": {" + '"' + "start" + '"' + f': {hero_bld_data_st}, "main": {hero_bld_data_mn}' + "}\n"
        
        with open(builds_file, "a") as outfile:
            outfile.write(hero_data)
        
        end_time = perf_counter_ns()
        time_spent.append((end_time-start_time))
        avg_time = sum(time_spent) / len(time_spent)
        est_her = len(hero_names) - h - 1
        outc_ms = int(round(((avg_time * est_her) / 1_000_000), 0))
        
        spaces = 20 - len(hero_nam)
        hero_nam = (' ' * int(spaces / 2)) + hero_nam + (' ' * int(spaces / 2))
        print(f"{h+1:3}/{len(hero_names)} | {hero_nam:20}| Took {(end_time-start_time)/1_000_000:6.0f}ms | Approx. time remaining: {outc_ms/1_000:6.2f}s | {100 / len(hero_names) * (h+1):5.2f}% done", end="\r")
    print((" "*100))
    print(f"\r\rSuccessfuly refreshed database. Took {sum(time_spent)/1_000_000_000:.2f}s. Average hero time was {(sum(time_spent) / len(time_spent))/1_000_000_000:.2f}s.") 

    with open(heroes_file, "a", encoding="utf-8") as f:
        f.write('}')
    with open(builds_file, "a", encoding="utf-8") as f:
        f.write('}')

    print()