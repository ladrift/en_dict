"""English dictionary implementation.

Support add word item, add example sentences."""
import json
import time

from trie import Trie


class Example(object):
    def __init__(self, sentence, translation):
        self.sentence = sentence
        self.translation = translation

    def __repr__(self):
        return "<Example: {}, {}>".format(self.sentence, self.translation)


class Meaning(object):
    def __init__(self, part_of_speech, explanation):
        self.part_of_speech = part_of_speech
        self.explanation = explanation

    def __repr__(self):
        return "<Meaning: {}, {}>"\
            .format(self.part_of_speech, self.explanation)


class Item(object):
    def __init__(self, word, meanings, examples):
        self.word = word
        self.meanings = meanings  # a list of Meaning
        self.examples = examples  # a list of Example

    def __repr__(self):
        return "<Item: {}, {}, {}>"\
            .format(self.word, self.meanings, self.examples)

    def to_dict(self):
        meanings = [meaning.__dict__ for meaning in self.meanings]
        examples = [example.__dict__ for example in self.examples]
        return dict(word=self.word, meanings=meanings, examples=examples)


class Dictionary(Trie):
    def __init__(self, dict_filename=None):
        super().__init__()
        if dict_filename:
            self.load_data(dict_filename)

    def insert(self, word, meanings, examples):
        """Insert an Item to Dictionary.
            Args:
                word: a string of word.
                meanings: a list of Meaning object or
                    two-tuple of `part_of_speech` and `explanation`.
                examples: a list of Example object or
                    two-tuple of `sentence` and `translation` string
        """
        if isinstance(meanings, (tuple, list)):
            if all(isinstance(meaning, tuple) and len(meaning) == 2
                   for meaning in meanings):
                # Transform it to Meaning objects.
                meanings = [Meaning(poc, explain) for poc, explain in meanings]
            elif all(isinstance(meaning, Meaning) for meaning in meanings):
                # Do nothing
                pass
            else:
                raise TypeError('`meanings` should be a list of Meaning object\
                        or two-tuple of `part_of_speech` and `explanation`')
        else:
            raise TypeError('`meanings` should be a list of Meaning object\
                        or two-tuple of `part_of_speech` and `explanation`')

        if isinstance(examples, (tuple, list)):
            if all(isinstance(example, tuple) and len(example) == 2
                   for example in examples):
                # Transform it to Example objects.
                examples = [Example(sen, tran) for sen, tran in examples]
            elif all(isinstance(example, Example) for example in examples):
                # Do nothing
                pass
            else:
                raise TypeError('`examples` should be a list of Example object\
                            or two-tuple of `sentence` and `translation`')
        else:
            raise TypeError('`examples` should be a list of Example object\
                        or two-tuple of `sentence` and `translation`')

        item = Item(word, meanings, examples)
        super().insert(word, item)

    def find(self, word):
        """Find word with tolerance of mis-capitalize or non-capitalize."""
        result = super().find(word)
        result = result if result is not None \
            else super().find(word.capitalize()) if word.islower() \
            else super().find(word.lower())

        return result

    def load_data(self, filename):
        """Load data from json file to Dictionary object"""
        items = json.load(open(filename))
        for item in items:
            self.insert(item['word'],
                        [(m['part_of_speech'], m['explanation'])
                         for m in item['meanings']],
                        [(e['sentence'], e['translation'])
                         for e in item['examples']]
                        )

if __name__ == "__main__":
    dic = Dictionary(dict_filename='data/items_comp.json')

    start = time.time()
    dic.find('zoom')
    end = time.time()
    print('Find time:', end - start)

    words = [item['word'] for item in json.load(open('data/items.json'))]
    from collections import defaultdict
    time_dict = defaultdict(list)
    for word in words:
        assert dic.find(word) is not None, "'{}' is not found!".format(word)
        start = time.time()
        for _ in range(100):
            dic.find(word)
        end = time.time()
        if len(word) == 29:
            print(word)
        time_dict[len(word)].append((end-start) / 1000)

    time_dict = {k: sum(v) / len(v) for k, v in time_dict.items()}
    import pprint; pprint.pprint(time_dict)

    with open('find_time.csv', 'w') as f:
        f.writelines([','.join((str(k), str(v))) + '\n' for k, v in time_dict.items()])

    # test prefix 'downtown'
    for value in dic.prefix_recommend('downtown'):
        print(value)
