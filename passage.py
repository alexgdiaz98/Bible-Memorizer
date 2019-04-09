import argparse
import difflib
import json
import math
import re
import requests

def main():
    parser = argparse.ArgumentParser('Memorize Scripture through typing.')
    parser.add_argument('filename', type=argparse.FileType('r'), nargs='?')
    
    args = parser.parse_args()
    if args.filename is not None:
        with args.filename as text_file:
            lines = text_file.readlines()
            for line in lines:
                line = line.replace('\n', '')
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
        print(lines)
    #print(lines, len(lines))
    entries = list(range(len(lines)))
    t = Tree(entries)
    #print(t)
    #print(''.join(lines), '\n')
    start = int(input("Starting Verse: "))
    end = int(input("Ending Verse: "))
    
    t = Tree(entries[start-1:end])
    check_verses(t, lines)
    
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

def check_verses(t, lines):
    if t.left is not None:
        check_verses(t.left, lines)
    if t.right is not None:
        check_verses(t.right, lines)
    if len(t.entry) == 1:
        i = t.entry[0]
        print("Verse %s: %s" % (i+1, lines[i]))
        a = input("      %s> " % (' '*len(str(i+1))))
        b = ''.join(lines[i])
        score_verse(a,b)
    else:
        verses = ' '.join(lines[t.entry[0]:t.entry[-1]+1])
        print("Verses %s-%s: %s" % (t.entry[0]+1, t.entry[-1]+1, verses))
        a = input("        %s> " % (' '*((len(str(t.entry[0]+1)))+len(str(t.entry[-1]+1)))))
        b = verses
        score_verse(a,b)

def score_verse(input, verse):
    count = 0
    print()
    for i,s in enumerate(difflib.ndiff(input, verse)):
        if s[0]==' ': continue
        elif s[0]=='-':
            count += 1
            print(u'Delete "{}" from position {}'.format(s[-1],i))
        elif s[0]=='+':
            count += 1
            print(u'Add "{}" to position {}'.format(s[-1],i)) 
    print(str(count) + " errors.")   
    print()

if __name__=="__main__":
    main()