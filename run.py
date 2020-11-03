#!/usr/bin/env python3
import argparse
import difflib
import json
import math
import os
import re
import requests
import sys

passages = {}

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

def get_file(filename):
    print(filename)
    with open(filename, 'r') as input_file:
        passageID = ''
        chapter = ''
        for line in input_file:
            line = line.strip()
            if re.match(r'^\d{7,8}\-\d{7,8}$', line):
                passageID = line
                passages[passageID] = []
            elif re.match(r'^([123] )?[A-Z a-z]*\d{1,3}$', line):
                chapter = line
                passages[passageID].append((chapter, []))
            elif re.match(r'^\d{1,3}\. ', line):
                passages[passageID][-1][1].append(line)
            else:
                sys.exit('Invalid line in source: %s' % line)
    print(passages)

def main():
    # Argument
    parser = argparse.ArgumentParser('Memorize Scripture through typing.')
    parser.add_argument('filename', nargs=1)
    args = parser.parse_args()
    os.system('cls' if os.name == 'nt' else 'clear') # Clears terminal
    
    if args.filename is not None:
        # Read a text file (from the argument)
        get_file(args.filename[0])
    else:
        sys.exit('No filename provided')
    print('%d passage(s)' % len(passages.keys()))
    for passageID in passages.keys():
        for chapterI, chapter in enumerate(passages[passageID]):
            print(chapter[0])
            raw = input('Starting Verse (\'s\' to skip chapter): ' + bcolors.OKGREEN)
        firstVerse, lastVerse = int(chapter[1][0].split('.')[0]), int(chapter[1][-1].split('.')[0])
        if raw == 's':
            continue
        elif raw == '':
            start = firstVerse
        else:
            start = int(raw)
        if start < firstVerse or start > lastVerse:
            sys.exit('Invalid Range')
        end = input(bcolors.ENDC + 'Ending Verse: ' + bcolors.OKGREEN)
        if end == '':
            end = start
        elif end == 'end':
            end = lastVerse
        else:
            end = int(end)
            if end > lastVerse or end < start:
                sys.exit('Invalid Range')
            
        if input(bcolors.ENDC + 'Show verses? (y/n): ' + bcolors.OKGREEN) == 'y':
            print()
            for i in range(start, end+1):
                print(bcolors.ENDC + chapter[1][i-firstVerse], end=' ')
            print("\n")
        print(bcolors.ENDC, end='')
        study_verses(chapter[1][start-firstVerse:end-firstVerse+1])


def study_verses(verses):
    for verse in verses:
        verseNum = int(verse.split('.')[0])
        verse = re.sub(r'^\d{1,3}\. ', '', verse)
        raw = input('%sVerse %d:%s ' % (bcolors.HEAD, verseNum, bcolors.ENDC))
        review_verse(raw, verse)


def review_verse(input, verse):
    count = 0
    correction = ''
    in_add = False
    in_sub = False
    print(bcolors.OKGREEN)
    for i,s in enumerate(difflib.ndiff(input, verse)):
        if s[0] == ' ':
            if in_add:
                correction += '%s)%s%c' % (bcolors.HEAD, bcolors.OKGREEN, s[-1])
                in_add = False
            elif in_sub:
                correction += '%s]%s%c' % (bcolors.FAIL, bcolors.OKGREEN, s[-1])
                in_sub = False
            else:
                correction += str(s[-1])
        elif s[0] == '-':
            count += 1
            # print(u'Delete "{}" from position {}'.format(s[-1],i))
            if in_add:
                correction += '%s)%s[%s%c' % (bcolors.HEAD, bcolors.FAIL, bcolors.OKGREEN, s[-1])
                in_add = False
                in_sub = True
            elif in_sub:
                correction += '%c' % s[-1]
            else:
                correction += '%s[%s%c' % (bcolors.FAIL, bcolors.OKGREEN, s[-1])
                in_sub = True
        elif s[0] == '+':
            count += 1
            # print(u'Add "{}" to position {}'.format(s[-1],i))
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
    print(str(count), 'errors:', correction)
    print()


if __name__ == '__main__':
    main()
