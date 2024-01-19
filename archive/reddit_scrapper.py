import praw
import time

from praw.models import MoreComments
from utils import words_regex


reddit = praw.Reddit("stylo_bot")

subreddit_pair = ["sleep", "eurovision"]

checked_users = {"AutoModerator"}

possible_users = []

sure_users = []

def check_subreddits(subreddit_pair):
    subreddits = [reddit.subreddit(subreddit_pair[0]), reddit.subreddit(subreddit_pair[1])]
    smaller_subreddit = None
    if subreddits[0].subscribers < subreddits[1].subscribers:
        smaller_subreddit = subreddits[0]
    else:
        smaller_subreddit = subreddits[1]
    start = time.time()
    for post in smaller_subreddit.hot(limit=None):
        redditor = post.author
        comments = post.comments.list()
        if redditor is not None:
            check_redditor(redditor, subreddits)
        for comment in comments:
            if isinstance(comment, MoreComments):
                # Won't handle this case for now
                continue
            else:
                redditor = comment.author
                if redditor is None or redditor in checked_users:
                    continue
                print("checking: " + redditor.name)
                check_redditor(redditor, subreddits)
        print("Checked " + str(len(checked_users)) + " users")
        print("Elapsed time: " + str(time.time() - start) + " s")
    print("Possible users: " + str(possible_users))
    print("Sure user: " + str(sure_users))


def check_redditor(redditor, subreddits):
    checked_users.add(redditor.name)
    comments = redditor.comments.new()
    submissions = redditor.submissions.new()
    subreddit_dict = {subreddits[0] : 0, subreddits[1] : 0}
    words_dict = {subreddits[0] : 0, subreddits[1] : 0}
    print(comments)
    try:
        for comment in comments:
            if isinstance(comment, MoreComments):
                # Won't handle this case for now
                continue
            if comment.subreddit in subreddits:
                subreddit_dict[comment.subreddit] += 1
                words_dict[comment.subreddit] += len(words_regex.findall(comment.body))
        for submission in submissions:
            if submission.subreddit in subreddits:
                words_dict[submission.subreddit] += len(words_regex.findall(submission.body))
        print(comments)
        return
    except:
        return
    if all(subreddit_dict.values()):
        print("Found potential user: " + str(redditor.name))
        print("Subreddit " + subreddit_pair[0] + " " + str(words_dict[subreddits[0]]) + "\nSubreddit "+ subreddit_pair[1] + ": " + str(words_dict[subreddits[1]]))
        if words_dict[subreddits[0]] >= 500 and words_dict[subreddits[1]] >= 500:
            print("SHOULD WORK!")
            sure_users.append(redditor.name)
            with open("sure_users.txt", "a") as file:
                file.write(redditor.name + " " + str(words_dict[subreddits[0]]) + " " + str(words_dict[subreddits[1]]) + "\n")
        elif words_dict[subreddits[0]] >= 200 and words_dict[subreddits[1]] >= 200:
            print("Might work")
            possible_users.append(redditor.name)
            with open("possible_users.txt", "a") as file:
                file.write(redditor.name + " " + str(words_dict[subreddits[0]]) + " " + str(words_dict[subreddits[1]]) + "\n")


if __name__ == "__main__":
    check_subreddits(subreddit_pair)
