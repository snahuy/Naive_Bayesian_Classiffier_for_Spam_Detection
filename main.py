# Name: Veasna Huy (Sna)
# Class: IT348 (Introduction to Artificial Intelligence)

## A Naïve Bayesian Classifier for Spam (Phishing) Detection

import os
import random


# Function to read text files from folders
def read_text_files_from_folder(file_path, list_of_text_files):
    data_folder = os.path.join(os.getcwd(), file_path)
    print(f"Reading Files: " + file_path)
    for root, folders, files in os.walk(data_folder):
        for file in files:
            path = os.path.join(root, file)
            with open(path) as inf:
                list_of_text_files.append(inf.read())


# Bernoulli Model
# Function to create dictionary. Word as the key, amount of it as the value. We only count the word once in each list
def word_dictionary(chosen_list, new_dictionary):
    for i in range(0, len(chosen_list)):
        temp_list = []
        temp = chosen_list[i].split()
        for j in range(0, len(temp)):
            if temp[j] not in new_dictionary:
                new_dictionary[temp[j]] = 1
                temp_list.append(temp[j])
            elif temp[j] in new_dictionary and temp[j] not in temp_list:
                new_dictionary[temp[j]] += 1


if __name__ == "__main__":
    # List of Ham Emails
    good_email_list = []
    # List of Spam Emails
    spam_email_list = []

    # Read them and add them to the list
    read_text_files_from_folder(r'email data\Ham\300 good emails', good_email_list)
    read_text_files_from_folder(r'email data\Ham\301-600 good ones', good_email_list)
    read_text_files_from_folder(r'email data\Spam', spam_email_list)
    print("Files Read." + "\n")

    # Shuffle the list
    random.shuffle(good_email_list)
    random.shuffle(spam_email_list)

    # List of testing emails
    ham_testing_set = good_email_list[:100]
    spam_testing_set = spam_email_list[:100]
    testing_set = ham_testing_set + spam_testing_set

    # Training set
    ham_training_set = good_email_list[100:600]
    spam_training_set = spam_email_list[100:600]

    # Dictionary of words in Ham email as a key and the amount it was repeated as value
    words_in_good_email_dictionary = {}
    word_dictionary(ham_training_set, words_in_good_email_dictionary)

    # Dictionary of words in Spam email as a key and the amount it was repeated as value
    words_in_spam_email_dictionary = {}
    word_dictionary(spam_training_set, words_in_spam_email_dictionary)

    # Dictionary to store the probability of the word for the HAM Emails
    prob_words_in_ham_email_dict = {}
    # Dictionary to store the probability of the word for the SPAM Emails
    prob_words_in_spam_email_dict = {}

    # Dictionary to store the probability of the word for HAM emails using Bernoulli Model
    number_of_key_ham_dic = len(words_in_good_email_dictionary)
    for key_ham, value_ham in words_in_good_email_dictionary.items():
        # Assign the ham word (key) to the probability of the HAM email
        prob_words_in_ham_email_dict[key_ham] = (value_ham + 1) / (len(ham_training_set) + 2)

    # Get the probability of the word for SPAM emails using Bernoulli Model
    number_of_key_spam_dic = len(words_in_spam_email_dictionary)
    for key_spam, value_spam in words_in_spam_email_dictionary.items():
        # Assign the spam word (key) to the probability of the spam email
        prob_words_in_spam_email_dict[key_spam] = (value_spam + 1) / (len(spam_training_set) + 2)

    prob_analysis_ham_test = {}
    prob_analysis_spam_test = {}

    print("Training Set....." + "\n")
    # Training the set
    for test_email in testing_set:
        email = test_email.split()
        prob_analysis_ham_test[test_email] = 0.5
        for word in email:
            if word not in prob_words_in_ham_email_dict:
                prob_words_in_ham_email_dict[word] = 1 / (len(ham_training_set) + 2)
            prob_analysis_ham_test[test_email] *= prob_words_in_ham_email_dict[word]
    for test_email in testing_set:
        email = test_email.split()
        prob_analysis_spam_test[test_email] = 0.5
        for word in email:
            if word not in prob_words_in_spam_email_dict:
                prob_words_in_spam_email_dict[word] = 1 / (len(spam_training_set) + 2)
            prob_analysis_spam_test[test_email] *= prob_words_in_spam_email_dict[word]

    # Calculating the Results
    true_positive = 0
    false_negative = 0
    true_negative = 0
    false_positive = 0

    # Comparing the probability of each training set to check and see if its TP, FN, TN or FP
    for ham_email in ham_testing_set:
        if ham_email in ham_testing_set:
            if prob_analysis_ham_test[ham_email] > prob_analysis_spam_test[ham_email]:
                true_positive += 1
            else:
                false_negative += 1

    for spam_email in spam_testing_set:
        if spam_email in spam_testing_set:
            if prob_analysis_spam_test[spam_email] > prob_analysis_ham_test[spam_email]:
                true_negative += 1
            else:
                false_positive += 1

    print("Results:")
    print(f"True Positive: " + str(true_positive))
    print(f"False Negative: " + str(false_negative))
    print(f"True Negative: " + str(true_negative))
    print(f"False Positive: " + str(false_positive))

    accuracy = (true_positive + true_negative) / (true_positive + false_positive + true_negative + false_negative)
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    true_negative_rate = true_negative / (true_negative + false_positive)
    f1_score = (2 * precision * recall) / (precision + recall)

    print()
    print(f"Accuracy: " + str(accuracy))
    print(f"Precision: " + str(precision))
    print(f"Recall: " + str(round(recall)))
    print(f"True Negative Rate: " + str(true_negative_rate))
    print(f"F1 Score: " + str(f1_score))
