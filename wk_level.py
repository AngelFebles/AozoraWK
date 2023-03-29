#This code reads japanese text from text.txt and determines the minimum Wanikani level needed 
#to read 80%, 85%, 90%, and 95% of the text

import json
import re
import numpy as np

def get_kanji():
    '''Sort list of kanji from WK API into levels (downloaded separately)'''
    kanji_level_map = {}
    lkeys = range(1,61)
    level_kanji_map = dict(zip(lkeys, ([] for _ in lkeys)))

    with open('kanji_levels/0120.json', encoding="utf-8") as f:
        data = json.loads(f.read())
    for i in data["data"]:
        kanji_level_map[i['data']['characters']] = i['data']['level']
        level_kanji_map[int(i['data']['level'])].append(i['data']['characters'])
    f.close()

    with open('kanji_levels/2140.json', encoding="utf-8") as f:
        data = json.loads(f.read())
    for i in data["data"]:
        kanji_level_map[i['data']['characters']] = i['data']['level']
        level_kanji_map[int(i['data']['level'])].append(i['data']['characters'])
    f.close()

    with open('kanji_levels/4160.json', encoding="utf-8") as f:
        data = json.loads(f.read())
    for i in data["data"]:
        kanji_level_map[i['data']['characters']] = i['data']['level']
        level_kanji_map[int(i['data']['level'])].append(i['data']['characters'])
    f.close()

    return kanji_level_map, level_kanji_map


def get_level(book, kanji_level_map):
    '''Gets all of the kanji from the text and finds the lowest level needed to be able to
    read [pct]% of the unique kanji.'''

    bk_text = re.findall(r'[㐀-䶵一-鿋豈-頻]',book)

    bk_text = set(bk_text)
    kanji_levels = []

    for item in bk_text:
        if item in kanji_level_map.keys():
            kanji_levels.append(kanji_level_map[item])
        else:
            kanji_levels.append(61)
    if kanji_levels == []:
        return []
    else:
        return [int(np.percentile(kanji_levels, 80)),int(np.percentile(kanji_levels, 85)),
        int(np.percentile(kanji_levels, 90)),int(np.percentile(kanji_levels, 95))]


def format_output(lvl):
    '''Formats output for printing'''
   
    for i in range(len(lvl)):
        if lvl[i]==61:
            lvl[i] = "X"
        else:
            lvl[i] = str(lvl[i])

    lvl = '\t'.join(lvl)
    return '%s\n' % (lvl)

def print_output(lvl):
    print('-------------------------------------')
    print('WK level for 80% - '+ lvl[0])
    print('WK level for 85% - '+ lvl[1])
    print('WK level for 90% - '+ lvl[2])
    print('WK level for 95% - '+ lvl[3])
    print('-------------------------------------')


if __name__=="__main__":
    kanji_level_map, level_kanji_map = get_kanji()

    w = open('output.tsv','w')
    w.write('WK 80%\tWK 85%\tWK 90%\tWK 95%\n')


    #text.txt is the file containing the text to be analyzed
    #To try different text, either change this file's contents or change the path to a different one.

    with open("text.txt", encoding="utf-8") as f:
        a = f.read()
        lvl = get_level(a, kanji_level_map)

        if (lvl != []) and (min(lvl) != 61):

            w.write(format_output(lvl))
        
        print_output(lvl)


