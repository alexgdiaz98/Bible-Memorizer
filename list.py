#!/usr/bin/env python3
import argparse
import difflib
import json
import math
import os
import re
import requests

"""
Enumeration of text styling options in ther terminal

"""
class bcolors:
    HEAD = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    parser = argparse.ArgumentParser('Memorize Scripture through typing.')
    parser.add_argument('--cheat', '-c', type=bool, nargs='?')
    parser.add_argument('filename', type=argparse.FileType('r'), nargs='?')
    args = parser.parse_args()
    if args.filename is not None:
        with args.filename as text_file:
            lines = text_file.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].replace('\n', '')
    else:
        with open('config.json') as config_file:
            API_KEY = json.load(config_file)["API_KEY"]
        print("Enter desired passsage (e.g. John 1:1, jn11.35, Genesis 1-3)")
        passage = input("Passage: ").replace(' ','+')
        url = "https://api.esv.org/v3/passage/text/?q=%s&include-headings=false&include-short-copyright=false&include-footnotes=false&include-passage-references=false&include-first-verse-numbers=false" % (passage)
        r = requests.get(url=url, headers={'Authorization': "%s" % API_KEY})
        data = json.loads(r.text)
        text = data["passages"][0]
        text = text.replace('\n','')
        text = re.sub(r' *\[\d+\] *', '\n', text)
        text = re.sub(r' +',' ',text)
        lines = text.split('\n')
        lines = lines[1:]
    os.system('cls' if os.name == 'nt' else 'clear')
    start = int(input("Starting Verse: " + bcolors.OKGREEN))
    end = input(bcolors.ENDC + "Ending Verse: " + bcolors.OKGREEN)
    if end == "":
        end = start
    elif end == "end":
        end = len(lines)
    else:
        end = int(end)
    if input(bcolors.ENDC + "Show verses? (y/n): " + bcolors.OKGREEN) == "y":
        print()
        for i in range(start-1,end):
            print(bcolors.HEAD + "[%d] " % (i+1) + bcolors.ENDC + lines[i], end=' ')
        print("\n")
    print(bcolors.ENDC, end='')
    if args.cheat == True:
        check_verses(lines, start, end, True)
    else:
        check_verses(lines, start, end, False)

def check_verses(lines, start, end, cheat):
    for i in range(start-1, end):
        if (cheat):
            print("%sVerse %d:%s %s" % (bcolors.HEAD, i+1, bcolors.ENDC, lines[i]))
            a = input("      %s%s>%s " % (' '*len(str(i+1)), bcolors.HEAD, bcolors.ENDC))
        else:
            a = input("%sVerse %s:%s " % (bcolors.HEAD, str(i+1), bcolors.ENDC))
        b = ''.join(lines[i])
        score_verse(a,b)

def score_verse(input, verse):
    count = 0
    correction = ""
    in_add = False
    in_sub = False
    os.system('cls' if os.name == 'nt' else 'clear')
    for i,s in enumerate(difflib.ndiff(input, verse)):
        if s[0]==' ':
            if in_add:
                correction += "%s)%s%c" % (bcolors.HEAD, bcolors.ENDC, s[-1])
                in_add = False
            elif in_sub:
                correction += "%s]%s%c" % (bcolors.FAIL, bcolors.ENDC, s[-1])
                in_sub = False
            else:
                correction += str(s[-1])
        elif s[0]=='-':
            count += 1
            #print(u'Delete "{}" from position {}'.format(s[-1],i))
            if in_add:
                correction += "%s)%s[%s%c" % (bcolors.HEAD, bcolors.FAIL, bcolors.ENDC, s[-1])
                in_add = False
                in_sub = True
            elif in_sub:
                correction += "%c" % s[-1]
            else:
                correction += "%s[%s%c" % (bcolors.FAIL, bcolors.ENDC, s[-1])
                in_sub = True
        elif s[0]=='+':
            count += 1
            #print(u'Add "{}" to position {}'.format(s[-1],i)) 
            if in_add:
                correction += "%c" % s[-1]
            elif in_sub:
                correction += "%s]%s(%s%c" % (bcolors.FAIL, bcolors.HEAD, bcolors.ENDC, s[-1])
                in_sub = False
                in_add = True
            else:
                correction += "%s(%s%c" % (bcolors.HEAD, bcolors.ENDC, s[-1])
                in_add = True
    if in_add:
        correction += bcolors.HEAD + ")" + bcolors.ENDC
    if in_sub:
        correction += bcolors.FAIL + "]" + bcolors.ENDC
    print(correction)
    print(str(count) + " errors.")   
    print()

if __name__=="__main__":
    main()
