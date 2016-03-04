import json


fr = open('dict.txt', 'r')

items = []

for line in fr.readlines():
    line = line.strip()

    word, meaning_str, *remain = line.split('<out>')

    raw_meanings = [x if x[-1] != '<' else x[:-1]
                    for x in meaning_str.split('<in>')]
    raw_examples = []
    if remain:
        # examples exists
        raw_examples = remain[0].split('<in>')
        # filter out blank string
        raw_examples = [e for e in raw_examples if e.strip() != '']
        examples = [{'sentence': sen.strip(), 'translation': trans.strip()}
                    for sen, trans in
                    zip(raw_examples[::2], raw_examples[1::2])]

    # Split meaning into part_of_speech and explanation
    meanings = [{'part_of_speech': (s.split('.')[0] + '.') if '.' in s else '',
                 'explanation': s.split('.')[1].strip() if '.' in s else s}
                for s in raw_meanings]

    item = {'word': word, 'meanings': meanings, 'examples': examples}
    items.append(item)

fo = open('items.json', 'w')
json.dump(items, fo, ensure_ascii=False, indent=4)

# compressed json
f_comp = open('items_comp.json', 'w')
json.dump(items, f_comp, ensure_ascii=False)

fr.close()
fo.close()
