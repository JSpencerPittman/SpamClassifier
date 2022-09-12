from re import findall, sub

class WordParser():
    def __init__(self, s):
        self.s = s

    # Returns the top k recurring words in the given
    # string
    def modeWords(self, k=10):
        sortedKeys = []
        sortedCounts = []
        wordCounts = self.wordCounts()

        for word in wordCounts:
            # check if there's space to add it
            if len(sortedCounts) < k:
                sortedKeys.append(word)
                sortedCounts.append(wordCounts[word])
            # check if the last element can sort it
            elif sortedCounts[k - 1] < wordCounts[word]:
                sortedKeys[k - 1] = word
                sortedCounts[k - 1] = wordCounts[word]
            else:
                continue

            curr_index = len(sortedCounts) - 1
            while (curr_index > 0 and sortedCounts[curr_index] > sortedCounts[curr_index - 1]):
                tempCount = sortedCounts[curr_index - 1]
                tempKey = sortedKeys[curr_index - 1]
                sortedCounts[curr_index - 1] = sortedCounts[curr_index]
                sortedKeys[curr_index - 1] = sortedKeys[curr_index]
                sortedCounts[curr_index] = tempCount
                sortedKeys[curr_index] = tempKey
                curr_index -= 1

        modeWords = []
        for wordCount in zip(sortedKeys, sortedCounts):
            modeWords.append(wordCount)
        return modeWords

    def wordCounts(self):
        wordCounts = {}
        for word in self.words():
            if word in wordCounts:
                wordCounts[word] += 1
            else:
                wordCounts[word] = 1
        return wordCounts

    # This takes a messy string and returns an array of every word in
    # it
    def words(self):
        # replace all whitespace with a single space
        # ''\n\n\n' -> ' '
        parsedString = sub('\s+', ' ', self.s)
        # remove any symbol that isn't an alphabetical character
        # or space
        parsedString = sub('[^A-Za-z ]+', '', parsedString)
        # convert the string into a list of words
        words = parsedString.split(' ')

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
        # This seperates out words that are conjoined AND
        # The first letter of the second word is capitalized
        # So 'helloThere' -> 'hello There' while 'HELLO' wouldn't
        # be affected
        for i in range(len(words)):
            unconjoinedWords = self._splitConjoinedWords(words[i])
            # even if the word wasn't a conjoined one it still
            # returns an array of length one containing the original
            # word
            words[i] = unconjoinedWords[0]
            # add the rest of the unconjoined words
            if len(unconjoinedWords) > 1:
                for i in range(1, len(unconjoinedWords)):
                    words.append(unconjoinedWords[i])

        # clean each word
        for i in range(len(words)):
            words[i] = self._cleanWord(words[i])

        # we do this the second time because after running
        # _splitConjoinedWords and _cleanWord more empty
        # entries are created
        for i in range(words.count('')):
            words.remove('')

        return words

    # removes plurals that end with s
    # and lowercases it
    def _cleanWord(self, word):
        word = sub('[s$]', '', word)
        word = word.lower()
        return word

    # many words can be joined like appleHoney
    # so this would merely return the split words
    # in a list like ['apple','Honey'] however if no
    # conjoined words are detected it merely returns the
    # original word in an array 'apple' -> ['apple']
    def _splitConjoinedWords(self, s):
        regexExpression = '[a-z][A-Z][a-z]'
        matches = findall(regexExpression, s)
        # if no conjoined words detected return list with
        # original word
        if len(matches) == 0:
            return [s]
        # for every match add a space in the string
        # and then split it into an list and return the
        # list
        for match in matches:
            unconjoinedString = match[0] + ' ' + match[1:]
            s = s.replace(match, unconjoinedString)
        return s.split(' ')

    def wordFrequencies(self):
        frequencies = self.wordCounts()
        totalWords = len(frequencies)
        for key in frequencies:
            frequencies[key] = 100 * (frequencies[key] / totalWords)
        return frequencies

    def uniqueWords(self):
        u_words = list(set(self.words()))
        return u_words


class EmailWordCounter:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.spamWordCounts = [('a', 0), ('b', 0)]
        self.hamWordCounts = [('a', 0), ('b', 0)]
        self.keySpamWordsList = []
        self.keySpamWordsDict = {}

    # This function records the repetitions of words in spam emails
    # as well as ham emails
    # returns spam emails, ham emails
    # wordCounts will be stored in a list of tuples [('word', count),...]
    def countWordOccurences(self):
        for emailIndex in range(1, len(self.X)):
            payload = self.X[emailIndex].unifyPayload()
            wa = WordParser(payload)
            words = wa.uniqueWords()
            if (self.y[emailIndex] == 1):
                self.spamWordCount = self.updateWordCount(words, True)
            else:
                self.hamWordCount = self.updateWordCount(words, False)

    def updateWordCount(self, words, isSpam):
        wordCounts = self.spamWordCounts if isSpam else self.hamWordCounts
        for word in words:

            locIndex = self.searchWordCounts(word, isSpam)
            if (locIndex >= 0):
                wordCounts[locIndex] = (word, wordCounts[locIndex][1] + 1)
            else:
                wordCounts.insert((-locIndex), (word, 1))
        return wordCounts

    def searchWordCounts(self, word, isSpam):
        wordCounts = self.spamWordCounts if isSpam else self.hamWordCounts

        upper = len(wordCounts) - 1
        lower = 0
        while lower < upper:
            searchIndex = int((upper + lower) / 2)
            if wordCounts[searchIndex][0] == word:
                return searchIndex
            elif wordCounts[searchIndex][0] > word:
                upper = searchIndex
            else:
                lower = searchIndex + 1
        while wordCounts[searchIndex][0] > word:
            searchIndex -= 1
        return -(searchIndex + 1)

    def getWordOccurence(self, word, isSpam):
        occurence = -1
        locIndex = self.searchWordCounts(word, isSpam)
        if (locIndex >= 0):
            return self.spamWordCounts[locIndex][1] if isSpam else self.hamWordCounts[locIndex][1]
        else:
            return -1

    def trimWordCounts(self):
        removalIndices = []
        for i in range(len(self.hamWordCounts)):
            if (self.hamWordCounts[i][1] < 5):
                removalIndices.append(i)
        for i in range(len(removalIndices) - 1, -1, -1):
            del self.hamWordCounts[removalIndices[i]]
        removalIndices = []
        for i in range(len(self.spamWordCounts)):
            if (self.spamWordCounts[i][1] < 5):
                removalIndices.append(i)
        for i in range(len(removalIndices) - 1, -1, -1):
            del self.spamWordCounts[removalIndices[i]]

    def balanceWordCounts(self):
        totalSpamEmails = int(self.y.sum())
        totalHamEmails = len(self.y) - totalSpamEmails
        # how much to multiply each spamWordOccurence by
        spamMultiplier = totalHamEmails / totalSpamEmails

        for i in range(len(self.spamWordCounts)):
            self.spamWordCounts[i] = (self.spamWordCounts[i][0], int(self.spamWordCounts[i][1] * spamMultiplier))

    def displayWordCounts(self):
        totalSpamWords = len(self.spamWordCounts)
        totalHamWords = len(self.hamWordCounts)

        for i in range(max(totalSpamWords, totalHamWords)):
            s = '#' + str(i) + ': '
            if (i < totalSpamWords):
                s += "SPAM " + str(self.spamWordCounts[i]) + " "
            if (i < totalHamWords):
                s += "HAM " + str(self.hamWordCounts[i]) + " "
            print(s)

    def calcKeySpamWordsList(self):
        self.countWordOccurences()
        self.trimWordCounts()
        self.balanceWordCounts()

        unsortedKeySpamWords = []
        maxOccurenceRatio = 0

        # for every spam word if it appears at least twice as much as a ham word then record it's occurence
        # ratio and the word in the unsortedKeySpamWords list
        for i in range(len(self.spamWordCounts)):
            wordCount = self.spamWordCounts[i]
            occurenceRatio = int(wordCount[1] / self.getWordOccurence(wordCount[0], False))
            if occurenceRatio >= 2:
                unsortedKeySpamWords.append((self.spamWordCounts[i][0], occurenceRatio))
                maxOccurenceRatio = max(maxOccurenceRatio, occurenceRatio)
            elif occurenceRatio < -1:
                unsortedKeySpamWords.append((self.spamWordCounts[i][0], -1))

        for i in range(maxOccurenceRatio + 1):
            self.keySpamWordsList.append([])

        for keySpamWord in unsortedKeySpamWords:
            if keySpamWord[1] > 0:
                self.keySpamWordsList[keySpamWord[1]].append(keySpamWord[0])
            else:
                self.keySpamWordsList[0].append(keySpamWord[0])

    def averageOccurenceRatio(self):
        totalWords = 0
        totalOccurenceRatios = 0
        for occurenceRatio, words in enumerate(self.keySpamWordsList[2:]):
            totalWords += len(words)
            totalOccurenceRatios += len(words) * (occurenceRatio + 2)
        return round(totalOccurenceRatios / totalWords)

    def calcKeySpamWordsDict(self):
        if (len(self.keySpamWordsList) == 0):
            self.calcKeySpamWordsList()
        leastSignificantOccurenceRatio = 2
        for occurenceRatio in range(leastSignificantOccurenceRatio, len(self.keySpamWordsList)):
            for word in self.keySpamWordsList[occurenceRatio]:
                self.keySpamWordsDict[word] = occurenceRatio
        avgOccRatio = self.averageOccurenceRatio()
        for word in self.keySpamWordsList[0]:
            self.keySpamWordsDict[word] = avgOccRatio


class EmailQuantifier:
    orderedAttributes = ["SpamWordIndex", "CarbonCopies", "PriceOcc", "PercentOcc", "LinkOcc", "UnsecureLinkOcc",
                         "SecureLinkOcc", "SpecialCharOcc", "UppercaseWordOcc"]

    def __init__(self, spamKeyWordsDict):
        self._spamKeyWordsDict = spamKeyWordsDict

    def quantifySingleEmail(self, email):
        numRepresentation = []
        numRepresentation.append(self.calcSpamWordIndex(email))
        numRepresentation.append(self.countCarbonCopies(email))
        numRepresentation.append(self.countPriceOccurences(email))
        numRepresentation.append(self.countPercentageOccurences(email))
        numRepresentation.append(self.countLinkOccurences(email))
        numRepresentation.append(self.countUnsecureLinkOccurences(email))
        numRepresentation.append(self.countSecureLinkOccurences(email))
        numRepresentation.append(self.countSpecialCharactersOccurences(email))
        numRepresentation.append(self.countUppercaseWordOccurences(email))
        return numRepresentation

    # Each row is for a single email
    def quantifyBatchEmails(self, emails):
        numRepresentations = []
        for email in emails:
            numRepresentations.append(self.quantifySingleEmail(email))
        return numRepresentations

    def calcSpamWordIndex(self, email):
        wp = WordParser(email.unifyPayload())
        words = wp.words()

        spamWordIndex = 0
        for word in words:
            if word in self._spamKeyWordsDict:
                spamWordIndex += self._spamKeyWordsDict[word]
        spamWordIndex = int((spamWordIndex * 100) / len(words))
        return spamWordIndex

    def countCarbonCopies(self, email):
        if email.copies == None:
            return 0
        total = 0
        total += email.copies.count(',')
        if len(email.copies) > 0:
            total += 1
        return total

    def countPriceOccurences(self, email):
        return self._regexPayloadSearch('\$[0-9\.]+', email)

    def countPercentageOccurences(self, email):
        return self._regexPayloadSearch('[0-9\.]+%', email)

    def countLinkOccurences(self, email):
        return self._regexPayloadSearch('[h][t][t][p]', email)

    def countUnsecureLinkOccurences(self, email):
        return self._regexPayloadSearch('[h][t][t][p][:]', email)

    def countSecureLinkOccurences(self, email):
        return self._regexPayloadSearch('[h][t][t][p][s][:]', email)

    def countSpecialCharactersOccurences(self, email):
        return self._regexPayloadSearch('[^a-zA-Z0-9\s]', email)

    def countUppercaseWordOccurences(self, email):
        return self._regexPayloadSearch('[A-Z]{2,100}', email)

    def _regexPayloadSearch(self, regexStr, email):
        return len(findall(regexStr, email.unifyPayload()))
