#Padding the Sentences and making them Lowercase
def padFile(fileName):
    file = open(fileName, "r")
    file_sentences = file.readlines()
    file.close()
    for sentence in range(0, len(file_sentences)):
        file_sentences[sentence] = file_sentences[sentence].lower()
        file_sentences[sentence] = file_sentences[sentence].rstrip("\n")
        file_sentences[sentence] = "<s> " + file_sentences[sentence] + " </s>"
    file = open(fileName, "w")
    file.close()
    file = open(fileName, "a")
    for new_sentence in file_sentences:
        file.write(new_sentence + "\n")
    return file_sentences


#Creating Word Dictionaries
def get_word_frequency(sentences):
    frequency_dict = {}
    for sentence in sentences:
        split_sentence = sentence.split()
        for word in split_sentence:
            if word in frequency_dict:
                frequency_dict[word] += 1
            else:
                frequency_dict[word] = 1
    return frequency_dict


#Marking Unknowns in the Training Data
def mark_unknowns_training(file):
    one_time_words = []
    for word, frequency in training_dict.items():
        if frequency <= 1:
            one_time_words.append(word)
    file_console = open(file, 'r')
    file_data = file_console.read()
    file_console.close()
    for lone_word in one_time_words:
        file_data = file_data.replace(" "+lone_word+" ", " <unk> ")
    file_console = open(file, 'w')
    file_console.write(file_data)


#Marking unknowns in Tests
def mark_unknowns_tests(file, respective_dict_keys):
    file_console = open(file, 'r')
    file_data = file_console.read()
    file_console.close()
    for test_word in respective_dict_keys:
        if test_word not in training_dict.keys():
            file_data = file_data.replace(" "+test_word+" ", " <unk> ")
    file = file[:-4]
    file_console = open(file+"-unknowns.txt", 'w+')
    file_console.write(file_data)


# Padding the sentences, making them lowercase, and putting results in a list
training_sentences = padFile("brown-train.txt")
brown_test_sentences = padFile("brown-test.txt")
learner_training_sentences = padFile("learner-test.txt")

# Separating the tokens and putting them in dictionary
training_dict = get_word_frequency(training_sentences)
brown_test_dict = get_word_frequency(brown_test_sentences)
learner_test_dict = get_word_frequency(learner_training_sentences)

# Marking the unknowns
mark_unknowns_training("brown-train.txt")
mark_unknowns_tests("brown-test.txt", brown_test_dict.keys())
mark_unknowns_tests("learner-test.txt", learner_test_dict.keys())