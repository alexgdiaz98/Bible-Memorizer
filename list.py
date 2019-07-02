#!/usr/bin/env python3
import argparse
import difflib
import json
import math
import os
import re
import requests

# Enumeration of text styling options in ther terminal
class bcolors:
    HEAD = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Use ESV API key to pull scripture
def get_ESV():
    with open('config.json') as config_file:
        API_KEY = json.load(config_file)['API_KEY']
        
    print('Enter desired passsage (e.g. John 1:1, jn11.35, Genesis 1-3)')
    passage = input('Passage: ').replace(' ','+')
    url = 'https://api.esv.org/v3/passage/text/?q=%s&include-headings=false&include-short-copyright=false&include-footnotes=false&include-passage-references=false&include-first-verse-numbers=false' % (passage)
    r = requests.get(url=url, headers={'Authorization': '%s' % API_KEY})
    
    data = json.loads(r.text)
    if data['passages'] == []:
        print('Passage not found.')
        return -1
    
    text = data['passages'][0]
    text = text.replace('\n','')
    lines = re.sub(r' *\[\d+\] *', '\n', text) # e.g. ' [5] ' -> '\n'
    lines = re.sub(r' +',' ',lines) # e.g. '     ' -> ' '
    lines = lines.split('\n')
    lines = lines[1:]
    return lines

def main():
    parser = argparse.ArgumentParser('Memorize Scripture through typing.')
    parser.add_argument('--cheat', '-c', type=bool, nargs='?')
    parser.add_argument('filename', type=argparse.FileType('r'), nargs='?')
    args = parser.parse_args()
    os.system('cls' if os.name == 'nt' else 'clear') # Clears terminal
    
    if args.filename is not None:
        # Read argument as file
        with args.filename as text_file:
            lines = text_file.readlines()
            for line in iter(lines):
                line = line.replace('\n', '')
    else:
        lines = get_ESV()
        if lines == -1:
            return -1
    
    print('%d verses' % len(lines))
    start = int(input('Starting Verse: ' + bcolors.OKGREEN))
    if start < 1 or start > len(lines):
        print('Invalid Range')
        return -1
    end = input(bcolors.ENDC + 'Ending Verse: ' + bcolors.OKGREEN)
    if end == '':
        end = start
    elif end == 'end':
        end = len(lines)
    else:
        end = int(end)
        if end > len(lines) or end < start:
            print('Invalid Range')
            return -1
        
    if input(bcolors.ENDC + 'Show verses? (y/n): ' + bcolors.OKGREEN) == 'y':
        print()
        for i in range(start-1,end):
            print(bcolors.HEAD + '[%d] ' % (i+1) + bcolors.ENDC + lines[i], end=' ')
        print("\n")
    print(bcolors.ENDC, end='')
    if args.cheat == True:
        study_verses(lines, start, end, True)
    else:
        study_verses(lines, start, end, False)

def study_verses(lines, start, end, cheat):
    for i in range(start-1, end):
        if (cheat):
            print('%sVerse %d:%s %s' % (bcolors.HEAD, i+1, bcolors.ENDC, lines[i]))
            a = input('      %s%s>%s ' % (' '*len(str(i+1)), bcolors.HEAD, bcolors.ENDC))
        else:
            a = input('%sVerse %s:%s ' % (bcolors.HEAD, str(i+1), bcolors.ENDC))
        b = ''.join(lines[i])
        review_verse(a,b)

def review_verse(input, verse):
    count = 0
    correction = ''
    in_add = False
    in_sub = False
    print(bcolors.OKGREEN)
    for i,s in enumerate(difflib.ndiff(input, verse)):
        if s[0]==' ':
            if in_add:
                correction += '%s)%s%c' % (bcolors.HEAD, bcolors.OKGREEN, s[-1])
                in_add = False
            elif in_sub:
                correction += '%s]%s%c' % (bcolors.FAIL, bcolors.OKGREEN, s[-1])
                in_sub = False
            else:
                correction += str(s[-1])
        elif s[0]=='-':
            count += 1
            #print(u'Delete "{}" from position {}'.format(s[-1],i))
            if in_add:
                correction += '%s)%s[%s%c' % (bcolors.HEAD, bcolors.FAIL, bcolors.OKGREEN, s[-1])
                in_add = False
                in_sub = True
            elif in_sub:
                correction += '%c' % s[-1]
            else:
                correction += '%s[%s%c' % (bcolors.FAIL, bcolors.OKGREEN, s[-1])
                in_sub = True
        elif s[0]=='+':
            count += 1
            #print(u'Add "{}" to position {}'.format(s[-1],i)) 
            if in_add:
                correction += '%c' % s[-1]
            elif in_sub:
                correction += '%s]%s(%s%c' % (bcolors.FAIL, bcolors.HEAD, bcolors.OKGREEN, s[-1])
                in_sub = False
                in_add = True
            else:
                correction += '%s(%s%c' % (bcolors.HEAD, bcolors.OKGREEN, s[-1])
                in_add = True
    if in_add:
        correction += bcolors.HEAD + ')'
    if in_sub:
        correction += bcolors.FAIL + ']'
    correction += bcolors.ENDC
    print(str(count), 'errors.', correction)
    print()

if __name__ == '__main__':
    main()
