import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

plt.rcParams["figure.figsize"] = (15.5, 8)
base_folder = "SuperStyl/"
folder_names = ["", "_reverse", "_confusion"]
output_folder = "/home/topcic/Documents/pdm_report/images/"
model_names = ["all-MiniLM-L6-v2"]#"all-distilroberta-v1", "all-MiniLM-L6-v2"]

from utils import pairs

def get_accuracy_data(pair):
    data = []
    for sub in pair:
        data.append(round(pd.read_csv(base_folder + sub + "/" + "output.csv", index_col=0).iloc[-3][2], 2))
    for name in folder_names:
        data.append(round(pd.read_csv(base_folder + "_".join(pair) + name + "/" + "output.csv", index_col=0).iloc[-3][2], 2))
    return data

def get_accuracy_plot():
    x = np.arange(5)  # the label locations
    width = 0.15  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')
    
    measurements = np.array([get_accuracy_data(pair) for pair in pairs]).T
    labels = ["First Subreddit", "Second Subreddit", "Trained on first", "Trained on second", "Topic Confusion"]
    for i in range(len(measurements)):
        measurement = measurements[i]
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=labels[i])
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy')
    ax.set_xticks(x + 0.3, list(map(lambda p: "_".join(p), pairs)))
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 1)
    plt.savefig(output_folder + "everything.png", bbox_inches='tight')
    plt.show()

def get_similarity_plot():
    accuracy = []
    similarity = []
    for pair in pairs:
        for sub in pair:
            df = pd.read_csv(base_folder + sub + "/" + "output.csv", index_col=0)
            users = df.index.values
            accuracy += list(df["f1-score"].to_list()[:-3])
            curr_temp = []
            for model in model_names:
                temp = []
                with open("similarity/" + "_".join(pair) + "/" + sub + "_" + model + ".json") as file:
                    sim_dict = json.load(file)
                    for user in users:
                        if user in sim_dict:
                            temp.append(sim_dict[user])
                        else:
                            for key in sim_dict.keys():
                                if key.startswith(user):
                                    temp.append(sim_dict[key])
                                    break
                if len(curr_temp) == 0:
                    curr_temp = temp
                else:
                    curr_temp = [curr_temp[i] + temp[i] for i in range(len(curr_temp))]
            curr_temp = list(map(lambda n: n / len(model_names), curr_temp))
            similarity += curr_temp
            
    plt.plot(similarity, accuracy, 'o')

    model = sm.OLS(accuracy, sm.add_constant(similarity))
    results = model.fit()
    b, m = results.params
    # plot y = m*x + b
    plt.xlabel('Similarity')
    plt.ylabel('Accuracy')
    plt.axline(xy1=(0, b), slope=m, label=f'$y = {m:.1f}x {b:+.1f}$', color="black")
    print(results.summary())
    plt.savefig(output_folder + "acc_vs_sim_sub.png", bbox_inches='tight')
    plt.show()
    
def get_inter_similarity_plot():
    accuracy = []
    similarity = []
    for pair in pairs:
        sim_first = 0
        sim_sec = 0
        for model in model_names:
            with open("similarity/" + "_".join(pair) + "/" + pair[0] + "_" + model + ".json") as file:
                values = json.load(file).values()
                sim_first += sum(list(values)) / len(values)
            with open("similarity/" + "_".join(pair) + "/" + pair[1] + "_" + model + ".json") as file:
                values = json.load(file).values()
                sim_sec += sum(list(values)) / len(values)
        sim_intra = ((sim_first / len(model_names)) + (sim_sec / len(model_names))) / 2
        acc_first = pd.read_csv(base_folder + pair[0] + "/" + "output.csv", index_col=0)["f1-score"].to_list()[-3]
        acc_sec = pd.read_csv(base_folder + pair[1] + "/" + "output.csv", index_col=0)["f1-score"].to_list()[-3]
        df = pd.read_csv(base_folder + "_".join(pair) + "/" + "output.csv", index_col=0)
        accuracy += [acc_first - df["f1-score"].to_list()[-3]]
        df = pd.read_csv(base_folder + "_".join(pair) + "_reverse" + "/" + "output.csv", index_col=0)
        users = df.index.values
        accuracy += [acc_sec - df["f1-score"].to_list()[-3]]
        for model in model_names:
            with open("similarity/" + "_".join(pair) + "/" + "_".join(pair) + "_" + model + ".json") as file:
                sim_dict = json.load(file)
                temp = []
                for user in users:
                    if user in sim_dict:
                        temp.append(sim_dict[user])
                    else:
                        for key in sim_dict.keys():
                            if key.startswith(user):
                                temp.append(sim_dict[key])
                                break
        similarity += [sim_intra - (sum(temp) / len(temp))]
        for model in model_names:
            with open("similarity/" + "_".join(pair) + "/" + "_".join(pair[::-1]) + "_" + model + ".json") as file:
                sim_dict = json.load(file)
                temp = []
                for user in users:
                    if user in sim_dict:
                        temp.append(sim_dict[user])
                    else:
                        for key in sim_dict.keys():
                            if key.startswith(user):
                                temp.append(sim_dict[key])
                                break
        similarity += [sim_intra - (sum(temp) / len(temp))]
            
            
    plt.plot(similarity, accuracy, 'o')

    model = sm.OLS(accuracy, sm.add_constant(similarity))
    results = model.fit()
    b, m = results.params
    # plot y = m*x + b
    plt.xlabel('Drop in similarity')
    plt.ylabel('Drop in accuracy')
    plt.axline(xy1=(0, b), slope=m, label=f'$y = {m:.1f}x {b:+.1f}$', color="black")
    print(results.summary())
    plt.savefig(output_folder + "acc_vs_sim_pairs.png", bbox_inches='tight')
    plt.show()
    
def get_inter_similarity_plot_per_user():
    accuracy = []
    similarity = []
    for pair in pairs:
        df = pd.read_csv(base_folder + "_".join(pair) + "/" + "output.csv", index_col=0)
        users = df.index.values
        accuracy += list(df["f1-score"].to_list()[:-3])
        curr_temp = []
        temp = []
        for model in model_names:
            with open("similarity/" + "_".join(pair) + "/" + "_".join(pair) + "_" + model + ".json") as file:
                sim_dict = json.load(file)
                for user in users:
                    if user in sim_dict:
                        temp.append(sim_dict[user])
                    else:
                        for key in sim_dict.keys():
                            if key.startswith(user):
                                temp.append(sim_dict[key])
                                break
            if len(curr_temp) == 0:
                curr_temp = temp
            else:
                curr_temp = [curr_temp[i] + temp[i] for i in range(len(curr_temp))]
        curr_temp = list(map(lambda n: n / len(model_names), curr_temp))
        similarity += curr_temp
            
    plt.plot(similarity, accuracy, 'o')

    model = sm.OLS(accuracy, sm.add_constant(similarity))
    results = model.fit()
    b, m = results.params
    # plot y = m*x + b
    plt.xlabel('Similarity')
    plt.ylabel('Accuracy')
    plt.axline(xy1=(0, b), slope=m, label=f'$y = {m:.1f}x {b:+.1f}$', color="black")
    print(results.summary())
    plt.savefig(output_folder + "acc_vs_sim_users.png", bbox_inches='tight')
    plt.show()

def get_inter_similarity_plot_per_user():
    accuracy = []
    similarity = []
    for pair in pairs:
        df = pd.read_csv(base_folder + "_".join(pair) + "/" + "output.csv", index_col=0)
        users = df.index.values
        accuracy += list(df["f1-score"].to_list()[:-3])
        curr_temp = []
        for model in model_names:
            temp = []
            with open("similarity/" + "_".join(pair) + "/" + "_".join(pair) + "_" + model + ".json") as file:
                sim_dict = json.load(file)
                for user in users:
                    if user in sim_dict:
                        temp.append(sim_dict[user])
                    else:
                        for key in sim_dict.keys():
                            if key.startswith(user):
                                temp.append(sim_dict[key])
                                break
            if len(curr_temp) == 0:
                curr_temp = temp
            else:
                curr_temp = [curr_temp[i] + temp[i] for i in range(len(curr_temp))]
        curr_temp = list(map(lambda n: n / len(model_names), curr_temp))
        similarity += curr_temp
            
    plt.plot(similarity, accuracy, 'o')

    model = sm.OLS(accuracy, sm.add_constant(similarity))
    results = model.fit()
    b, m = results.params
    # plot y = m*x + b
    plt.xlabel('Similarity')
    plt.ylabel('Accuracy')
    plt.axline(xy1=(0, b), slope=m, label=f'$y = {m:.1f}x {b:+.1f}$', color="black")
    print(results.summary())
    plt.savefig(output_folder + "acc_vs_sim_users.png", bbox_inches='tight')
    plt.show()

get_inter_similarity_plot_per_user()
get_inter_similarity_plot()   
get_similarity_plot()
get_accuracy_plot()
