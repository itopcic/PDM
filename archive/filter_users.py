import json

new_results = {}

with open("user_results.json") as file:
    res = json.load(file)
    for key in res.keys():
        new_res = dict(filter(lambda pair: pair[1] >= 700, res[key].items()))
        if len(new_res) >= 3:
            new_results[key] = new_res

with open("new_user_results.json", "w+") as file:
    json.dump(new_results, file, indent=4)

print(len(new_results.keys()))
