import json

from utils import words_regex, subreddits

users = {}

checked_users = {"AutoModerator"}

for sub in subreddits:
    filename = "data/" + sub + "_combine_comments.json"
    with open(filename, "r") as file:
        comments = json.load(file)
        current_author = ""
        user_subs = {}
        for comment in comments:
            if comment["author"] in checked_users:
                current_author = comment["author"]
                continue
            if current_author == "":
                current_author = comment["author"]
            if comment["author"] != current_author:
                checked_users.add(current_author)
                users[current_author] = user_subs
                user_subs = {}
                current_author = comment["author"]
            if not comment["subreddit"] in user_subs:
                user_subs[comment["subreddit"]] = len(words_regex.findall(comment["body"]))
            else:
                user_subs[comment["subreddit"]] += len(words_regex.findall(comment["body"]))
        users[current_author] = user_subs
        checked_users.add(current_author)    

with open("user_results.json", "w+") as file:
    file.write(json.dumps(users, indent=4))
