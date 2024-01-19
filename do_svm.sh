#!/bin/bash

function extract_features() {
    local folder=$1
    # Generate word unigrams
    python ../main.py -s ../../texts/$folder/normal/* -t words -n 1 -x txt --absolute_freqs;
    mv feats_tests_n1_k_5000.csv feats_tests_n1_words_k_5000.csv;
    # Generate word bigrams
    python ../main.py -s ../../texts/$folder/normal/* -t words -n 2 -x txt --absolute_freqs;
    mv feats_tests_n2_k_5000.csv feats_tests_n2_words_k_5000.csv;
    # Generate word trigrams
    python ../main.py -s ../../texts/$folder/normal/* -t words -n 3 -x txt --absolute_freqs;
    mv feats_tests_n3_k_5000.csv feats_tests_n3_words_k_5000.csv;

    # Add POS 
    python ../main.py -s ../../texts/$folder/POS/* -t words -n 1 -x txt --absolute_freqs;
    mv feats_tests_n1_k_5000.csv feats_tests_n1_pos_k_5000.csv;

    # Add Lemmatization removed since it does not change the results
    #python ../main.py -s ../../texts/$folder/Lemma/* -t words -n 1 -x txt --absolute_freqs;
    #mv feats_tests_n1_k_5000.csv feats_tests_n1_lemma_k_5000.csv;

    # Generate ngrams
    python ../main.py -s ../../texts/$folder/normal/* -t chars -n 1 -x txt --absolute_freqs;
    python ../main.py -s ../../texts/$folder/normal/* -t chars -n 2 -x txt --absolute_freqs;
    python ../main.py -s ../../texts/$folder/normal/* -t chars -n 3 -x txt --absolute_freqs;
    python ../main.py -s ../../texts/$folder/normal/* -t chars -n 4 -x txt --absolute_freqs;
    python ../main.py -s ../../texts/$folder/normal/* -t chars -n 5 -x txt --absolute_freqs;

    # Remove features which appear less than 3 times
    for n in 1 2 3 4 5
    do
        python ../../drop_columns.py feats_tests_n${n}_k_5000.csv feature_list_chars${n}grams5000mf.json
    done

    # Merge everything
    python ../merge_datasets.csv.py -o merged.csv feats_tests_n*;

    # Split train/test
    python ../split.py -s ../../texts/$folder/split.json merged.csv;
}

function do_svm() {
    local folder=$1
    local double=$2

    # If folder exists remove the folder
    if [ -d $folder ]; then
        rm -rf $folder;
    fi

    # Create folder for the results and move there
    mkdir $folder;
    cd $folder;
    
    extract_features $folder;

    # Do the SVM
    python ../train_svm.py merged_train.csv --test_path merged_valid.csv;

    # If we have 2 Subreddits as inputs, we need to do it in reverse and with the topic confusion
    if [ $double -gt 0 ]; then
        if [ -d ../${folder}_reverse ]; then
            rm -rf ../${folder}_reverse;
        fi
        mkdir ../${folder}_reverse
        cd ../${folder}_reverse
        python ../train_svm.py ../$folder/merged_valid.csv --test_path ../$folder/merged_train.csv;
        if [ -d ../${folder}_confusion ]; then
            rm -rf ../${folder}_confusion;
        fi
        mkdir ../${folder}_confusion
        cd ../${folder}_confusion
        python ../split.py -s ../../texts/${folder}_confusion/split.json ../$folder/merged.csv
        python ../train_svm.py _train.csv --test_path _valid.csv;
    fi
    
    cd /home/topcic/Documents/PDM/SuperStyl
}

if [ $# -lt 1 ]; then
    exit
fi

# Go to SuperStyl folder
cd /home/topcic/Documents/PDM/SuperStyl
# Activate environment
source env/bin/activate

# If we have 2 subreddits as inputs do the SVM for each of the Subreddits separately and then combined
if [ $# -gt 1 ]; then
    do_svm $1 0
    do_svm $2 0 
    do_svm "${1}_${2}" 1
else
    do_svm $1 0
fi
