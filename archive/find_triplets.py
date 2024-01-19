import itertools
import json

popular_subreddits = {"AskReddit", "AmItheAsshole", "NoStupidQuestions", "ask", "WhitePeopleTwitter", "unpopularopinion", "todayilearned", "explainlikeimfive", "facepalm", 
                      "pics", "PublicFreakout", "Damnthatsinteresting", "videos", "interestingasfuck", "mildlyinfuriating",
                      "memes", "TooAfraidToAsk", "changemyview", "CrazyFuckingVideos", "nextfuckinglevel", "AITAH", "Advice", "therewasanattempt",
                      "TrueUnpopularOpinion", "BestofRedditorUpdates", "AskWomenOver30", "LifeProTips", "offmychest", "TrueOffMyChest"}

bad_pairs =  list(map(list, itertools.combinations(['Saxophonics', 'Jazz', 'saxophone', 'Vinyl_Jazz', 'Jazz'], 2)))
bad_pairs += list(map(list, itertools.combinations(['AskAcademia', 'academia', 'Professors', 'AskProfessors', 'GradSchool', 'college', "PhD", 'labrats'], 2)))
bad_pairs += list(map(list, itertools.combinations(['nyc', 'newyorkcity', 'AskNYC'], 2)))
bad_pairs += list(map(list, itertools.combinations(['britishproblems', 'CasualUK', 'AskUK'], 2)))
bad_pairs += list(map(list, itertools.combinations(['judo', 'martialarts', 'bjj', 'wrestling', 'ufc', 'mma', 'mmamemes'], 2)))
bad_pairs += list(map(list, itertools.combinations(['webdev', 'learnjavascript', 'learnprogramming'], 2)))
bad_pairs += list(map(list, itertools.combinations(['BabyBumps', 'pregnant', 'beyondthebump'], 2)))
bad_pairs += list(map(list, itertools.combinations(['DentalSchool', 'Dentistry', 'askdentists'], 2)))
bad_pairs += list(map(list, itertools.combinations(['Dogtraining', 'DogAdvice', 'reactivedogs', 'dog', 'dogs'], 2)))
bad_pairs += list(map(list, itertools.combinations(['doordash_drivers', 'UberEATS', 'doordash'], 2)))
bad_pairs += list(map(list, itertools.combinations(['Naturewasmetal', 'Paleontology', 'Dinosaurs', 'JurassicPark'], 2)))
bad_pairs += list(map(list, itertools.combinations(['Aquariums', 'bettafish', 'PlantedTank'], 2)))
bad_pairs += list(map(list, itertools.combinations(["Equestrian", "Horses", "homestead"], 2)))
bad_pairs += list(map(list, itertools.combinations(["WWE", "Wrasslin"], 2)))
bad_pairs += list(map(list, itertools.combinations(['adhdwomen', 'ADHD'], 2)))
bad_pairs += list(map(list, itertools.combinations(['worldnews', 'news'], 2)))
bad_pairs += list(map(list, itertools.combinations(['dating_advice', 'dating'], 2)))
bad_pairs += list(map(list, itertools.combinations(['relationships', 'relationship_advice'], 2)))

triplets_dict = {}

def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)

def filter_bad_pairs(triplet): 
    for pair in bad_pairs:
        if sublist(pair, triplet):
            return False
    return True

with open("new_user_results.json") as file:
    res = json.load(file)
    keys = list(res.keys())
    for i in range(len(keys)):
        print("{:.0f}%".format(i/len(keys) * 100), end="\r")
        key = keys[i]
        subs = set(filter(lambda sub: not sub in popular_subreddits, res[key].keys()))
        triplets = itertools.combinations(subs, 3)
        for triplet in triplets:
            if triplet in triplets_dict:
                triplets_dict[triplet].append(key)
            else:
                triplets_dict[triplet] = [key]
    triplets_dict = dict(filter(lambda pair: len(pair[1]) >= 10 and filter_bad_pairs(pair[0]), triplets_dict.items()))

with open("triplets_results.json", "w+") as file:
    mapped_triplets = dict(map(lambda pair: [str(pair[0]), pair[1]], triplets_dict.items()))
    json.dump(mapped_triplets, file, indent=4)
