import json
import os

from utils import *

# Generates texts of the same length for all users by splitting and merging all the texts from a user
# Care is taken to avoid having one text being split into two texts. This is to avoid having one part
# of the text being used in training data and one part in testing which would influence the results as
# we would be using training data as testing data

needed_texts = int(min_len / texts_len) # Number of texts needed per user

# Function which splits the texts
def get_text_for_svm(main_sub, other_sub):
    subs = [main_sub, other_sub]
    dir_name = main_sub + "_" + other_sub

    try: 
        os.mkdir("pairs/" + dir_name)
    except FileExistsError:
        print("Dir already exists")

    users_comments = None

    user_texts = {}

    # Load all the texts
    with open("user_data/" + main_sub + "_" + other_sub + ".json") as file:
        users_comments = json.load(file)

    for sub in subs:
        for user in users_comments.keys():
            print("checking user " + user)
            # Remove urls
            texts = list(map(lambda s: url_regex.sub("", s), users_comments[user][sub]))
            # Extract texts which are already over the minimum length
            len_n_texts = set(filter(lambda s: len(words_regex.findall(s)) >= texts_len, texts))
            nb_texts = len(len_n_texts)
            # If there are enough texts over the min length we are done with this user
            if nb_texts >= needed_texts:
                user_texts[user] = list(map(lambda s: words_regex.findall(s)[:texts_len], len_n_texts))[:needed_texts]
                continue
            # If not, we continue if there is enough data
            enough = needed_texts - nb_texts
            not_used_texts = list(set(texts) - len_n_texts)
            all_combined = " ".join(not_used_texts)
            tokenized = words_regex.findall(all_combined)
            if len(tokenized) < texts_len * enough:
                continue
            if nb_texts >= 2:
                user_texts[user] = list(map(lambda s: words_regex.findall(s)[:texts_len], len_n_texts))
                all_combined = " ".join(not_used_texts)
                for i in range(int(len(tokenized) / texts_len)):
                    if len(user_texts[user]) >= needed_texts:
                        continue
                    user_texts[user] += [tokenized[i*texts_len:(i+1)*texts_len]]
                    
            # Combine texts to be as close as possible to the min length. As this is an NP problem, we start with one text
            # and add until we get as close as possible. We do not check if it is the optimal solution
            
            # List of tuples of the texts and its length useful in the generating phase
            texts_and_lengths = list(map(lambda t: [t, len(words_regex.findall(t))], not_used_texts))
            copy_t_and_l = texts_and_lengths.copy()
            
            found_combinations = [] # List of lists of texts to combine
            curr_combination = [0] # Current combination we are generating
            smallest_over = 1000000 # Smallest length just over the min length
            biggest_under = 0 # Biggest length just under the min length
            curr_under = 0 # Current value in the loop
            curr_over = 0 # Current value in the loop
            next_i = 0 # Text to use as a start next
            # We search as long as we do not have enough texts and as long as there is enough data to create the texts
            while len(found_combinations) < enough and sum(map(lambda p: p[1], copy_t_and_l)) >= texts_len:
                if smallest_over < 1000000:
                    curr_combination = [next_i]
                    smallest_over = 1000000
                    biggest_under = 0
                    curr_under = 0
                    curr_over = 0
                s = sum(map(lambda i: texts_and_lengths[i][1], curr_combination)) # Current length of the merged texts
                # Go through all the remaining texts
                for i in range(len(texts_and_lengths)):
                    # Do not continue if the texts is already used, already in another combination or is the one we started with
                    if i in curr_combination or any(map(lambda l: i in l, found_combinations)) or i == next_i:
                        continue
                    # Here we compute the smallest over and the biggest under
                    p = texts_and_lengths[i]
                    length = s + p[1]
                    if length >= texts_len:
                        if length < smallest_over:
                            curr_over = i
                            smallest_over = length
                    else:
                        if length > biggest_under:
                            curr_under = i
                            biggest_under = length
                # If we have a length over the min length we add the current combination to the list of found combinations and start over with the next one
                if smallest_over < 1000000:
                    curr_combination += [curr_over]
                    found_combinations += [curr_combination]
                # If we have not found a combination that is over the min length we add the closest to the min length to the combination and restart
                else:
                    curr_combination += [curr_under]
                # Remove used texts from the text we check next
                copy_t_and_l = [p for p in copy_t_and_l if not p in list(map(lambda i: texts_and_lengths[i], curr_combination))]
                # The next start is the first remaining text if there is one, else we leave the loop
                if len(copy_t_and_l) > 0:
                    next_i = texts_and_lengths.index(copy_t_and_l[0])
                else:
                    break
                
            # If we have found enough texts with the method above, we recombine the texts and add them to the user dict of texts
            if len(found_combinations) == enough:
                res = list(map(lambda s: words_regex.findall(s)[:texts_len], len_n_texts))
                for comb in found_combinations:
                    s = ""
                    for i in comb:
                        s += texts_and_lengths[i][0] + " "
                    res += [words_regex.findall(s)[:texts_len]]
                user_texts[user] = res[:needed_texts]
                
        # Write the results to file
        with open("pairs/" + dir_name + "/" + sub + ".json", "w+") as f:
            json.dump(user_texts, f, indent=4)

if __name__ == "__main__":
    for pair in pairs:
        get_text_for_svm(*pair)
