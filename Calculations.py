import math
from decimal import *


# def unknownify(dictionary_keys):
#     for key in dictionary_keys:
#         if key in training_dictionary.keys():
#             continue
#         else:
#             unknown_test_words.append(key)

def bigramify_sentence(sentence):
    sentence_dictionary = {}
    for word in sentence.split():
        if word not in training_dictionary:
            sentence = sentence.replace(" " + word + " ", " <unk> ")
    words = sentence.split()
    for i in range(1, len(words)):
        if (words[i - 1] + " " + words[i]) in sentence_dictionary:
            sentence_dictionary[words[i - 1] + " " + words[i]] += 1
        else:
            sentence_dictionary[words[i - 1] + " " + words[i]] = 1
    return sentence_dictionary.keys()


def bigramify_file(file):  # Used to get Bigram Dictionaries
    bigrams_dictionary = {}
    file_console = open(file, 'r')
    sentences = file_console.readlines()
    for sentence in sentences:
        words = sentence.split()
        for i in range(1, len(words)):
            if (words[i - 1] + " " + words[i]) in bigrams_dictionary:
                bigrams_dictionary[words[i - 1] + " " + words[i]] += 1
            else:
                bigrams_dictionary[words[i - 1] + " " + words[i]] = 1
    return bigrams_dictionary


def get_token_sum(dictionary):  # Used for Questions 2,3
    token_sum = 0
    for word_frequency in dictionary.values():
        token_sum += word_frequency
    # token_sum -= (dictionary["<s>"] + dictionary["</s>"])
    return token_sum


def find_unknowns(dictionary):  # Used for Question 3
    unobserved_words_list = []
    unobserved_words_frequency = 0
    unobserved_tokens_frequency = 0
    for key in dictionary:
        if (key not in training_dictionary) and (key != ("<s>" or "</s>")):
            unobserved_tokens_frequency += dictionary[key]
            if key not in unobserved_words_list:
                unobserved_words_list.append(key)
    unobserved_words_frequency = unobserved_words_list.__len__()
    return unobserved_words_frequency, unobserved_tokens_frequency


def dictionarize(file_name):  # Used to get initial data
    file = open(file_name, 'r')
    file_data = file.read()
    file.close()
    file_data = file_data.split()
    word_dict = {}
    for word in file_data:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    return word_dict


def compare_bigrams(bigram_compare):  # Used for Question 4
    unobserved_word_bigrams_sum = 0
    unobserved_token_bigrams_sum = 0
    total_tokens = 0
    for key in bigram_compare:
        if key in bigrams_training:
            total_tokens += bigram_compare[key]
        else:
            total_tokens += bigram_compare[key]
            unobserved_word_bigrams_sum += 1
            unobserved_token_bigrams_sum += bigram_compare[key]
    unobserved_word_bigrams_percentage = unobserved_word_bigrams_sum / len(bigram_compare)
    unobserved_token_bigrams_percentage = unobserved_token_bigrams_sum / total_tokens
    return unobserved_word_bigrams_percentage, unobserved_token_bigrams_percentage


def unigram_test(sentence):  # Used for Question 5
    words = sentence.split()
    log_probability = 1
    # written_result = "Unigram Calculation for: %s \n" % (sentence)
    for word in words:
        if word in training_dictionary:
            # written_result += "C(%s)/C(total tokens) = %s / %s \n" % (word, training_dictionary[word], token_sum)
            log_probability *= (training_dictionary[word] / token_sum)
        else:
            log_probability *= (training_dictionary["<unk>"] / token_sum)
    # written_result += "Multiplication and Log Result: %s" % (math.log(total_probability, 2))
    # print(written_result)

    try:
        return math.log(log_probability,2)
    except ValueError:
        return math.inf




def bigram_test(sentence):  # Used for Question 5

    sentence_bigrams = bigramify_sentence(sentence)
    result = 1
    # written_result = "Bigram Calculation for: %s \n" % (sentence)
    for test_bigram in sentence_bigrams:
        if test_bigram in bigrams_training:
            # written_result += "C(%s)/C(%s) = %s / %s \n" % (test_bigram,
            #                                                 test_bigram.split()[0],
            #                                                 bigrams_training[test_bigram],
            #                                                 training_dictionary[test_bigram.split()[0]])
            result *= (bigrams_training[test_bigram] / training_dictionary[test_bigram.split()[0]])
        else:
            # written_result += "C(%s)/C(%s) = 0 \n" % (test_bigram,
            #                                           test_bigram.split()[0])
            result = 0
    # written_result += "Multiplication and Log Result: %s" % (result)
    if result == 0:
        # print(written_result)
        return 0
    # print(written_result)
    return math.log(result,2)


def bigram_test_addone(sentence):  # Used for Question 5
    sentence_bigrams = bigramify_sentence(sentence)
    result = 1
    # written_result = "Bigram Add One Calculation for: %s \n" % (sentence)
    for test_bigram in sentence_bigrams:
        if test_bigram in bigrams_training:
            # written_result += "(C(%s) + 1)/(C(%s) + %s) = %s / %s \n" % (test_bigram,
            #                                                              test_bigram.split()[0],
            #                                                              len(bigrams_training),
            #                                                              bigrams_training[test_bigram] + 1,
            #                                                              training_dictionary[
            #                                                                  test_bigram.split()[0]] + len(
            #                                                                  bigrams_training))
            result *= (bigrams_training[test_bigram] + 1 / (
                    training_dictionary[test_bigram.split()[0]] + len(bigrams_training)))
        else:
            # written_result += "(C(%s) + 1)/(C(%s) + %s) = %s / %s \n" % (test_bigram,
            #                                                              test_bigram.split()[0],
            #                                                              len(bigrams_training),
            #                                                              0 + 1,
            #                                                              training_dictionary[
            #                                                                  test_bigram.split()[0]] + len(
            #                                                                  bigrams_training))

            result *= (1 / (training_dictionary[test_bigram.split()[0]] + len(bigrams_training)))
    # written_result += "Multiplication and Log Result is: %s" % result
    # print(written_result)
    return math.log(result,2)


def compute_perplexity(log_prob, sentence_length):
    length = sentence_length
    return 2 ** ((-1) * log_prob / length)


def corpus_perplexity(file):    # Not being used
    file_console = open(file, 'r')
    file_lines = file_console.readlines()
    file_console.close()
    total_prob_unigram = 0
    total_prob_bigram = 0
    total_prob_bigram_addone = 0
    for line in file_lines:
        total_prob_unigram += unigram_test(line)
        total_prob_bigram += bigram_test(line)
        total_prob_bigram_addone += bigram_test_addone(line)
    file_console = open(file, 'r')
    file_data = file_console.read()
    size = file_data.split().__len__()
    return (compute_perplexity(total_prob_unigram, size),
            compute_perplexity(total_prob_bigram, size),
            compute_perplexity(total_prob_bigram_addone, size))


def corpus_perplexity_unigram(file):
    file_console = open(file, 'r')
    file_lines = file_console.readlines()
    file_console.close()
    total_prob_unigram = 0
    for line in file_lines:
        total_prob_unigram += unigram_test(line)
    file_console = open(file, 'r')
    file_data = file_console.read()
    size = file_data.split().__len__()
    return compute_perplexity(total_prob_unigram, size)


def corpus_perplexity_bigram(file):
    file_console = open(file, 'r')
    file_lines = file_console.readlines()
    file_console.close()
    total_prob_bigram = 0
    for line in file_lines:
        total_prob_bigram += bigram_test(line)
    file_console = open(file, 'r')
    file_data = file_console.read()
    size = file_data.split().__len__()
    return compute_perplexity(total_prob_bigram, size)


def corpus_perplexity_bigram_addone(file):
    file_console = open(file, 'r')
    file_lines = file_console.readlines()
    file_console.close()
    total_prob_bigram_addone = 0
    for line in file_lines:
        total_prob_bigram_addone += bigram_test_addone(line)
    file_console = open(file, 'r')
    file_data = file_console.read()
    size = file_data.split().__len__()
    return compute_perplexity(total_prob_bigram_addone, size)


training_dictionary = dictionarize("brown-train.txt")
brown_test_dictionary = dictionarize("brown-test.txt")
learner_test_dictionary = dictionarize("learner-test.txt")

# Question 1
word_types = training_dictionary.__len__()
print("Training Total Unique Words:", word_types)

# Question 2
token_sum = get_token_sum(training_dictionary)
print("Training Token Sum:", token_sum)

# Question 3
brown_test_counts = find_unknowns(brown_test_dictionary)
learner_test_counts = find_unknowns(learner_test_dictionary)
# For brown test
unobserved_brown_word_percentage = brown_test_counts[0] / (brown_test_dictionary.__len__())
unobserved_brown_token_percentage = brown_test_counts[1] / get_token_sum(brown_test_dictionary)
print("Unobserved Word Percentage in Brown:", unobserved_brown_word_percentage)
print("Unobserved Token Percentage in Brown:", unobserved_brown_token_percentage)
# Unobserved Word Percentage in Brown: 0.3124370594159114
# Unobserved Token Percentage in Brown: 0.07356253704801423

# For Learner Test
unobserved_learner_word_percentage = learner_test_counts[0] / learner_test_dictionary.__len__()
unobserved_learner_token_percentage = learner_test_counts[1] / get_token_sum(learner_test_dictionary)
print("Unobserved Word Percentage in Learner:", unobserved_learner_word_percentage)
print("Unobserved Token Percentage in Learner:", unobserved_learner_token_percentage)
# Unobserved Word Percentage in Learner: 0.194621372965322
# Unobserved Token Percentage in Learner: 0.033659730722154224

# ------ #

# Generating Bigrams of all data
bigrams_training = bigramify_file("brown-train.txt")
bigrams_brown = bigramify_file("brown-test-unknowns.txt")
bigrams_learner = bigramify_file("learner-test-unknowns.txt")

# Question 4
# Prints Percentage of Unobserved Bigrams and Unobserved Tokens, respectively
brown_compare = compare_bigrams(bigrams_brown)
learner_compare = compare_bigrams(bigrams_learner)
print("Brown's Unobserved Bigram Words Percentage is %s and Tokens Percentage is %s" % brown_compare)
print("Learner's Unobserved Bigram Words Percentage is %s and Tokens Percentage is %s" % learner_compare)

# Question 5. Sentences are manually padded.
# Testing the sentences on the unigram model.
test_sentence_1 = "<s> he was laughed off the screen . </s>"
test_sentence_2 = "<s> there was no compulsion behind them . </s>"
test_sentence_3 = "<s> i look forward to hearing your reply . </s>"

sentence_1_unigram = unigram_test(test_sentence_1)
sentence_2_unigram = unigram_test(test_sentence_2)
sentence_3_unigram = unigram_test(test_sentence_3)

print("The log probabilities, under the unigram model, "
      "of the three sentences are %s, %s, %s respectively" % (sentence_1_unigram,
                                                              sentence_2_unigram,
                                                              sentence_3_unigram))
sentence_1_bigram = bigram_test(test_sentence_1)
sentence_2_bigram = bigram_test(test_sentence_2)
sentence_3_bigram = bigram_test(test_sentence_3)

print("The log probabilities, under the bigram model, "
      "of the three sentences are %s, %s, %s respectively" % (sentence_1_bigram,
                                                              sentence_2_bigram,
                                                              sentence_3_bigram))

sentence_1_bigram_addone = bigram_test_addone(test_sentence_1)
sentence_2_bigram_addone = bigram_test_addone(test_sentence_2)
sentence_3_bigram_addone = bigram_test_addone(test_sentence_3)

print("The log probabilities, under the bigram Add-One model, "
      "of the three sentences are %s, %s, %s respectively" % (sentence_1_bigram_addone,
                                                              sentence_2_bigram_addone,
                                                              sentence_3_bigram_addone))

# Question 6
print("Perplexity for Sentence 1 Unigram model : %s" % compute_perplexity(sentence_1_unigram,
                                                                          test_sentence_1.split().__len__()))
print("Perplexity for Sentence 2 Unigram model : %s" % compute_perplexity(sentence_2_unigram,
                                                                          test_sentence_2.split().__len__()))
print("Perplexity for Sentence 3 Unigram model : %s" % compute_perplexity(sentence_3_unigram,
                                                                          test_sentence_3.split().__len__()))

print("Perplexity for Sentence 1 Bigram model : %s" % compute_perplexity(sentence_1_bigram,
                                                                         test_sentence_1.split().__len__()))
print("Perplexity for Sentence 2 Bigram model : %s" % compute_perplexity(sentence_2_bigram,
                                                                         test_sentence_2.split().__len__()))
print("Perplexity for Sentence 3 Bigram model : %s" % compute_perplexity(sentence_3_bigram,
                                                                         test_sentence_3.split().__len__()))

print("Perplexity for Sentence 1 Bigram-AddOne model : %s" % compute_perplexity(sentence_1_bigram_addone,
                                                                                test_sentence_1.split().__len__()))
print("Perplexity for Sentence 2 Bigram-AddOne model : %s" % compute_perplexity(sentence_2_bigram_addone,
                                                                                test_sentence_2.split().__len__()))
print("Perplexity for Sentence 3 Bigram-AddOne model : %s" % compute_perplexity(sentence_3_bigram_addone,
                                                                                test_sentence_3.split().__len__()))

# Question 7
print("brown test has unigram perplexity of %s, bigram perplexity of %s, bigram add-one perplexity of %s"
      % (corpus_perplexity_unigram("brown-test-unknowns.txt"),
         corpus_perplexity_bigram("brown-test-unknowns.txt"),
         corpus_perplexity_bigram_addone("brown-test-unknowns.txt")))

print("learner test has unigram perplexity of %s, bigram perplexity of %s, bigram add-one perplexity of %s"
      % (corpus_perplexity_unigram("learner-test-unknowns.txt"),
         corpus_perplexity_bigram("learner-test-unknowns.txt"),
         corpus_perplexity_bigram_addone("learner-test-unknowns.txt")))
