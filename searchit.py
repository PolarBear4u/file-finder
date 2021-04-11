import json
import time

import finder

input_path = ""
output_path = ""
keywords = list()
settings = dict()

# ----------------- create settings file / load settings ------------------------
try:
    with open("settings.json", "r") as file:
        settings = json.load(file)
        input_path = settings["input"]
        output_path = settings["output"]
        keywords = settings["keywords"]
        print("input:", input_path)
        print("output:", output_path)
        print("keywords:", keywords)
        want_change_input = input("Do you want to change the input path (y/n): ")
        want_change_output = input("Do you want to change the output path (y/n): ")
        want_change_keywords = input("Do you want to change the keywords (y/n): ")
        if want_change_input == "y":
            input_path = input("Enter input path: ")
        if want_change_output == "y":
            output_path = input("Enter output path: ")     
        if want_change_keywords == "y":
            keywords = input("Enter your keywords: ").lower().split()

    with open("settings.json", "w") as file:
        settings["input"] = input_path
        settings["output"] = output_path
        settings["keywords"] = keywords
        json.dump(settings, file)  
        print("saved")

except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
    with open("settings.json", "w") as file:
        input_path = input("Enter input path: ")
        output_path = input("Enter output path: ")
        keywords = input("Enter keywords: ").lower().split()
        settings["input"] = input_path
        settings["output"] = output_path
        settings["keywords"] = keywords
        json.dump(settings, file)
        print("Saved")

# ---------------- search ----------------------------------------------------
print("starting finder")
finder.search(input_path, output_path, keywords, True, time.time())




