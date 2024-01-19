import json
from utils import pairs

# From the scrapped data, generates a file containing all the users texts in both Subreddits if the users has the
# minimum length of texts in both Subreddits. The algorithm is simple, we go use the result file
# generated during scraping to check if the user has enough text and add all the comments we find in the data file.

def get_user_comments(main_sub, other_sub):

    subs = [main_sub, other_sub]

    users = []
    users_comments = {}

    with open("results/" + main_sub + "_results.json") as file:
        subreddits = json.load(file)
        users = subreddits[other_sub]

    with open("data/" + main_sub + "_combine_comments.json") as file:
        comments = json.load(file)
        for comment in comments:
            user = comment["author"]
            sub = comment["subreddit"]
            if user in users and sub in subs:
                if user in users_comments.keys():
                    users_comments[user][sub].append(comment["body"])
                else:
                    if sub == other_sub:
                        users_comments[user] = {sub: [comment["body"]], main_sub: []}
                    else:
                        users_comments[user] = {sub: [comment["body"]], other_sub: []}

        with open("user_data/" + main_sub + "_" + other_sub + ".json", "w+") as file:
            json.dump(users_comments, file, indent=4)           

if __name__ == "__main__":
    for pair in pairs:
        get_user_comments(*pair)