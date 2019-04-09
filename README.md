# Bible Memorizer
A tool to memorize passages of scripture through typing them repeatedly. Capable of passages from the ESV or any text you copy+paste.

## Dependencies
- python3

## Usage
```python3 passage.py  [filename]```

Arguments:

```filename``` - Optional - specifies file to read passage from. If not included, the application asks for a passage reference and uses and ESV API to get a passage.

Ex.
```python3 passage.py

Enter desired passsage (e.g. John 1:1, jn11.35, Genesis 1-3)
Passage: Romans 12
Starting Verse: 1
Ending Verse: 21
```

Ex.
```python3 passage.py src/Romans+12+NASB.txt

Starting Verse: 1
Ending Verse: 21
```

## API_KEY
To access the ESV API, you need an API KEY available [here](https://api.esv.org/docs/). Once you have an API KEY, create a ```config.json``` file with contents like so:
```
{
    "API_KEY": "YoUr_ApI_kEy_HeRe"
}
```