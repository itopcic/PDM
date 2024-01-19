import json
import praw
import time
from utils import words_regex

from praw.models import MoreComments, Subreddit, Redditor

reddit = praw.Reddit("stylo_bot")

checked_users = {"AutoModerator"}

def scrape_subreddit(subreddit):
    results = {}
    all_comments = []
    checked_users = {"AutoModerator"}
    if not isinstance(subreddit, Subreddit):
        subreddit = reddit.subreddit(subreddit)
    print("Checking subreddit: " + subreddit.display_name)
    posts = subreddit.hot(limit=None)
    start = time.time()
    for post in posts:
        redditor = post.author
        comments = post.comments.list()
        if redditor is not None and not redditor.name in checked_users:
            print("checking: " + redditor.name)
            results, all_comments, checked_users = scrape_redditor(redditor, subreddit, results, all_comments, checked_users)
        for comment in comments:
            if isinstance(comment, MoreComments):
                # Won't handle this case for now
                continue
            else:
                redditor = comment.author
                if redditor is None or redditor.name in checked_users:
                    continue
                print("checking: " + redditor.name)
                results, all_comments, checked_users = scrape_redditor(redditor, subreddit, results, all_comments, checked_users)
        print("Checked " + str(len(checked_users)) + " users in subreddit " + subreddit.display_name)
        print("Elapsed time: " + str(time.time() - start) + " s")
    for sub in results:
        if len(results[sub]) >= 12:
            print("Candidate " + sub + " " + str(len(results[sub])) + " redditors")
    with open("results/" + subreddit.display_name + "_results_second.json", "w+") as file:
        file.write(json.dumps(results, indent=4))
    print("Scrapped " + str(len(all_comments)) + " comments")
    with open("data/" + subreddit.display_name + "_comments_second.json", "w+") as file:
        file.write(json.dumps(all_comments, indent=4))
    print("Scrapped at a speed of " + str(len(all_comments) / (time.time() - start) * 60) + " comments per minute")
    print("Scrapped at a speed of " + str(len(checked_users) / (time.time() - start) * 60) + " users per minute")

def scrape_redditor(redditor, subreddit, results, all_comments, checked_users):
    #start = time.time()
    if not isinstance(redditor, Redditor):
        checked_users.add(redditor)
        redditor = reddit.redditor(redditor)
    else:
        checked_users.add(redditor.name)
    comments = redditor.comments.hot(limit=None)
    submissions = redditor.submissions.hot(limit=None)
    subreddit_dict = {}
    #print("init " + str(time.time() - start) + " s")
    #start = time.time()
    try:
        for comment in comments:
            if isinstance(comment, MoreComments):
                    # Won't handle this case for now
                    continue
            elif comment.subreddit.display_name in subreddit_dict:
                subreddit_dict[comment.subreddit.display_name] += len(words_regex.findall(comment.body))
            else:
                subreddit_dict[comment.subreddit.display_name] = len(words_regex.findall(comment.body))
            if len(all_comments) <= 20000000:
                all_comments.append({"author" : comment.author.name, "body" : comment.body, "id" : comment.id,
                                    "link_id" : comment.link_id, "parent_id" : comment.parent_id, 
                                    "subreddit" : comment.subreddit.display_name, "created_utc" : comment.created_utc})
        #print("comments " + str(time.time() - start) + " s")
        #start = time.time()
        for submission in submissions:
            if submission.subreddit.display_name in subreddit_dict:
                subreddit_dict[submission.subreddit.display_name] += len(words_regex.findall(submission.selftext))
            else:
                subreddit_dict[submission.subreddit.display_name] = len(words_regex.findall(submission.selftext))
        #print("submission: " + str(time.time() - start) + " s")
        #start = time.time()
    except:
        return results, all_comments, checked_users
    if subreddit.display_name in subreddit_dict and subreddit_dict[subreddit.display_name] >= 500:
        for sub in subreddit_dict:
            if not sub == subreddit.display_name:
                if subreddit_dict[sub] >= 500:
                    if sub in results and not redditor.name in results[sub]:
                        results[sub].append(redditor.name)
                    else:
                        results[sub] = [redditor.name]
    return results, all_comments, checked_users
    #print("test: " + str(time.time() - start) + " s")
    #start = time.time()

if __name__ == "__main__":
    subreddits_to_check = ["Dentistry"]#, "vscode", "wrestling", "facebook", "Money", "Horses", "PhD"]
    for sub in subreddits_to_check:
        scrape_subreddit(sub)
