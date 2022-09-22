from re import findall, sub


class WordParser():
    """
    A Library that provides utility functions to
    analyze strings
    """

    def __init__(self, s):
        self.s = s

    # Returns the top k recurring words in the given
    # string
    def modeWords(self, k=10):
        """
        Returns the top k recurring words in the given string
        """

        sorted_keys = []
        sorted_counts = []
        word_counts = self.word_counts()

        for word in word_counts:
            # check if there's space to add it
            if len(sorted_counts) < k:
                sorted_keys.append(word)
                sorted_counts.append(word_counts[word])
            # check if the last element can sort it
            elif sorted_counts[k - 1] < word_counts[word]:
                sorted_keys[k - 1] = word
                sorted_counts[k - 1] = word_counts[word]
            else:
                continue

            curr_index = len(sorted_counts) - 1
            while curr_index > 0 and sorted_counts[curr_index] > sorted_counts[curr_index - 1]:
                temp_count = sorted_counts[curr_index - 1]
                temp_key = sorted_keys[curr_index - 1]
                sorted_counts[curr_index - 1] = sorted_counts[curr_index]
                sorted_keys[curr_index - 1] = sorted_keys[curr_index]
                sorted_counts[curr_index] = temp_count
                sorted_keys[curr_index] = temp_key
                curr_index -= 1

        mode_words = []
        for wordCount in zip(sorted_keys, sorted_counts):
            mode_words.append(wordCount)
        return mode_words

    def word_counts(self):
        word_counts = {}
        for word in self.words():
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
        return word_counts

    # This takes a messy string and returns an array of every word in
    # it
    def words(self):
        # replace all whitespace with a single space
        # ''\n\n\n' -> ' '
        parsed_string = sub('\s+', ' ', self.s)
        # remove any symbol that isn't an alphabetical character
        # or space
        parsed_string = sub('[^A-Za-z ]+', '', parsed_string)
        # convert the string into a list of words
        words = parsed_string.split(' ')

        # There are many empty entries that often get
        # counted so this removes them from words
        for i in range(words.count('')):
            words.remove('')

        # seperate out words that may be conjoined
        # capitalization in the middle but not
        # surrounded by caps catched helloThere but not
        # HELLO

        # Problem:
        # A common problem is words get merged after
        # removing special characters
        # Partial Solution:
        # This separates out words that are conjoined AND
        # The first letter of the second word is capitalized
        # So 'helloThere' -> 'hello There' while 'HELLO' wouldn't
        # be affected
        for i in range(len(words)):
            unconjoined_words = self._split_conjoined_words(words[i])
            # even if the word wasn't a conjoined one it still
            # returns an array of length one containing the original
            # word
            words[i] = unconjoined_words[0]
            # add the rest of the unconjoined words
            if len(unconjoined_words) > 1:
                for i in range(1, len(unconjoined_words)):
                    words.append(unconjoined_words[i])

        # clean each word
        for i in range(len(words)):
            words[i] = self._clean_word(words[i])

        # we do this the second time because after running
        # _splitConjoinedWords and _cleanWord more empty
        # entries are created
        for i in range(words.count('')):
            words.remove('')

        return words

    # removes plurals that end with s
    # and lowercases it
    @staticmethod
    def _clean_word(word):
        word = sub('[s$]', '', word)
        word = word.lower()
        return word

    # many words can be joined like appleHoney
    # so this would merely return the split words
    # in a list like ['apple','Honey'] however if no
    # conjoined words are detected it merely returns the
    # original word in an array 'apple' -> ['apple']
    @staticmethod
    def _split_conjoined_words(s):
        regex_expression = '[a-z][A-Z][a-z]'
        matches = findall(regex_expression, s)
        # if no conjoined words detected return list with
        # original word
        if len(matches) == 0:
            return [s]
        # for every match add a space in the string
        # and then split it into an list and return the
        # list
        for match in matches:
            unconjoined_string = match[0] + ' ' + match[1:]
            s = s.replace(match, unconjoined_string)
        return s.split(' ')

    def word_frequencies(self):
        frequencies = self.word_counts()
        total_words = len(frequencies)
        for key in frequencies:
            frequencies[key] = 100 * (frequencies[key] / total_words)
        return frequencies

    def unique_words(self):
        u_words = list(set(self.words()))
        return u_words


class EmailWordCounter:
    def __init__(self, X, y):
        self.ham_word_count = None
        self.spam_word_count = None
        self.X = X
        self.y = y
        self.spam_word_counts = [('a', 0), ('b', 0)]
        self.ham_word_counts = [('a', 0), ('b', 0)]
        self.key_spam_words_list = []
        self.key_spam_words_dict = {}

    # This function records the repetitions of words in spam emails
    # as well as ham emails
    # returns spam emails, ham emails
    # wordCounts will be stored in a list of tuples [('word', count),...]
    def count_word_occurences(self):
        for emailIndex in range(1, len(self.X)):
            payload = self.X[emailIndex].unifyPayload()
            wa = WordParser(payload)
            words = wa.unique_words()
            if self.y[emailIndex] == 1:
                self.spam_word_count = self.update_word_count(words, True)
            else:
                self.ham_word_count = self.update_word_count(words, False)

    def update_word_count(self, words, isSpam):
        word_counts = self.spam_word_counts if isSpam else self.ham_word_counts
        for word in words:

            loc_index = self.search_word_counts(word, isSpam)
            if loc_index >= 0:
                word_counts[loc_index] = (word, word_counts[loc_index][1] + 1)
            else:
                word_counts.insert((-loc_index), (word, 1))
        return word_counts

    def search_word_counts(self, word, isSpam):
        word_counts = self.spam_word_counts if isSpam else self.ham_word_counts

        upper = len(word_counts) - 1
        lower = 0
        while lower < upper:
            search_index = int((upper + lower) / 2)
            if word_counts[search_index][0] == word:
                return search_index
            elif word_counts[search_index][0] > word:
                upper = search_index
            else:
                lower = search_index + 1
        while word_counts[search_index][0] > word:
            search_index -= 1
        return -(search_index + 1)

    def get_word_occurence(self, word, is_spam):
        loc_index = self.search_word_counts(word, is_spam)
        if loc_index >= 0:
            return self.spam_word_counts[loc_index][1] if is_spam else self.ham_word_counts[loc_index][1]
        else:
            return -1

    def trim_word_counts(self):
        removal_indices = []
        for i in range(len(self.ham_word_counts)):
            if self.ham_word_counts[i][1] < 5:
                removal_indices.append(i)
        for i in range(len(removal_indices) - 1, -1, -1):
            del self.ham_word_counts[removal_indices[i]]
        removal_indices = []
        for i in range(len(self.spam_word_counts)):
            if self.spam_word_counts[i][1] < 5:
                removal_indices.append(i)
        for i in range(len(removal_indices) - 1, -1, -1):
            del self.spam_word_counts[removal_indices[i]]

    def balance_word_counts(self):
        total_spam_emails = int(self.y.sum())
        total_ham_emails = len(self.y) - total_spam_emails
        # how much to multiply each spamWordOccurence by
        spam_multiplier = total_ham_emails / total_spam_emails

        for i in range(len(self.spam_word_counts)):
            self.spam_word_counts[i] = (self.spam_word_counts[i][0], int(self.spam_word_counts[i][1] * spam_multiplier))

    def display_word_counts(self):
        total_spam_words = len(self.spam_word_counts)
        total_ham_words = len(self.ham_word_counts)

        for i in range(max(total_spam_words, total_ham_words)):
            s = '#' + str(i) + ': '
            if i < total_spam_words:
                s += "SPAM " + str(self.spam_word_counts[i]) + " "
            if i < total_ham_words:
                s += "HAM " + str(self.ham_word_counts[i]) + " "
            print(s)

    def calc_key_spam_words_list(self):
        self.count_word_occurences()
        self.trim_word_counts()
        self.balance_word_counts()

        unsorted_key_spam_words = []
        max_occurence_ratio = 0

        # for every spam word if it appears at least twice as much as a ham word then record it's occurence
        # ratio and the word in the unsorted_key_spam_words list
        for i in range(len(self.spam_word_counts)):
            word_count = self.spam_word_counts[i]
            occurence_ratio = int(word_count[1] / self.get_word_occurence(word_count[0], False))
            if occurence_ratio >= 2:
                unsorted_key_spam_words.append((self.spam_word_counts[i][0], occurence_ratio))
                max_occurence_ratio = max(max_occurence_ratio, occurence_ratio)
            elif occurence_ratio < -1:
                unsorted_key_spam_words.append((self.spam_word_counts[i][0], -1))

        for i in range(max_occurence_ratio + 1):
            self.key_spam_words_list.append([])

        for keySpamWord in unsorted_key_spam_words:
            if keySpamWord[1] > 0:
                self.key_spam_words_list[keySpamWord[1]].append(keySpamWord[0])
            else:
                self.key_spam_words_list[0].append(keySpamWord[0])

    def average_occurence_ratio(self) -> object:
        total_words = 0
        total_occurence_ratios = 0
        for occurenceRatio, words in enumerate(self.key_spam_words_list[2:]):
            total_words += len(words)
            total_occurence_ratios += len(words) * (occurenceRatio + 2)
        return round(total_occurence_ratios / total_words)

    def calc_key_spam_words_dict(self):
        if len(self.key_spam_words_list) == 0:
            self.calc_key_spam_words_list()
        least_significant_occurence_ratio = 2
        for occurenceRatio in range(least_significant_occurence_ratio, len(self.key_spam_words_list)):
            for word in self.key_spam_words_list[occurenceRatio]:
                self.key_spam_words_dict[word] = occurenceRatio
        avg_occ_ratio = self.average_occurence_ratio()
        for word in self.key_spam_words_list[0]:
            self.key_spam_words_dict[word] = avg_occ_ratio


class EmailQuantifier:
    orderedAttributes = ["SpamWordIndex", "CarbonCopies", "PriceOcc", "PercentOcc", "LinkOcc", "UnsecureLinkOcc",
                         "SecureLinkOcc", "SpecialCharOcc", "UppercaseWordOcc"]

    def __init__(self, spam_key_words_dict):
        self._spam_key_words_dict = spam_key_words_dict

    def quantify_single_email(self, email):
        num_representation = [self.calc_spam_word_index(email), self.count_carbon_copies(email),
                              self.count_price_occurences(email), self.count_percentage_occurences(email),
                              self.count_link_occurences(email), self.count_unsecure_link_occurences(email),
                              self.count_secure_link_occurences(email), self.count_special_characters_occurences(email),
                              self.count_uppercase_word_occurences(email)]
        return num_representation

    # Each row is for a single email
    def quantify_batch_emails(self, emails):
        num_representations = []
        for email in emails:
            num_representations.append(self.quantify_single_email(email))
        return num_representations

    def calc_spam_word_index(self, email):
        wp = WordParser(email.unifyPayload())
        words = wp.words()

        spam_word_index = 0
        for word in words:
            if word in self._spam_key_words_dict:
                spam_word_index += self._spam_key_words_dict[word]
        spam_word_index = int((spam_word_index * 100) / len(words))
        return spam_word_index

    @staticmethod
    def count_carbon_copies(email):
        if email.copies is None:
            return 0
        total = 0
        total += email.copies.count(',')
        if len(email.copies) > 0:
            total += 1
        return total

    def count_price_occurences(self, email):
        return self._regex_payload_search('\$[0-9\.]+', email)

    def count_percentage_occurences(self, email):
        return self._regex_payload_search('[0-9\.]+%', email)

    def count_link_occurences(self, email):
        return self._regex_payload_search('[h][t][t][p]', email)

    def count_unsecure_link_occurences(self, email):
        return self._regex_payload_search('[h][t][t][p][:]', email)

    def count_secure_link_occurences(self, email):
        return self._regex_payload_search('[h][t][t][p][s][:]', email)

    def count_special_characters_occurences(self, email):
        return self._regex_payload_search('[^a-zA-Z0-9\s]', email)

    def count_uppercase_word_occurences(self, email):
        return self._regex_payload_search('[A-Z]{2,100}', email)

    @staticmethod
    def _regex_payload_search(regexStr, email):
        return len(findall(regexStr, email.unifyPayload()))
