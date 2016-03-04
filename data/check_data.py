import json


def count_bad(num):
    with open('dict.txt') as f:
        count = 0
        for l in f:
            l = l.strip()
            if len(l.split('<out>')) == num:
                count += 1
                print(l.split('<out>'))
    return count


def check_meanings():
    with open('items.json') as f:
        items = json.load(f)
        count = 0
        for item in items:
            meanings = item['meanings']
            for meaning in meanings:
                if '.' in meaning and ' ' not in meaning:
                    print(item)
                    count += 1
    return count


def check_poc():
    with open('items.json') as f:
        items = json.load(f)
        count = 0
        for item in items:
            meanings = item['meanings']
            for meaning in meanings:
                if '.' not in meaning:
                    print(item)
                    count += 1
    return count
