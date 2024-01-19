import json
import os
import praw
import time

from praw.models import MoreComments, Subreddit, Redditor
from utils import words_regex, subreddits, min_len

# Scrapes the given Subreddit with the help of PRAW

# Setup values
reddit = praw.Reddit("stylo_bot")

checked_users = {"AutoModerator"}

spin='-\|/'

spin_pos = 0

# Function used to go through all the post and comments in one Subreddit as far back as Reddit lets us
def scrape_subreddit(subreddit):
    results = {}
    all_comments = []
    # Load the old result file if it exists
    if os.path.isfile("results/" + subreddit + "_comments.json") and os.path.getsize("results/" + subreddit + "_comments.json") > 0:
        with open("results/" + subreddit + "_results.json") as file:
            results = json.load(file)
    # Loads already scrapped data if it exists
    if os.path.isfile("data/" + subreddit + "_comments.json") and os.path.getsize("data/" + subreddit + "_comments.json") > 0:
        with open("data/" + subreddit + "_comments.json") as file:
            all_comments = json.load(file)
    checked_users = {"AutoModerator"}
    if not isinstance(subreddit, Subreddit):
        subreddit: Subreddit = reddit.subreddit(subreddit)
    print("Checking subreddit: " + subreddit.display_name)
    posts = subreddit.hot(limit=None)
    start = time.time()
    # For all posts in the Subreddit
    for post in posts:
        redditor = post.author
        comments = post.comments.list()
        # If the Redditor is not deleted and if we have not checked him
        if redditor is not None and not redditor.name in checked_users:
            # We scrape everything we can for that particular user
            results, all_comments, checked_users = scrape_redditor(redditor, subreddit, results, all_comments, checked_users)
        for comment in comments:
            if isinstance(comment, MoreComments):
                # Won't handle this case for now
                continue
            else:
                redditor = comment.author
                # If the Redditor is not deleted and if we have not checked him
                if redditor is None or redditor.name in checked_users:
                    continue
                # We scrape everything we can for that particular user
                results, all_comments, checked_users = scrape_redditor(redditor, subreddit, results, all_comments, checked_users)
    # Write the results to file but first remove duplicates
    for key in results.keys():
        results[key] = list(set(results[key]))
    for sub in results:
        if len(results[sub]) >= 12:
            print("Candidate " + sub + " " + str(len(results[sub])) + " redditors")
    with open("results/" + subreddit.display_name + "_results.json", "w+") as file:
        file.write(json.dumps(results, indent=4))
    # Remove duplicate comments
    ids = set(map(lambda c: c["id"], all_comments))
    final_comments = []
    for c in all_comments:
        if c["id"] in ids:
            final_comments.append(c)
            ids.remove(c["id"])
    print("Scrapped " + str(len(final_comments)) + " comments")
    with open("data/" + subreddit.display_name + "_new_comments.json", "w+") as file:
        file.write(json.dumps(final_comments, indent=4))
    print("Took " + str(time.time() - start) + " s total for subreddit " + subreddit.display_name)

# Function used to go through all the post and comments from one Redditor as far back as Reddit lets us
def scrape_redditor(redditor, subreddit, results, all_comments, checked_users):
    global spin_pos
    print(spin[spin_pos], end="\r")
    spin_pos = (spin_pos + 1) % 4
    if not isinstance(redditor, Redditor):
        checked_users.add(redditor)
        redditor = reddit.redditor(redditor)
    else:
        checked_users.add(redditor.name)
    # Get all the comments and posts from that user
    comments = redditor.comments.hot(limit=None)
    submissions = redditor.submissions.hot(limit=None)
    subreddit_dict = {}
    try:
        # Go through all the comments from the Redditor
        for comment in comments:
            if isinstance(comment, MoreComments):
                    # Won't handle this case for now
                    continue
            elif comment.subreddit.display_name in subreddit_dict:
                subreddit_dict[comment.subreddit.display_name] += len(words_regex.findall(comment.body))
            else:
                subreddit_dict[comment.subreddit.display_name] = len(words_regex.findall(comment.body))
            # We put a size limit on the number of comments we want in total to have enough storage
            if len(all_comments) <= 100000000:
                all_comments.append({"author" : comment.author.name, "body" : comment.body, "id" : comment.id,
                                    "link_id" : comment.link_id, "parent_id" : comment.parent_id, 
                                    "subreddit" : comment.subreddit.display_name, "created_utc" : comment.created_utc})
        # Go through all the posts from the redditor
        for submission in submissions:
            if submission.subreddit.display_name in subreddit_dict:
                subreddit_dict[submission.subreddit.display_name] += len(words_regex.findall(submission.selftext))
            else:
                subreddit_dict[submission.subreddit.display_name] = len(words_regex.findall(submission.selftext))
    except:
        return results, all_comments, checked_users
    # If the users has the minimum length of texts, add him to the result file
    if subreddit.display_name in subreddit_dict and subreddit_dict[subreddit.display_name] >= min_len:
        for sub in subreddit_dict:
            if not sub == subreddit.display_name:
                if subreddit_dict[sub] >= min_len:
                    if sub in results and not redditor.name in results[sub]:
                        results[sub].append(redditor.name)
                    else:
                        results[sub] = [redditor.name]
    return results, all_comments, checked_users

if __name__ == "__main__":
    for sub in subreddits:
        scrape_subreddit(sub)
