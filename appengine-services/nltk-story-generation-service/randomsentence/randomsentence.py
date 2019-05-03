import nltk
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
nltk.download('treebank')
# nltk.download('gutenberg')
# nltk.download('punkt')

from nltk.corpus import brown
# from nltk.corpus import nps_chat
# from nltk.corpus import genesis
# from nltk.corpus import gutenberg
from nltk.corpus import treebank

# from nltk.corpus import snowball_data

import markovify
try:
    from secrets import choice
except ImportError:
    from random import choice

__doctest_skip__ = ['RandomSentence.get_tagged_sent']


class RandomSentence:
    def __init__(self, do_markovify=True):
        print("tagging the datasets and markovifying them ... please wait!")
        # print(list(brown.tagged_sents()))
        # print(list(nps_chat.tagged_words()))
        # with open("reddit_apple_android.txt", "w") as text_file:
        #     self.tagged_sents = list(nltk.pos_tag(sent) for sent in (text_file.sents('reddit_apple_android.txt')))

        self.tagged_sents = list(brown.tagged_sents())
        # self.tagged_sents = list(treebank.tagged_sents())
        # self.tagged_sents = list(nltk.pos_tag(sent) for sent in (gutenberg.sents('austen-emma.txt')))
        # self.tagged_sents = list(nltk.pos_tag(sent) for sent in (gutenberg.sents('quora.txt')))
        # self.tagged_sents = list(nltk.pos_tag(sent) for sent in (gutenberg.sents('reddit_apple_android.txt')))
        # self.tagged_sents = list(nltk.pos_tag(sent) for sent in (gutenberg.sents('hackernews.txt')))
        self.tagged_sents.append(list(treebank.tagged_sents()))
        # self.tagged_sents.append(list(nps_chat.tagged_words()))
        # self.tagged_sents.append(list(nltk.pos_tag(sent) for sent in (gutenberg.sents('austen-emma.txt'))))
        # self.tagged_sents.append(list(nltk.pos_tag(sent) for sent in (gutenberg.sents('chesterton-brown.txt'))))
        # self.tagged_sents.append(list(nltk.pos_tag(sent) for sent in (gutenberg.sents('austen-persuasion.txt'))))
        # self.tagged_sents.append(list(nltk.pos_tag(sent) for sent in (gutenberg.sents('austen-sense.txt'))))
        # self.tagged_sents.append(list(nltk.pos_tag(sent) for sent in (gutenberg.sents('reddit_apple_android.txt'))))
        # self.tagged_sents.append(list(nltk.pos_tag(sent) for sent in (genesis.sents('english-web.txt'))))
        # self.tagged_sents.append(list(nltk.pos_tag(gutenberg.sents('austen-persuasion.txt'))))
        # self.tagged_sents.append(list(nltk.pos_tag(gutenberg.sents('austen-sense.txt'))))
        # self.tagged_sents.append(list(nltk.pos_tag(genesis.sents('english-web.txt'))))
        # self.tagged_sents.append(list(genesis.tagged_words()))
        # self.tagged_sents.append(list(snowball_data.tagged_words()))  

        # print(self.tagged_sents)
        if do_markovify:
            self.model = markovify.Chain(self.tagged_sents, 2)

    def get_tagged_sent(self):
        # return list of tuples of non-space-separated strings
        # >>> random_sentence = RandomSentence()
        # >>> random_sentence.get_tagged_sent()
        # [('As', 'CS'), ('she', 'PPS'), ('was', 'BEDZ'), ('rather', 'QL'), 
        # ('tired', 'VBN'), ('this', 'DT'), ('evening', 'NN'), (',', ','), 
        # ('her', 'PP$'), ('simple', 'JJ'), ('``', '``'), ('Thank', 'VB'), 
        # ('you', 'PPO'), ('for', 'IN'), ('the', 'AT'), ('use', 'NN'), ('of', 'IN'), 
        # ('your', 'PP$'), ('bath', 'NN'), ("''", "''"), ('--', '--'), ('when', 'WRB'), 
        # ('she', 'PPS'), ('sat', 'VBD'), ('down', 'RP'), ('opposite', 'IN'), 
        # ('him', 'PPO'), ('--', '--'), ('spoken', 'VBN'), ('in', 'IN'), ('a', 'AT'), 
        # ('low', 'JJ'), ('voice', 'NN'), (',', ','), ('came', 'VBD'), ('across', 'RB'), 
        # ('with', 'IN'), ('coolnesses', 'NNS'), ('of', 'IN'), ('intelligence', 'NN'), 
        # ('and', 'CC'), ('control', 'NN'), ('.', '.')]
        
        try:
            return list(self.model.gen())
        except AttributeError:
            return choice(self.tagged_sents)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
