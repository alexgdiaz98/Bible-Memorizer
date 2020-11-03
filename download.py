#!/usr/bin/env python3
import argparse
import difflib
import json
import math
import os
import re
import requests
import sys

BOOKS = ['Gen', 'Ex', 'Lev', 'Num', 'Deut', 'Josh', 'Judg', 'Ruth', '1 Sam', '2 Sam', '1 Kings', '2 Kings', '1 Chron', '2 Chron', 'Ezra', 'Neh', 'Est', 'Job', 'Ps', 'Prov', 'Eccles', 'Song', 'Isa', 'Jer', 'Lam', 'Ezek', 'Dan', 'Hos', 'Joel', 'Amos', 'Obad', 'Jonah', 'Mic', 'Nah', 'Hab', 'Zeph', 'Hag', 'Zech', 'Mal', 'Matt', 'Mark', 'Luke', 'John', 'Acts', 'Rom', '1 Cor', '2 Cor', 'Gal', 'Eph', 'Phil', 'Col', '1 Thess', '2 Thess', '1 Tim', '2 Tim', 'Titus', 'Philem', 'Heb', 'James', '1 Pet', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Rev']

CHAPTER_LENS = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]

assert(len(CHAPTER_LENS) == 66)

def get_ESV():
    with open('config.json') as config_file:
        API_KEY = json.load(config_file)['ESV']
        
    print('Enter desired passsage (e.g. John 1:1, jn11.35, Genesis 1-3)')
    raw = input('Passage: ').replace(' ', '+')
    url = 'https://api.esv.org/v3/passage/text/?q=%s&include-headings=false&include-short-copyright=false&include-footnotes=false&include-passage-references=false&indent-poetry=false&indent-paragraphs=0' % (raw)
    r = requests.get(url=url, headers={'Authorization': '%s' % API_KEY})
    data = json.loads(r.text)
    
    if data['passages'] == []:
        sys.exit('Passage not found.')
        
    parsed = data['parsed'] # List of parsed passages
    print('Writing to %s ESV.txt...' % data['canonical'])
    passageID = 0
    with open('src/%s ESV.txt' % data['canonical'], 'wt') as output_file:
        for passage in parsed:
            start, end = str(passage[0]), str(passage[1])
            firstBook, firstChapter, firstVerse = int(start[:-6]), int(start[-6:-3]), int(start[-3:])
            lastBook, lastChapter, lastVerse = int(end[:-6]), int(end[-6:-3]), int(end[-3:])
            output_file.write(start + '-' + end + '\n')
            chapters = []
            for i in range(firstBook-1, lastBook):
                first = firstChapter if i == firstBook-1 else 1
                last = (lastChapter if i == lastBook else CHAPTER_LENS[i]) + 1
                chapters.append([str(num) for num in range(first, last)])
                    
            print('%s %d:%d - %s %d:%d' % (BOOKS[firstBook-1], firstChapter, firstVerse, BOOKS[lastBook-1], lastChapter, lastVerse))
            # Format JSON text into a list of strings, with one verse per string
            text = data['passages'][passageID]
            text = text.replace('\n', ' ')
            text = re.sub(r' +', ' ', text)             # e.g. '     ' -> ' '
            text = re.sub(r' *\[(\d+)\] *', r'\n\1. ', text).strip()   # e.g. ' [5] ' -> '\n5. '
            bookI = 0
            chapterI = 0
            for verseI, verse in enumerate(text.split('\n')):
                if verseI == 0 or verse.split(' ')[0] == '1':
                    output_file.write(BOOKS[firstBook + bookI - 1] + ' ' + chapters[bookI][chapterI] + '\n')
                    chapterI += 1
                    if chapterI == len(chapters[bookI]):
                        bookI += 1
                        chapterI = 0
                        
                output_file.write(verse + '\n') 
                    
            passageID += 1

if __name__ == '__main__':
    get_ESV()