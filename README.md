- This is the code used in my Master Thesis at EPFL. To run the scrapper, you first need to create a praw.ini by following this [tutorial](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html).
- You also need to install the [SuperStyl library](https://github.com/SupervisedStylometry/SuperStyl) in the root of the project.
- The workflow to replicate the project is the following:
  1. In utils.py, change the subreddits variable to the list of Subreddits you want to scrape and run reddit_scrapper.py
  2. Once the scraping is done, you can user find_candidate_subreddits.py to find potential pairs of Subreddits
  3. Change the pairs of Subreddits in utils.py
  4. Run get_user_comments.py to generate a list of users with their texts in the pairs of Subreddits
  5. Run get_text_for_svm.py to generate texts of the same lengths based on values in utils.py
  6. Run create_files_for_svm.py to get the txt files to use with SuperStyl
  7. You can finally run do_all_svms.py to execute the whole SVM pipeline which will get you your accuracy
  8. You can run semantic_similarity.py to compute the similarity
  9. You can run create_plots.py to generate the same plots used in the thesis
