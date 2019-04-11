#!/usr/bin/env python3
import argparse
import difflib
import json
import math
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

class Tree(object):
    def __init__(self, entries):
        li = []
        if len(entries) == 1:
            self.entry = entries
            self.left = None
            self.right = None
        else:
            for i in entries:
                li.append(i)
            self.entry = li
            self.left = Tree(entries[:math.ceil(len(entries)/2)])
            self.right = Tree(entries[math.ceil(len(entries)/2):])
    def __repr__(self, level=0):
        ret = "\t"*level+repr(self.entry)+"\n"
        for child in (self.left, self.right):
            if child is not None:
                ret += child.__repr__(level+1)
        return ret

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
        #print(lines)
    #print(lines, len(lines))
    entries = list(range(len(lines)))
    t = Tree(entries)
    #print(t)
    #print(''.join(lines), '\n')
    print("\n"*50)
    start = int(input("Starting Verse: " + bcolors.OKGREEN))
    end = input(bcolors.ENDC + "Ending Verse: " + bcolors.OKGREEN)
    if end == "end":
        end = len(lines)
    else:
        end = int(end)
    if input(bcolors.ENDC + "Show verses? (y/n): " + bcolors.OKGREEN) == "y":
        print()
        for i in range(start-1,end):
            print(bcolors.HEAD + "[%d] " % (i+1) + bcolors.ENDC + lines[entries[i]], end=' ')
        print("\n")
    print(bcolors.ENDC, end='')
    t = Tree(entries[start-1:end])
    if args.cheat == True:
        check_verses(t, lines, True)
    else:
        check_verses(t, lines, False)

def check_verses(t, lines, cheat):
    if t.left is not None:
        check_verses(t.left, lines, cheat)
    if t.right is not None:
        check_verses(t.right, lines, cheat)
    if len(t.entry) == 1:
        i = t.entry[0]
        if (cheat):
            print("%sVerse%s %d: %s" % (bcolors.HEAD, bcolors.ENDC, i+1, lines[i]))
            a = input("      %s%s>%s " % (' '*len(str(i+1)), bcolors.HEAD, bcolors.ENDC))
        else:
            a = input("%sVerse %s:%s " % (bcolors.HEAD, str(i+1), bcolors.ENDC))
        b = ''.join(lines[i])
        score_verse(a,b)
    else:
        verses = ' '.join(lines[t.entry[0]:t.entry[-1]+1])
        if (cheat):
            print("%sVerses %s-%s:%s %s" % (bcolors.HEAD, t.entry[0]+1, t.entry[-1]+1, bcolors.ENDC, verses))
            a = input("        %s> " % (' '*((len(str(t.entry[0]+1)))+len(str(t.entry[-1]+1)))))
        else:
            a = input("%sVerses %s-%s:%s " % (bcolors.HEAD, str(t.entry[0]+1), str(t.entry[-1]+1), bcolors.ENDC))
        b = verses
        score_verse(a,b)

def score_verse(input, verse):
    count = 0
    correction = ""
    in_add = False
    in_sub = False
    print()
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