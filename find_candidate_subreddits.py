import json

# Goes through the scrapped data and checks for other Subreddits which have enough data for possibly be a pair of Subreddits
# We filter the most popular Subreddits which have not a clearly defined topic.

subreddits = ["husky", "Jazz", "Dentistry", "wrestling", "Horses", "PhD"]

popular_subreddits = ["AskReddit", "AmItheAsshole", "NoStupidQuestions", "ask", "unpopularopinion", "todayilearned", "explainlikeimfive", 
                      "pics", "PublicFreakout", "Damnthatsinteresting", "videos", "interestingasfuck", "mildlyinfuriating", "facepalm", "TrueOffMyChest",
                      "memes", "TooAfraidToAsk", "changemyview", "CrazyFuckingVideos", "nextfuckinglevel", "AITAH", "Advice", "therewasanattempt",
                      "AskMen", "TrueUnpopularOpinion", "BestofRedditorUpdates", "AskWomenOver30", "LifeProTips"]

def sub_filter(pair):
    return pair[0] not in popular_subreddits and len(pair[1]) >= 6

for sub in subreddits:
    with open("results/" + sub + "_results.json") as f:
        results = json.loads(f.read())

    filtered = filter(sub_filter, results.items())
    print(sub + " = " + str(list(dict(filtered).keys())) + "\n")
