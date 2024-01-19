import os
import json

from sentence_similarity import sentence_similarity
from utils import pairs

model_name = "all-distilroberta-v1"

similarity_dir = "similarity/"

def compare_sentences(sentence_1=str, sentence_2=str, model_name=str, embedding_type="cls_token_embedding", metric="cosine") -> str:
    """Utilizes an NLP model that calculates the similarity between 
    two sentences or phrases."""

    model = sentence_similarity(model_name=model_name, embedding_type=embedding_type)
    score = model.get_score(sentence_1, sentence_2, metric=metric)
    return(f"{score}")

def compare_data(first_data, second_data):
    results = {}
    for key in first_data.keys():
        temp = []
        for i in range(len(first_data[key])):
            first = first_data[key][i]
            if key in second_data:
                for j in range(len(second_data[key])):
                    sec = second_data[key][j]
                    if first != sec:
                        temp.append(float(compare_sentences(sentence_1=" ".join(first), sentence_2=" ".join(sec), model_name=model_name)))
        if key in second_data:
            results[key] = sum(temp) / len(temp)
    return results

def similarity(pair):
    dir = "pairs/" + "_".join(pair) + "/"
    with open(dir + pair[0] + ".json", "r") as file:
        first_sub = json.load(file)

    with open(dir + pair[1] + ".json", "r") as file:
        sec_sub = json.load(file)
    
    print("Comparing Subreddits " + " and ".join(pair))
    #results_inter = compare_data(first_sub, sec_sub)
    print("Comparing Subreddits " + " and ".join(pair[::-1]))
    results_inter_rev = compare_data(sec_sub, first_sub)
    print("Comparing Subreddit " + pair[0])
    #results_intra_first = compare_data(first_sub, first_sub)
    print("Comparing Subreddit " + pair[1])   
    #results_intra_sec = compare_data(sec_sub, sec_sub)
    
    if not os.path.isdir(similarity_dir):
        os.mkdir(similarity_dir)
    
    pair_dir = "_".join(pair) + "/"
    pair_dir_rev = "_".join(pair[::-1]) + "/"
        
    if not os.path.isdir(similarity_dir + pair_dir):
        os.mkdir(similarity_dir + pair_dir)
    """
    with open(similarity_dir + pair_dir + pair_dir[:-1] + "_" + model_name + ".json", "w") as file:
        json.dump(results_inter, file)
        """
    with open(similarity_dir + pair_dir + pair_dir_rev[:-1] + "_" + model_name + ".json", "w") as file:
        json.dump(results_inter_rev, file)
        
    """with open(similarity_dir + pair_dir + pair[0] + "_" + model_name + ".json", "w") as file:
        json.dump(results_intra_first, file)"""
        
    """with open(similarity_dir + pair_dir + pair[1] + "_" + model_name + ".json", "w") as file:
        json.dump(results_intra_sec, file)"""

if __name__ == "__main__":
    for pair in pairs:
        similarity(pair)
