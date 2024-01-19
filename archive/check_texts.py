import json
from praw import Reddit

reddit = Reddit("stylo_bot")

subreddit = "Jazz"

potential_subreddits = ["nba", "nfl", "movies", "politics", "books", "bayarea"]


with open("results/" + subreddit + "_results.json") as f:
    results = json.loads(f.read())
    
    for sub in potential_subreddits[:1]:
        users = results[sub]

        for user in users:
            print(user)
            redditor = reddit.redditor(user)
            text_main = ""
            text_second = ""
            for comment in redditor.comments.hot(limit=None):
                if comment.subreddit.display_name == subreddit:
                    text_main += "\n" + comment.body
                elif comment.subreddit.display_name == sub:
                    text_second += "\n" +  comment.body
            print("User " + redditor.name)
            print("Subreddit " + subreddit + " text: " + text_main)
            print("Subreddit " + sub + " text: " + text_second)
