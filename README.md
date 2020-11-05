# Bible Memorizer
A tool to memorize passages of scripture through typing them repeatedly. Capable of passages from the ESV or any text you copy+paste.

## Dependencies
- python3

## API_KEY
To access the ESV API, you need an API KEY available [here](https://api.esv.org/docs/). Once you have an API KEY, create a `config.json` file with contents like so:
```json
{
    "ESV": "YoUr_ApI_kEy_HeRe"
}
```

## Usage
`python3 download.py` 

or

`./run.py [filename]`

Arguments:

`filename` - specifies file to read passage from. File must be formatted by download.py

Ex.
```
python3 download.py

Enter desired passsage (e.g. John 1:1, jn11.35, Genesis 1-3)
Passage: 2 John-Jude 3
```

Ex.
```
python3 run.py src/Romans+12+NASB.txt

Starting Verse ('s' to skip chapter): 1
Ending Verse: 21
```

