import json

from utils import words_regex, min_len, subreddits

# Computes the results file again if needed

subreddit_dict = {}

checked_users = {"AutoModerator"}

def update_subreddits(user_subs, subreddit, user):
    if subreddit in user_subs and user_subs[subreddit] <= min_len:
        return
    for key in user_subs.keys():
        if key != subreddit:
            if user_subs[key] >= min_len:
                if key in subreddit_dict:
                    subreddit_dict[key].append(user)
                else:
                    subreddit_dict[key] = [user]


for sub in subreddits:
    subreddit_dict = {}
    filename = "data/" + sub + "_combine_comments.json"
    with open(filename, "r") as file:
        comments = json.load(file)
        current_author = ""
        user_subs = {}
        for comment in comments:
            if comment["author"] in checked_users:
                continue
            if current_author == "":
                current_author = comment["author"]
            if comment["author"] != current_author:
                checked_users.add(current_author)
                update_subreddits(user_subs, sub, current_author)
                user_subs = {}
                current_author = comment["author"]
            if not comment["subreddit"] in user_subs:
                user_subs[comment["subreddit"]] = len(words_regex.findall(comment["body"]))
            else:
                user_subs[comment["subreddit"]] += len(words_regex.findall(comment["body"]))
        checked_users.add(comment["author"])    
    with open("results/" + sub + "_results.json", "w+") as file:
        file.write(json.dumps(subreddit_dict, indent=4))
