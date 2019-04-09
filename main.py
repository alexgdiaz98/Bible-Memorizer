import requests
import json
import re

API_KEY = "MCoFGhLc0ZYGoK8lemx1BnSJp9SQQH99s7mCb72c"

def cleanhtml(raw_html):
    cleantext = raw_html.replace("<span class=\"it\">", "").replace("</span>", "")
    cleantext = cleantext.replace("<p class=\"p\">","").replace("</p>","")
    cleantext = re.sub(r'<sup id="+"', '', cleantext)
    return cleantext

#while True:
    print("Starting Verse: ", end='')
    #start = input()
    print("Ending Verse: ", end='')
    #end = input()
start = "Romans+12:1"
end = "-10"
message = "https://%s:@bibles.org/v2/passages.js?q[]=%s%s&version=eng-NASB&include_marginalia=false" % (API_KEY, str(start), str(end))
    #message = "https://bibles.org/v2/versions.js"
print(message)
data = API_KEY
r = requests.get(url=message)
data = json.loads(r.text)
print(cleanhtml(data["response"]["search"]["result"]["passages"][0]["text"]))


