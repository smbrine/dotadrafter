import os
import json
from datetime import datetime, timedelta
from datasetsRefresher import refreshDatasets

def load_files_in_resources(folder_path):
    current_time = datetime.now()
    files_older_than_24h = []
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for file in os.listdir(folder_path):
        if file != ".DS_Store":
            file = str(file).replace('.json', '')
            date, time = file.split('_')[1:]
            file_datetime = datetime.strptime(f'{date}_{time}', '%Y-%m-%d_%H-%M')
            file_age = current_time - file_datetime

            if file_age < timedelta(hours=24):
                files_older_than_24h.append(file)

    return files_older_than_24h

folder_path = "./resources"
fresh_files = load_files_in_resources(folder_path)

if fresh_files:
    print("\nFound satisfying files. Importing...\n")
    for i, file in enumerate(fresh_files):
        if i == 0:
            with open(f'{folder_path}/{file}.json', "r", encoding="utf-8") as f:
                counter_dataset = json.load(f)
        else: 
            with open(f'{folder_path}/{file}.json', "r", encoding="utf-8") as f2:
                build_dataset = json.load(f2)
else:
    print("\nProgram could not find the required files. Refreshing datasets:")
    refreshDatasets()
    fresh_files = load_files_in_resources(folder_path)
    for i, file in enumerate(fresh_files):
        if i == 0:
            with open(f'{folder_path}/{file}.json', "r", encoding="utf-8") as f:
                counter_dataset = json.load(f)
        else: 
            with open(f'{folder_path}/{file}.json', "r", encoding="utf-8") as f2:
                build_dataset = json.load(f2)
    

while (user_input := input("Type in hero name: ")) != "exit":
    
    print()
    try:
        for i, counter in enumerate(counter_dataset[user_input].items()):
            name, value = counter
            if (i+1) <= 5:
                string = f"{name:20} has {float(value):.2f}% advantage over {user_input}"
                print(string)
                
            if (i+1) == (len(counter_dataset[user_input].items()) - 6): 
                print()
                
            if (i+1) >= (len(counter_dataset[user_input].items()) - 5):
                string = f"{user_input:20} has {float(value.replace('-', '')):.2f}% advantage over {name}"
                print(string)
    except:
        print(f"Unable to find {user_input}. Try again\n")
        continue
    try:
        start_items = build_dataset.get(user_input)["start"]
    except:
        print("\nInternal error. I know 'bout this if it's either razor or natures-prophet. Probably this character is low on pickrate at the moment.\n")
        continue
    print("\nStart buy:")
    for i, _ in enumerate(list(start_items.items())):
        item, val = list(start_items.items())[i]
        print(f"    {item:23} ({val.get('chance')}%)")
    
    main_build = build_dataset.get(user_input)["main"]
    print("\nMain build:")
    for i, _ in enumerate(list(main_build.items())):
        item, val = list(main_build.items())[i]
        print(f"    {item:20} ({val.get('chance')}%) before {val.get('timing'):2}min")
    print()
    
    
    
        