# cosmogramma.py
# by Matt Dargen
#
# Class for easily constructing random sentences from text files

import random

class Cosmogramma:

    # __init__
    #   fileName = name of text file to be read from
    #   n = number of words per gram (n > 1)
    #   start = symbol in text file representing the beginning of a sentence
    #   end = symbol in text file representing the end of a line
    def __init__(self, fileName, n, start="<s>", end="<e>"):
        self.r = random.Random()
        try:
            #open input file
            self.file = file = open(fileName,'r')

            #construct list of grams
            tokens = file.read().split()
            self.n = n
            if n > 1:
                self.__construct_grams__(tokens)
            else:
                self.grams = []
                #n outside of acceptable range
                raise NException

            #make sure that start and end are in file
            if start not in tokens and end not in tokens:
                raise SymbolException("start and end symbols")
            elif start not in tokens:
                raise SymbolException("start symbol")
            elif end not in tokens:
                raise SymbolException("end symbol")
            else:
                #set start and end symbols
                self.start = start
                self.end = end
        except IOError:
            print("Error initializing NGram: " + str(fileName) + " not found")
        except NException:
            print("Error initializing NGram: " + str(n) + " is outside of acceptable range (2-4)")
        except SymbolException as e:
            print("Error initializing NGram: specified " + e.message + " is not in input file!")

    def __construct_grams__(self, tokens):
        self.grams = []
        g = []
        for i in range(len(tokens) - self.n):
            for j in range(self.n):
                g.append(tokens[i+j])
            self.grams.append(g)
            g = []

    # set_symbols(start, end)
    # sets the start and end symbols
    #   start = symbol in text file that represents the beginning of a sentence
    #   end = symbol in text file that represents the end of a sentence
    def set_symbols(self, start, end):
        self.start = start
        self.end = end

    def set_start(self, start):
        self.start = start

    def get_start(self):
        return self.start

    def set_end(self, end):
        self.end = end

    def get_end(self):
        return self.end


    # set_n(n)
    # sets the number of words per gram
    #   n = the number of words per gram
    def set_n(self, n):
        try:
            self.file.seek(0)
            tokens = self.file.read().split()
            self.n = n
            if n > 1:
                self.__construct_grams__(tokens)
            else:
                #n outside of acceptable range
                raise NException
        except NException:
            print("Error changing n value: n not in acceptable range (2-4)")

    def get_n(self):
        return self.n

    # generate()
    # constructs a sentence from ngrams taken from specified text file
    # returns sentence (string)
    def generate(self):
        sentence = ""

        #select starting ngram
        g = self.r.choice([x for x in self.grams if x[0] == self.start])

        #add words to sentence until end symbol is found
        while g[self.n-1] != self.end:
            matched = False

            #select a random ngram and check that the first n-1 items
            #   match the last n-1 items of the current sentence
            while not matched:
                matched = True
                x = self.r.choice(self.grams)
                for i in range(self.n - 1):
                    matched = matched and x[i] == g[i+1]

            #set matched ngram to current ngram and add to sentence
            g = x
            if g[0] != self.start:
                sentence += g[0] + " "

        #add remaining words in last ngram to sentence
        #   after end symbol is found
        if self.n > 2:
            for i in range(1, self.n - 1):
                sentence += g[i] + " "

        return sentence

# class NException
# raised when n value is not appropriate
class NException(Exception):
    pass

# class SymbolException
# raised when start or end symbols are not in file
class SymbolException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
