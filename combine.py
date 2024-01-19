import json
import os

# Script to combine the Subreddit data from 2 different scraping sessions. I had to do it since I did not have enough RAM
# or enough storage to do it all in one go in the scrapper.

subreddits = [ "Jazz", "Dentistry", "Paleontology", "wrestling", "Horses", "PhD", "husky"]

for sub in subreddits:
    with open("/media/topcic/USB Data/data/" + sub + "_new_comments.json", "r") as file:
        all_comments = json.load(file)
    if os.path.exists("/media/topcic/USB/" + sub + "_new_comments.json"):
        with open("/media/topcic/USB/" + sub + "_new_comments.json", "r") as file:
            all_comments += json.load(file)
            ids = set(map(lambda c: c["id"], all_comments))
            final_comments = []
            for c in all_comments:
                if c["id"] in ids:
                    final_comments.append(c)
                    ids.remove(c["id"])
            with open("/media/topcic/USB Data/" + sub + "_combine_comments.json", "w+") as file:
                file.write(json.dumps(final_comments, indent=2))
